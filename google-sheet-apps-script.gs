/**
 * whydoweneedai.com — Quiz lead handler (Google Apps Script)
 * ==========================================================
 *
 * This web app receives each quiz submission from the site (index.html /
 * quiz.html), appends it as a row to the linked Google Sheet, AND sends the
 * lead a follow-up email inviting them to complete the AI assessment.
 *
 * SETUP
 * -----
 * 1. Open the Google Sheet that collects leads → Extensions → Apps Script.
 * 2. Paste this whole file over the existing script (it keeps the append
 *    behaviour and adds the follow-up email).
 * 3. Edit the CONFIG block below — most importantly ASSESSMENT_FORM_URL once
 *    the assessment form exists. Until then the email still sends and simply
 *    tells the lead we'll be in touch.
 * 4. Deploy → Manage deployments → edit the existing deployment → New version
 *    → Deploy. The web app URL stays the same, so no site change is needed.
 *    (First-ever deploy: Deploy → New deployment → Web app → Execute as "Me",
 *    Access "Anyone", then paste the URL into SHEET_WEBAPP_URL in the site.)
 * 5. The first run asks for authorization (Sheets + send email as you) —
 *    approve it.
 *
 * The front end posts JSON as text/plain (no-cors, fire-and-forget), so this
 * script never blocks the score reveal and returns quickly.
 */

// ─── CONFIG ────────────────────────────────────────────────────────────────
var CONFIG = {
  // Tab within the spreadsheet to append rows to. Created if missing.
  SHEET_NAME: 'Leads',

  // Link the follow-up email points the lead to. Fill this in once the
  // assessment form page is live. Leave '' to send the email without a button.
  ASSESSMENT_FORM_URL: '',

  // Shown as the sender name; the address is the account that owns the script.
  FROM_NAME: 'whydoweneedai.com',

  // Reply-to address for the follow-up email (where lead replies should land).
  REPLY_TO: 'admin@whydoweneedai.com',

  // Optional: also send yourself a heads-up when a new lead comes in.
  // Set to '' to disable the internal notification.
  NOTIFY_EMAIL: 'admin@whydoweneedai.com'
};

// Column order for the Sheet. Header row is written automatically if the tab
// is empty. Keep these keys in sync with the payload the site sends.
var COLUMNS = [
  { key: 'timestamp',  header: 'Timestamp' },
  { key: 'firstName',  header: 'First name' },
  { key: 'lastName',   header: 'Last name' },
  { key: 'company',    header: 'Company' },
  { key: 'email',      header: 'Email' },
  { key: 'phone',      header: 'Phone' },
  { key: 'readyScore', header: 'AI ReadyScore' },
  { key: 'persona',    header: 'Persona' },
  { key: 'pain',       header: 'Pain' },
  { key: 'worry',      header: 'Worry' },
  { key: 'pageUrl',    header: 'Page URL' },
  { key: 'emailSent',  header: 'Follow-up sent' }
];

// ─── ENTRY POINT ───────────────────────────────────────────────────────────
function doPost(e) {
  try {
    var data = parseBody(e);

    var emailSent = '';
    if (isValidEmail(data.email)) {
      try {
        sendFollowUpEmail(data);
        emailSent = 'yes';
      } catch (mailErr) {
        emailSent = 'error: ' + mailErr;
        console.error('Follow-up email failed', mailErr);
      }
    } else {
      emailSent = 'skipped (no email)';
    }

    data.emailSent = emailSent;
    appendRow(data);
    notifyInternal(data);

    return json({ ok: true, emailSent: emailSent });
  } catch (err) {
    console.error('doPost failed', err);
    return json({ ok: false, error: String(err) });
  }
}

// Lets you open the web app URL in a browser to confirm it's deployed.
function doGet() {
  return json({ ok: true, service: 'whydoweneedai quiz handler' });
}

// ─── HELPERS ───────────────────────────────────────────────────────────────
function parseBody(e) {
  var raw = (e && e.postData && e.postData.contents) ? e.postData.contents : '{}';
  var obj = JSON.parse(raw);
  return {
    timestamp:  new Date(),
    firstName:  clean(obj.firstName),
    lastName:   clean(obj.lastName),
    company:    clean(obj.company),
    email:      clean(obj.email),
    phone:      clean(obj.phone),
    readyScore: obj.readyScore != null ? obj.readyScore : '',
    persona:    clean(obj.persona),
    pain:       clean(obj.pain),
    worry:      clean(obj.worry),
    pageUrl:    clean(obj.pageUrl)
  };
}

function appendRow(data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(CONFIG.SHEET_NAME);

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS.map(function (c) { return c.header; }));
  }
  sheet.appendRow(COLUMNS.map(function (c) {
    return data[c.key] != null ? data[c.key] : '';
  }));
}

function sendFollowUpEmail(data) {
  var name = data.firstName || 'there';
  var subject = 'Your AI ReadyScore — and your next step, ' + name;

  var cta = '';
  if (CONFIG.ASSESSMENT_FORM_URL) {
    cta =
      '<p style="margin:24px 0;">' +
        '<a href="' + escapeAttr(CONFIG.ASSESSMENT_FORM_URL) + '" ' +
          'style="display:inline-block;background:#4f46e5;color:#fff;' +
          'text-decoration:none;font-weight:800;padding:14px 26px;' +
          'border-radius:12px;font-family:Nunito,Arial,sans-serif;">' +
          'Start my free AI assessment →' +
        '</a>' +
      '</p>';
  } else {
    cta =
      '<p style="margin:24px 0;font-weight:700;">' +
        'We\'ll follow up shortly with a short assessment so we can map your ' +
        'first AI automation together.' +
      '</p>';
  }

  var scoreLine = (data.readyScore !== '' && data.readyScore != null)
    ? '<p style="margin:0 0 8px;font-size:16px;">Your AI ReadyScore came in at ' +
        '<b>' + escapeHtml(String(data.readyScore)) + '</b>' +
        (data.persona ? ' — <b>' + escapeHtml(data.persona) + '</b>.' : '.') +
      '</p>'
    : '';

  var htmlBody =
    '<div style="font-family:Nunito,Arial,sans-serif;color:#1f2430;' +
      'max-width:520px;margin:0 auto;line-height:1.5;">' +
      '<p style="font-size:18px;margin:0 0 16px;">Hi ' + escapeHtml(name) + ' 👋</p>' +
      '<p style="margin:0 0 12px;">Thanks for taking the AI readiness quiz' +
        (data.company ? ' for <b>' + escapeHtml(data.company) + '</b>' : '') + '!</p>' +
      scoreLine +
      '<p style="margin:12px 0;">The next step is a short assessment. It takes a ' +
        'few minutes and helps us map the single highest-ROI automation for you ' +
        '— no pressure, no jargon.</p>' +
      cta +
      '<p style="margin:24px 0 0;color:#6b7280;font-size:13px;">' +
        'Built by someone who was also confused by AI once.<br>' +
        'whydoweneedai.com</p>' +
    '</div>';

  var plainBody =
    'Hi ' + name + ',\n\n' +
    'Thanks for taking the AI readiness quiz' +
      (data.company ? ' for ' + data.company : '') + '!\n\n' +
    (scoreLine ? 'Your AI ReadyScore: ' + data.readyScore +
      (data.persona ? ' (' + data.persona + ')' : '') + '\n\n' : '') +
    'The next step is a short assessment that helps us map the single ' +
    'highest-ROI automation for you.\n\n' +
    (CONFIG.ASSESSMENT_FORM_URL
      ? 'Start here: ' + CONFIG.ASSESSMENT_FORM_URL + '\n\n'
      : 'We\'ll follow up shortly with the assessment.\n\n') +
    'whydoweneedai.com';

  MailApp.sendEmail({
    to: data.email,
    subject: subject,
    htmlBody: htmlBody,
    body: plainBody,
    name: CONFIG.FROM_NAME,
    replyTo: CONFIG.REPLY_TO
  });
}

function notifyInternal(data) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  try {
    MailApp.sendEmail({
      to: CONFIG.NOTIFY_EMAIL,
      subject: 'New quiz lead: ' + (data.firstName || '') + ' ' + (data.lastName || ''),
      body:
        'Name: ' + data.firstName + ' ' + data.lastName + '\n' +
        'Company: ' + data.company + '\n' +
        'Email: ' + data.email + '\n' +
        'Phone: ' + data.phone + '\n' +
        'AI ReadyScore: ' + data.readyScore + '\n' +
        'Persona: ' + data.persona + '\n' +
        'Pain: ' + data.pain + '\n' +
        'Worry: ' + data.worry + '\n' +
        'Page: ' + data.pageUrl + '\n' +
        'Follow-up email: ' + data.emailSent
    });
  } catch (err) {
    console.error('Internal notification failed', err);
  }
}

function isValidEmail(v) {
  return typeof v === 'string' && /.+@.+\..+/.test(v);
}

function clean(v) {
  return (v == null) ? '' : String(v).trim();
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function escapeAttr(s) {
  return escapeHtml(s).replace(/"/g, '&quot;');
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

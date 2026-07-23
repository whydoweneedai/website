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
  // Tab quiz leads are appended to. Created if missing.
  SHEET_NAME: 'Leads',

  // Tab assessment-form submissions are appended to. Created if missing.
  ASSESSMENT_SHEET_NAME: 'Assessments',

  // Link the follow-up email points the lead to. Contact fields are appended as
  // query params so the form prefills for returning leads.
  ASSESSMENT_FORM_URL: 'https://whydoweneedai.com/assessment.html',

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

// Column order for the Assessments tab (assessment.html submissions).
var ASSESSMENT_COLUMNS = [
  { key: 'timestamp',         header: 'Timestamp' },
  { key: 'firstName',         header: 'First name' },
  { key: 'lastName',          header: 'Last name' },
  { key: 'email',             header: 'Email' },
  { key: 'company',           header: 'Company' },
  { key: 'role',              header: 'Role' },
  { key: 'industry',          header: 'Industry' },
  { key: 'teamSize',          header: 'Team size' },
  { key: 'timeEaters',        header: 'Biggest time-eaters' },
  { key: 'handoffTask',       header: 'Task to hand off' },
  { key: 'leadSource',        header: 'How customers find them' },
  { key: 'leadLeak',          header: 'Where leads leak' },
  { key: 'repeatedQuestions', header: 'Repeated questions' },
  { key: 'dataLocation',      header: 'Where data lives' },
  { key: 'toolsUsed',         header: 'Tools used' },
  { key: 'goal',              header: '90-day goal' },
  { key: 'other',             header: 'Other notes' },
  { key: 'readyScore',        header: 'AI ReadyScore' },
  { key: 'pageUrl',           header: 'Page URL' },
  { key: 'emailSent',         header: 'Confirmation sent' }
];

// ─── ENTRY POINT ───────────────────────────────────────────────────────────
function doPost(e) {
  try {
    var obj = parseJsonBody(e);
    return (obj.type === 'assessment')
      ? handleAssessment(obj)
      : handleQuizLead(obj);
  } catch (err) {
    console.error('doPost failed', err);
    return json({ ok: false, error: String(err) });
  }
}

// Quiz submission (index.html / quiz.html): log + send the follow-up email that
// invites the lead to complete the assessment.
function handleQuizLead(obj) {
  var data = normalizeQuizLead(obj);

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
  appendRow(CONFIG.SHEET_NAME, COLUMNS, data);
  notifyInternal(
    'New quiz lead: ' + data.firstName + ' ' + data.lastName,
    quizLeadSummary(data)
  );

  return json({ ok: true, type: 'quiz', emailSent: emailSent });
}

// Assessment submission (assessment.html): log + send a thank-you confirmation.
function handleAssessment(obj) {
  var data = normalizeAssessment(obj);

  var emailSent = '';
  if (isValidEmail(data.email)) {
    try {
      sendAssessmentReceivedEmail(data);
      emailSent = 'yes';
    } catch (mailErr) {
      emailSent = 'error: ' + mailErr;
      console.error('Assessment confirmation email failed', mailErr);
    }
  } else {
    emailSent = 'skipped (no email)';
  }

  data.emailSent = emailSent;
  appendRow(CONFIG.ASSESSMENT_SHEET_NAME, ASSESSMENT_COLUMNS, data);
  notifyInternal(
    '📋 New AI assessment: ' + data.firstName + ' ' + data.lastName +
      (data.company ? ' (' + data.company + ')' : ''),
    assessmentSummary(data)
  );

  return json({ ok: true, type: 'assessment', emailSent: emailSent });
}

// Lets you open the web app URL in a browser to confirm it's deployed.
function doGet() {
  return json({ ok: true, service: 'whydoweneedai quiz handler' });
}

// ─── HELPERS ───────────────────────────────────────────────────────────────
function parseJsonBody(e) {
  var raw = (e && e.postData && e.postData.contents) ? e.postData.contents : '{}';
  return JSON.parse(raw);
}

function normalizeQuizLead(obj) {
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

function normalizeAssessment(obj) {
  return {
    timestamp:         new Date(),
    firstName:         clean(obj.firstName),
    lastName:          clean(obj.lastName),
    email:             clean(obj.email),
    company:           clean(obj.company),
    role:              clean(obj.role),
    industry:          clean(obj.industry),
    teamSize:          clean(obj.teamSize),
    timeEaters:        clean(obj.timeEaters),
    handoffTask:       clean(obj.handoffTask),
    leadSource:        clean(obj.leadSource),
    leadLeak:          clean(obj.leadLeak),
    repeatedQuestions: clean(obj.repeatedQuestions),
    dataLocation:      clean(obj.dataLocation),
    toolsUsed:         clean(obj.toolsUsed),
    goal:              clean(obj.goal),
    other:             clean(obj.other),
    readyScore:        obj.readyScore != null ? obj.readyScore : '',
    pageUrl:           clean(obj.pageUrl)
  };
}

function appendRow(sheetName, columns, data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) sheet = ss.insertSheet(sheetName);

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(columns.map(function (c) { return c.header; }));
  }
  sheet.appendRow(columns.map(function (c) {
    return data[c.key] != null ? data[c.key] : '';
  }));
}

function sendFollowUpEmail(data) {
  var name = data.firstName || 'there';
  var subject = 'Your AI ReadyScore — and your next step, ' + name;
  var formUrl = assessmentUrlFor(data);

  var cta = '';
  if (formUrl) {
    cta =
      '<p style="margin:24px 0;">' +
        '<a href="' + escapeAttr(formUrl) + '" ' +
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
    (formUrl
      ? 'Start here: ' + formUrl + '\n\n'
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

// Thank-you email once someone completes the assessment form.
function sendAssessmentReceivedEmail(data) {
  var name = data.firstName || 'there';
  var subject = 'We\'ve got your assessment, ' + name + ' ✅';

  var htmlBody =
    '<div style="font-family:Nunito,Arial,sans-serif;color:#1f2430;' +
      'max-width:520px;margin:0 auto;line-height:1.5;">' +
      '<p style="font-size:18px;margin:0 0 16px;">Hi ' + escapeHtml(name) + ' 🎉</p>' +
      '<p style="margin:0 0 12px;">Thanks for sharing how things run' +
        (data.company ? ' at <b>' + escapeHtml(data.company) + '</b>' : '') + '.</p>' +
      '<p style="margin:12px 0;">We\'ll review your answers and put together a ' +
        'ranked list of the highest-ROI ways AI can save you time — in plain ' +
        'language, tied to what you actually do. Keep an eye on your inbox; ' +
        'we\'ll be in touch soon.</p>' +
      '<p style="margin:24px 0 0;color:#6b7280;font-size:13px;">' +
        'Built by someone who was also confused by AI once.<br>' +
        'whydoweneedai.com</p>' +
    '</div>';

  var plainBody =
    'Hi ' + name + ',\n\n' +
    'Thanks for sharing how things run' +
      (data.company ? ' at ' + data.company : '') + '.\n\n' +
    'We\'ll review your answers and put together a ranked list of the ' +
    'highest-ROI ways AI can save you time. Keep an eye on your inbox — ' +
    'we\'ll be in touch soon.\n\n' +
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

// Build the assessment form link with the lead's contact fields as query params
// so the form prefills for them. Returns '' if no form URL is configured.
function assessmentUrlFor(data) {
  if (!CONFIG.ASSESSMENT_FORM_URL) return '';
  var q = [];
  if (data.firstName) q.push('fn=' + encodeURIComponent(data.firstName));
  if (data.lastName)  q.push('ln=' + encodeURIComponent(data.lastName));
  if (data.email)     q.push('e='  + encodeURIComponent(data.email));
  if (data.company)   q.push('c='  + encodeURIComponent(data.company));
  if (data.readyScore !== '' && data.readyScore != null) {
    q.push('s=' + encodeURIComponent(data.readyScore));
  }
  var sep = CONFIG.ASSESSMENT_FORM_URL.indexOf('?') === -1 ? '?' : '&';
  return q.length ? CONFIG.ASSESSMENT_FORM_URL + sep + q.join('&')
                  : CONFIG.ASSESSMENT_FORM_URL;
}

function quizLeadSummary(data) {
  return 'Name: ' + data.firstName + ' ' + data.lastName + '\n' +
    'Company: ' + data.company + '\n' +
    'Email: ' + data.email + '\n' +
    'Phone: ' + data.phone + '\n' +
    'AI ReadyScore: ' + data.readyScore + '\n' +
    'Persona: ' + data.persona + '\n' +
    'Pain: ' + data.pain + '\n' +
    'Worry: ' + data.worry + '\n' +
    'Page: ' + data.pageUrl + '\n' +
    'Follow-up email: ' + data.emailSent;
}

function assessmentSummary(data) {
  return 'Name: ' + data.firstName + ' ' + data.lastName + '\n' +
    'Email: ' + data.email + '\n' +
    'Company: ' + data.company + '\n' +
    'Role: ' + data.role + '\n' +
    'Industry: ' + data.industry + '\n' +
    'Team size: ' + data.teamSize + '\n\n' +
    'Biggest time-eaters:\n' + data.timeEaters + '\n\n' +
    'Task to hand off:\n' + data.handoffTask + '\n\n' +
    'How customers find them: ' + data.leadSource + '\n' +
    'Where leads leak:\n' + data.leadLeak + '\n\n' +
    'Repeated questions:\n' + data.repeatedQuestions + '\n\n' +
    'Where data lives: ' + data.dataLocation + '\n' +
    'Tools used: ' + data.toolsUsed + '\n\n' +
    '90-day goal:\n' + data.goal + '\n\n' +
    'Other notes:\n' + data.other + '\n\n' +
    'AI ReadyScore (from quiz): ' + data.readyScore + '\n' +
    'Confirmation email: ' + data.emailSent;
}

function notifyInternal(subject, body) {
  if (!CONFIG.NOTIFY_EMAIL) return;
  try {
    MailApp.sendEmail({ to: CONFIG.NOTIFY_EMAIL, subject: subject, body: body });
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

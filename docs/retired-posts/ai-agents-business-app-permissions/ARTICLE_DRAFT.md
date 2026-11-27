# AI Agents Are Moving Into Your Business Apps. Set the Rules Before They Act.

*October 9, 2026 · News & Signals · Editorial draft*

An assistant that reads a customer inquiry is useful. One that changes the customer's CRM record is operational. One that sends a price under your company's name has made a business commitment.

Those are three different levels of authority. Recent announcements from Google and Microsoft are pushing the boundary closer to everyday work.

## What changed

Google Cloud announced a universal Gemini work agent on October 8, 2026, describing a system that can use skills and tools across enterprise applications. Google emphasizes agent identity, permission controls, audit trails, and spending limits. This is a vendor announcement, not an independent reliability result.

Source: https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026

Google Workspace announced integrations with tools including HubSpot, QuickBooks, Salesforce, Asana, and Mailchimp on September 15. Google marked the rollout available to eligible editions and says admins can disable third-party connectors. Its September 30 correction updated the admin path. Connecting a service does not automatically authorize every action.

Source: https://workspaceupdates.googleblog.com/2026/09/connect-to-more-tools-with-gemini-in-Google-Workspace.html

Microsoft's September 25 Copilot announcement described Home, Code, and Autopilot, an agent meant to work while its user is away. Home and Code were announced for gradual Frontier rollout, with Autopilot to enter private preview. A preview is not general availability.

Source: https://news.microsoft.com/source/emea/2026/09/new-microsoft-copilot-brings-home-code-and-autopilot-together

## The permission decision

Treat access as four separate boundaries: **read** a record, **draft** a response, **stage** a change for review, and **commit** an action that changes the world outside the assistant. These boundaries should not carry the same approval policy. A wrong draft is easier to correct than a mistaken customer quote or invoice change.

## The Agent Action Contract

Copy these fields before enabling any business connector:

- **Job:** What single outcome is in scope?
- **Source of truth:** Which approved record resolves conflicts?
- **May read:** Which inboxes, folders, and fields?
- **May draft:** Which messages, notes, and summaries?
- **May stage:** Which proposed changes require review?
- **May commit without approval:** List exact actions, or write 'none.'
- **Never touch:** Which records, financial changes, deletions, or exports?
- **Escalation:** When must a person decide?
- **Evidence:** Where are sources, approvals, and actions logged?
- **Recovery:** Who can undo mistakes?
- **Stop rule:** Which error pauses the pilot?

A prompt asking the AI to be careful is not an enforceable permission policy.

## A worked example

*Illustrative, not a real customer case or first-hand test.* A contractor wants to save time on incoming inquiries. Start with synthetic emails and sample CRM records. Permit the assistant to read, draft replies, and propose CRM notes. Keep all sends and record edits behind human approval. Block quoting prices, promising dates, merging contacts, and touching invoices.

Prepare 20 synthetic cases, including missing information, duplicate names, complaints, and discount requests. Log whether the tool selected the right record, asked for missing facts, and respected forbidden actions. These are a test plan, not claimed test results. If quality is adequate, evaluate a narrow approved pilot including correction and review time.

## Act, watch, wait

**Act:** Audit workspace connectors, turn off unnecessary connections, select one low-risk workflow, and complete the Action Contract before testing with approved non-sensitive data.

**Watch:** Verify plan eligibility, real connector capabilities, approval gates, audit logs, spending controls, and recoverability. Calculate time saved after review and mistakes.

**Wait:** Avoid autonomous refunds, payments, bulk emails, deletions, and sensitive exports without documented safeguards and a real business need.

## The skeptical case

Rules-based automation may still be more reliable and economical for deterministic work. Agent access does not eliminate hallucinations, misleading source content, or privacy risks. Announcements are not evidence that every account can perform every action. This article distinguishes vendor statements from editorial inference and does not claim hands-on product tests.

See our guides: [AI vs. automation](/blog/ai-vs-automation/), [data handling](/blog/data-ai-tools/), and [evaluating pilots](/blog/evaluate-ai-pilot/).

## The connection

Perhaps enterprise agents take longer to reach small businesses than today's demos imply. That is a fair skeptical forecast. But access to mail, calendars, and customer records already matters. The competitive advantage is not the flashiest assistant; it is knowing what it may read, propose, change, and never touch.

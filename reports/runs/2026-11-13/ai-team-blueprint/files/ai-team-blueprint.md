# AI Team Blueprint v1: Missing-Records Chase

## 1. Use case
An AI team that finds which of your 40 clients are missing receipts or bank statements each month, drafts the chase emails for your approval, and tracks replies until the records are complete.

**Why (your answers):**
- Chasing is your biggest time sink, about 25 hrs/month.
- You use Xero, Dext, Gmail and Drive, so the data already exists.
- You're comfortable with no-code tools but not code.
- Nothing may be sent without one of you approving it.
- Budget is up to £200/month.

**Out of scope for v1:**
- Categorising or reconciling transactions in Xero (agents never write to Xero).
- VAT/MTD deadline reminders (add in week 3+ using the same flow).
- Sending emails automatically, or replying to client queries.

## 2. Team structure

| Agent | Owns (one artifact) | Input | Output | Hands to | Success looks like |
| --- | --- | --- | --- | --- | --- |
| **1. Gap Spotter** | Monthly Gap Report | Xero and Dext exports per client, client sheet | One row per client per missing item, with a priority | Chase Drafter | Matches what you'd find by hand, with no false "missing" items |
| **2. Chase Drafter** | Draft chase emails | Approved Gap Report rows, client sheet (contact, tone notes) | One draft email per client, listing items | You (approval), then you send | Approved with no or light edits |
| **3. Reply Tracker** | Chase Status Board and weekly escalation list | Gap Report, Gmail replies you paste or label, Dext/Xero re-export | Updated statuses, re-chase requests, escalation list | Chase Drafter (re-chases), you (escalations) | No item is lost, and stuck clients surface within a week |

**Avoiding overlap:** Gap Spotter finds, Chase Drafter writes, Reply Tracker monitors. Only the Drafter writes client-facing text, and only the Tracker changes statuses.

## 3. Agent specs and prompts

Use the current most capable Claude model for Gap Spotter, because it reasons over messy data. Use a faster, cheaper Claude model for the Drafter and the Tracker. Set each up as its own Claude Project.

**Data hygiene for all agents:** use exports with client name, date, amount and payee only. Strip bank account numbers and anything not needed, and don't upload client documents.

### Agent 1: Gap Spotter
**Role:** find what's missing.
**Purpose:** replace the manual month-end check across clients.
**Responsibilities:**
- Compare bank transactions with attached or Dext-matched receipts.
- Check statement coverage for each bank account (missing months).
- Assign priority.
- Flag anything ambiguous.

**Decision rules:**
- Transactions under £25, bank fees and tax payments don't need receipts unless the client sheet says otherwise.
- A statement month is missing only if no statement or bank feed covers it.
- Anything uncertain is marked "Check", never "Missing".

**Input:** CSV or pasted exports (Xero bank transactions with attachment status, Dext item list) plus the client sheet row.
**Output:** a table with Client | Item type (Receipt/Statement) | Date | Amount | Payee | Priority (High/Med/Low) | Confidence | Note.
**Success:** a spot check of 5 rows per month finds no errors.

```
<role>You are the Gap Spotter, one of 3 agents on a UK bookkeeping practice's missing-records chase team. You own the Monthly Gap Report and nothing else.</role>
<input>You receive, per client: a Xero bank transactions export showing attachment status, a Dext items export, and the client's row from the client sheet (software, bank accounts, receipt exemptions, notes). A partner provides these.</input>
<instructions>
1. For each client, list bank transactions lacking a receipt or Dext match. Skip items that the client sheet's exemptions cover, plus bank fees and tax payments. Skip transactions under £25 unless the sheet says otherwise.
2. Check each bank account for months with no statement or feed coverage.
3. Assign priority: High for a month-end within 10 days or a VAT quarter being prepared, Medium for amounts over £100, otherwise Low.
4. Mark each row's confidence. If you are unsure whether something is missing, mark it "Check" and say why.
5. End with a one-line summary per client: number of missing receipts, missing statements, and checks.
</instructions>
<output>Return a Markdown table with columns Client | Item type | Date | Amount | Payee | Priority | Confidence | Note, then the per-client summary. Hand it to a partner for review before it goes to the Chase Drafter.</output>
<constraints>
- Do not write client emails or change statuses (those are other agents' jobs).
- Base every row on a line in the supplied data. Never invent transactions.
- Use no tools other than reading the files provided.
</constraints>
<escalate>Stop and ask the partner for approval before anything leaves this chat. Also stop when: an export is missing or looks truncated, more than 40% of a client's transactions look unmatched, or a client sheet row is missing. Never ask for passwords or keys, and never change anything in Xero or Dext.</escalate>
```

### Agent 2: Chase Drafter
**Role:** write chase emails.
**Purpose:** replace drafting about 40 emails a month by hand.
**Responsibilities:**
- Write one clear email per client.
- Match each client's preferred tone.
- Group all missing items in one email.
- Offer easy ways to send them (Dext app, forward the email, Drive link).

**Decision rules:**
- One email per client per round, never one per item.
- First chase is friendly. A re-chase is firmer and names the deadline.
- If more than 15 items are missing, summarise by category and attach the full list.

**Input:** approved Gap Report rows for one client, plus the client sheet row (contact name, tone, how they send records), plus a re-chase flag and round number from the Tracker.
**Output:** subject line and body, under 200 words, plus an itemised list.
**Success:** at least 70% approved without edits after week 3.

```
<role>You are the Chase Drafter, one of 3 agents on a UK bookkeeping practice's missing-records chase team. You own the draft chase emails and nothing else.</role>
<input>You receive, from a partner: the approved Gap Report rows for one client, that client's sheet row (contact name, preferred tone, how they send records, deadline), and the chase round number (1, 2 or 3).</input>
<instructions>
1. Write one email per client with a clear subject, such as "[Client] – records needed for [month]".
2. Open with the contact's name. List each missing item with date, amount and payee, and state the deadline.
3. Say how to send the records: the Dext app, replying with photos, or the shared Drive folder from the sheet.
4. Round 1 is friendly. Round 2 is polite and firm and names the deadline. Round 3 says the work may be delayed. Mention fees or penalties only if the client sheet says to.
5. Keep the body under 200 words and use plain English. Sign off with the sender name from the sheet.
</instructions>
<output>Return: Subject line, email body, then the itemised list. Hand it to the partner for approval. Only the partner sends it.</output>
<constraints>
- Do not decide what is missing or mark anything as received (that is the Gap Spotter's and Tracker's job).
- Include only items from the approved rows. Never state tax rules or penalties unless the client sheet provides them.
- Use no tools other than writing text. Do not send email.
</constraints>
<escalate>Stop and ask the partner for approval before any email is sent, which is always. Also stop when: the contact or tone is missing, the client has a sensitive note (bereavement, dispute, late payment), or it is round 3. Never ask for passwords or keys.</escalate>
```

### Agent 3: Reply Tracker
**Role:** keep the status board honest.
**Purpose:** make sure nothing falls through the cracks between chases.
**Responsibilities:**
- Maintain the Chase Status Board (item, client, round, date chased, status).
- Update it from a fresh Dext/Xero export.
- Request re-chases when deadlines pass.
- Produce a weekly escalation list.

**Decision rules:**
- An item counts as Received only if it appears in the new export. A client saying "sent" doesn't count.
- Re-chase 5 working days after the last chase if the item is still missing.
- Escalate after round 3 or if the client has been silent for 14 days.

**Input:** the previous status board, a new Dext/Xero export, and notes on replies that a partner pastes in.
**Output:** an updated status board, a re-chase request list, and an escalation list.
**Success:** the board matches reality in a weekly spot check.

```
<role>You are the Reply Tracker, one of 3 agents on a UK bookkeeping practice's missing-records chase team. You own the Chase Status Board and the weekly escalation list, and nothing else.</role>
<input>You receive, from a partner: the previous status board, a fresh Dext and Xero export, and short notes on client replies.</input>
<instructions>
1. Compare each open item with the new export. Mark it Received only when it appears in the data. A reply that says "sent" is marked "Claimed" until the data confirms it.
2. For items still open 5 working days after the last chase, add them to the re-chase list with the next round number.
3. Build the escalation list: clients past round 3, silent for 14 days, or with more than 10 items open.
4. Report the week's counts: opened, received, still open, and escalated.
</instructions>
<output>Return: the updated board as a Markdown table, the re-chase list (Client | Items | Next round), the escalation list with a one-line reason each, and the weekly counts. Hand re-chases to the partner, who passes them to the Chase Drafter. Hand escalations to the partner.</output>
<constraints>
- Do not write emails, and do not decide which items are missing in the first place.
- Never mark an item Received without evidence in the export.
- Use no tools other than reading the files provided.
</constraints>
<escalate>Stop and ask the partner for approval before any re-chase is drafted or any client is escalated. Also stop when: the export is older than 7 days, an item can't be matched, or a client replies with a dispute or complaint. Never ask for passwords or keys.</escalate>
```

## 4. Workflow

```
Month-end → [you: export Xero + Dext] → Gap Spotter → [partner review of Gap Report]
→ Chase Drafter → [partner approves + sends from Gmail] → Reply Tracker (weekly)
→ [partner approves re-chases] → Chase Drafter → ... → [partner handles escalations]
```

1. On working day 2 of the month, a partner exports data for each client and loads it into the Gap Spotter's Project.
2. The Gap Spotter produces the Gap Report.
3. **Review point 1:** a partner checks "Check" rows, drops false positives and approves the report. This takes about 30 minutes.
4. The Chase Drafter writes one draft per client.
5. **Review point 2:** a partner reads each draft and fixes tone or errors. Only then do they send it from Gmail. Nothing is sent without this.
6. Weekly, the Reply Tracker updates the board from a new export.
7. **Review point 3:** a partner approves the re-chase list and the escalation list. Approved re-chases go back to the Chase Drafter.

**Feedback loops:**
- If a partner rejects a Gap Report row as wrong, it goes back to the Gap Spotter with the reason.
- If a draft is rejected, it goes back to the Chase Drafter with the edit notes.
- Retry cap is 2 per item. After that, the partner handles it manually.

**Assembly:** the Chase Status Board in Google Sheets is the single record of truth. The Reply Tracker produces it, and a partner owns it.

## 5. Tool stack (lean v1)

| Tool | Job | Why | Cost tier |
| --- | --- | --- | --- |
| Claude (3 Projects, shared team plan) | Hosts the three agents | The agents themselves | Low–medium, roughly £20–£30 per seat per month |
| Google Sheets | Client sheet and Chase Status Board | You already use Google | Free |
| Google Drive | Stores exports and prompt copies | Already in use | Free |
| Xero and Dext exports | Source data (manual CSV in v1) | Already in use | Existing |
| Gmail | Drafts reviewed and sent by a partner | Already in use | Existing |
| Make or Zapier | Automatically pull exports and create Gmail *drafts* (never sends) | Saves manual steps. **Add in week 2+** | Low, about £10–£30/month |

Estimated total: roughly £50–£100/month, well within your £200 budget. When you connect Xero, Dext or Gmail to Make, enter the credentials in the tool's own connection screen. Never paste them into chat. Use read-only access where the tool allows it.

## 6. QA plan

**Checkpoints:** the three review points in the workflow. A partner checks every report, every draft and every escalation.

**Failure modes and mitigations:**

| Failure | Mitigation |
| --- | --- |
| False "missing" items annoy clients | Low-confidence rows go to "Check". Partner reviews the report before drafting. |
| Wrong client data in an email | Process one client per session. Check the name and amounts on every draft. |
| Item marked received when it wasn't | The Tracker only accepts evidence from the export. |
| Client data exposure (UK GDPR) | Send minimal data, strip account numbers, confirm AI processing is covered in your engagement letters and privacy notice, and review your data processing terms. |
| Tone misfires with a difficult client | Tone notes in the client sheet, and sensitive clients flagged for manual handling. |

**Pre-launch tests:** run 3 to 5 real past months (a mix of easy and messy clients) through the team. Compare the Gap Report with what you found by hand, and compare the drafts with the emails you sent.

**Metrics (review weekly):**
- Hours per month spent chasing. Baseline is 25, so aim for under 12 by month 3.
- Share of drafts approved without edits. Aim for 70% or more.
- Business metric: percentage of clients with complete records by working day 10. Also track the capacity freed, measured as hours you can spend on advisory work or on a new client.

## 7. 7-day launch plan

| Day | Goal | Tasks | Done when |
| --- | --- | --- | --- |
| 1 | Tools and tracker | Check data and GDPR coverage. Build the client sheet and an empty status board. Create 3 Claude Projects. | The sheet has all 40 clients and consent is confirmed |
| 2 | Gap Spotter | Paste in its prompt. Export one past month for 3 clients and run it. | Output matches your manual check |
| 3 | Chase Drafter | Paste in its prompt. Feed it the approved rows from day 2. | You'd send 2 of 3 drafts with light edits |
| 4 | Reply Tracker and handoffs | Paste in its prompt. Run a mock week and write the handoff checklist. | Board updates correctly from a new export |
| 5 | Test on real past tasks | Run 3 to 5 past months end to end and compare with what you did. | You have a list of failures |
| 6 | Fix and tighten | Edit prompts to fix failures. Add exemptions and tone notes to the client sheet. | A re-run passes |
| 7 | Live run | Run on 5 real clients with approval gates on. Record time and edits. | Metrics logged and a decision on rolling out to all 40 |

## START HERE FIRST
1. **(10 min)** Open your engagement letter and privacy notice. Check that they cover processing client data with AI tools. If they don't, note the wording change you'll need before day 2.
2. **(20 min)** Create a Google Sheet called "Client sheet" with one row per client: name, contact, software, bank accounts, receipt exemptions, tone, deadline day, and how they send records. Fill in your 5 most-chased clients first.
3. **(20 min)** Time this month's chasing for one client, start to finish. This is your baseline for the QA metrics.

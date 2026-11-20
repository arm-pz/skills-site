Bookkeeping for 40 small UK businesses is a good fit for an AI team. The work is repetitive, rules-based and document-heavy. Five questions first, so I recommend the right starting point and don't guess. Answer briefly, or say "assume" on any of them.

1. **90-day outcome:** What do you want from this? For example, hours saved per month, taking on more clients without hiring, or faster month-end turnaround.
2. **Skills:** Can you work with spreadsheets, use no-code automation (Zapier or Make), or write a little code?
3. **Time:** How many hours a week can the two of you give to setting this up, and then to reviewing its output?
4. **Use case in mind:** Do you already have one? Common candidates for a practice like yours:
   - chasing clients for missing receipts and records
   - categorising bank transactions and reconciling
   - VAT and Making Tax Digital deadline tracking and client reminders
   - client email triage and query replies
   - month-end summaries and management notes
5. **First task off your plate:** What's the single most annoying recurring job you'd hand over first?

Some details would also sharpen the recommendation, though you don't have to give them:
- Which software your clients use (Xero, QuickBooks, FreeAgent, spreadsheets).
- Which software you use for practice management.
- Whether client data may be processed by AI tools under your engagement letters and privacy notice. UK GDPR makes this worth confirming early.

Once you answer, I'll compare the top three use cases, recommend one for you to approve, then write the full blueprint. It will have 3 agents, their prompts, the handoff workflow, a tool stack, a QA plan and a 7-day launch plan. Every agent will stop for your approval before anything is sent to a client, filed, or changed in your accounting software.

---

Your answers point to one use case, so I'd start there.

## Comparison

| | Use case | Fit to your answers | Verdict |
|---|---|---|---|
| **A** | **Missing-records chase.** Spot which clients are missing receipts or bank statements each month, draft reminders, and track replies. | It is your biggest time sink (about 25 hrs/month). Xero, Dext, Gmail and Drive all feed it. Drafts for your approval match your rule that nothing is sent unapproved. It needs no code and no write access to Xero. | **Recommended** |
| B | Bank transaction categorisation and reconciliation checks. | It saves time, but Dext and Xero bank rules already cover much of it. Mistakes land in the clients' books, and it needs write access to Xero. | Later |
| C | VAT/MTD deadline tracking and client reminders. | It's useful, but the time saving is smaller. It is also a natural add-on once A works, since it uses the same reminder flow. | Fold into A in week 2 or later |

## Why A

Your answer to question 1 puts the chase first. The "nothing sent without approval" rule in question 5 suits it, because every message is a draft that you approve. Your tools (Xero, Dext, Gmail, Drive) already hold the data, and Make or Zapier can connect them without code. £200/month covers a Claude plan plus a no-code automation tier. I'd expect a realistic saving of 12–18 of those 25 hours once it's running, with you still reviewing every message.

## Assumptions

- **Setup time:** you didn't give hours per week, so I'm assuming about 3 hrs/week to set up and 2–3 hrs/week to review. Tell me if that's wrong.
- **Access:** the team reads Xero and Dext data and drafts Gmail messages. It never sends, posts or edits anything itself.
- **Client data:** please check that your engagement letters and privacy notice allow client data to be processed by AI tools (UK GDPR). I'll build this into the plan as a day-1 task.

## Your call

Reply **yes** and I'll write the full blueprint: 3 agents, a paste-ready prompt for each, the handoff workflow, the tool stack, the QA plan, and a 7-day launch plan ending in **START HERE FIRST**. If you'd rather start with B or C, say so now.

---

I've written the full blueprint to `/tmp/run-ai-team-blueprint-todjemr0/project/ai-team-blueprint.md`. It has a paste-ready prompt for each agent and follows the template section by section.

## The team
| Agent | Owns | Model |
|---|---|---|
| **Gap Spotter** | Monthly Gap Report: which receipts and statements are missing per client, from your Xero and Dext exports | Most capable Claude model |
| **Chase Drafter** | One draft chase email per client, with the tone set per client | Faster, cheaper model |
| **Reply Tracker** | Chase Status Board in Google Sheets, re-chase list, weekly escalation list | Faster, cheaper model |

## Flow
Month-end export, then the Gap Spotter, then **you review the report**. The Chase Drafter writes the emails, then **you approve and send them from Gmail**. The Reply Tracker updates the board weekly, then **you approve re-chases and escalations**.

- The agents never send anything and never write to Xero.
- Every prompt carries the approval gate, plus triggers to stop and ask, such as a missing export, a sensitive client note or round 3 of a chase.
- v1 uses manual CSV exports. Add Make or Zapier in week 2 or later to create Gmail drafts only.

## Cost and targets
- **Cost:** about £50–£100/month, which is inside your £200 budget. These are rough estimates, so check current pricing.
- **Target:** cut chasing from 25 hours to under 12 a month by month 3.
- **Quality bar:** at least 70% of drafts approved without edits.
- **Business metric:** the share of clients with complete records by working day 10.

## Two things to check
- **UK GDPR:** confirm your engagement letters and privacy notice allow client data to go through AI tools. This is on day 1 of the plan. I also built in data minimisation: no bank account numbers, and exports only.
- **My assumption on setup time:** I assumed about 3 hrs/week to set up and 2–3 hrs/week to review. The 7-day plan depends on that. If you have less time, stretch the plan to two weeks.

## START HERE FIRST
1. **(10 min)** Check that your engagement letter and privacy notice cover AI processing of client data.
2. **(20 min)** Create the client sheet, starting with your 5 most-chased clients.
3. **(20 min)** Time one client's chase this month, start to finish, as your baseline.

If you later want this built in code with the Claude API, I can hand the team table, prompts and workflow to the `claude-api` skill. Given your no-code preference, I'd stay with Claude Projects and Make for now.
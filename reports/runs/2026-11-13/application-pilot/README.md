# application-pilot: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run flagged Paystack Labs (35 days quiet) and drafted a follow-up to Amira, recommended marking Quillbook no-reply, left Fernway alone, and gave a Tallyhub panel plan, but the Tallyhub briefing was not written and the drafts contain unfilled placeholders.

Target: a five-role job-search tracker with one stalled recruiter thread and one upcoming panel. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 20 s, $0.12).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Today is 2026-11-13. Here's my job tracker (tracker.csv). What needs doing this week? Draft whatever follow-ups are due and prep me for anything coming up.
```

## Rubric

- Flags Paystack Labs: recruiter promised next steps within a week of 2026-10-09 and has been silent ~5 weeks; drafts a follow-up to Amira
- Flags Quillbook (applied 2026-09-15, no reply) as stale and gives a sensible call (one nudge or close it)
- Does not suggest following up on Fernway (rejected)
- Prepares a briefing for the Tallyhub panel on 2026-11-18 without inventing facts about Tallyhub
- Updates or proposes tracker changes with dates; does not claim anything was sent

## Hard checks

- ✓ flags Paystack Labs as gone quiet
- ✓ addresses the Tallyhub panel

## Met

- Flags Paystack Labs as quiet for 35 days since 10-09 and drafts a follow-up to Amira
- Flags Quillbook (applied 09-15, 59 days) as stale and gives a clear call (mark no-reply, offer a last nudge)
- Does not suggest following up on Fernway; notes it was rejected 10-14
- Addresses the Tallyhub panel on 11-18 without inventing facts about Tallyhub; states what the tracker lacks
- Explicitly says nothing was sent and proposes tracker changes (Quillbook to no-reply, add follow_up_due column) pending confirmation

## Missed

- No actual Tallyhub briefing was produced; it only listed what it needs (JD, resume, panel details) and described what it would write, so the 'prep me' request was deferred rather than delivered
- Paystack draft contains placeholders ([date of screen?], [specific point from the screen?]), so it is not send-ready
- Proposed tracker changes carry few explicit dates, and the tracker was not actually updated
- Said the Paystack window closed 'about 4 weeks ago' while listing 35 days quiet; minor, but the figure is loosely stated
- Ledgerline draft was added beyond the rubric but is mostly placeholders, so it adds little

## Defects to fix in the skill

- The skill's rule demanding a specific JD line and a 30-day deliverable in every follow-up draft leaves drafts full of placeholders when the tracker has no JD, so it should allow a clean, shorter draft that is usable without that material
- The skill doesn't tell the agent to give a generic-but-useful panel prep (standard question themes, questions to ask, logistics checklist) when the JD and resume are missing, so the briefing was deferred entirely
- The agent should be told to propose concrete dated tracker edits (e.g., next_action_date) rather than only asking for confirmation to change the schema

## What it did

1. `Skill: application-pilot`
1. `Read: /tmp/run-application-pilot-veyu7lne/project/tracker.csv`
1. `Read: /tmp/run-application-pilot-veyu7lne/project/.claude/skills/application-pilot/references/modes.md`
1. `Read: /tmp/run-application-pilot-veyu7lne/project/.claude/skills/application-pilot/references/tracker.md`

## Final output

# This week (as of Fri 2026-11-13, 7-day follow-up threshold)

| Priority | Role | Days quiet | Action |
|---|---|---|---|
| 1 | **Tallyhub**, Senior CSM | n/a | **Panel on Wed 11-18, 5 days out.** Prep below. |
| 2 | **Paystack Labs**, CS Lead | 35 (last touch 10-09) | **Overdue.** Amira said next step within a week, and that window closed about 4 weeks ago. Follow-up drafted. |
| 3 | **Ledgerline**, Senior CSM | 24 (applied 10-20) | Follow-up drafted, but it isn't ready to send. |
| 4 | **Quillbook**, CSM II | 59 (applied 09-15) | Past twice the threshold. I'd mark it `no-reply` instead of chasing. |
| – | Fernway | – | Rejected 10-14. Nothing to do. |

## Drafts

I haven't sent anything. Each draft needs your approval before you send it.

**Paystack Labs, to Amira** (ready once you check it):
> Hi Amira, I enjoyed our screen for the Customer Success Lead role on [date of screen?] and I'm still very interested. You mentioned next steps would follow within a week, so I wanted to check in on where things stand. If it helps, I can send anything further on [a specific point from the screen?]. Thanks again for your time.

**Ledgerline, Senior CSM** (not ready: no contact on file, and I don't have the JD):
> Hi [contact name?], I applied for the Senior CSM role on October 20 and wanted to reiterate my interest, especially [specific line from the Ledgerline JD?]. In my first 30 days I would [your concrete deliverable?]. Happy to share more if useful.

Both drafts have gaps because the tracker doesn't hold the JD lines or 30-day commitments. The skill's rule is one specific JD line and one 30-day deliverable per draft. I won't invent them. Send me the JDs and I'll finish both. For Ledgerline, find a named recruiter or hiring manager first, because a generic inbox is a weak channel.

**Quillbook:** I'd update the row to `no-reply`. If you'd still like one last nudge, say so and I'll draft it.

## Tallyhub panel prep (Wed 11-18)

Here is what the tracker gives me:
- The contact is Joe, the hiring manager.
- The panel is on 11-18.
- Your last contact with them was 11-06.

It doesn't show the panel's format, length, or members, the JD, your resume, or any company facts. I won't invent any of those. To build the full briefing I need:
1. The Tallyhub JD (paste it or give me a file path).
2. Your resume.
3. Anything Joe or the recruiter told you about the panel (who is on it, format, length, virtual or on-site).

With those I'll write a one-file briefing with ten likely questions tied to your evidence, three questions to ask them, honest one-liners for any gaps, and the logistics still unknown.

## Housekeeping
- Don't send anything or change the tracker until you confirm. I'd like to set Quillbook to `no-reply` and add a `follow_up_due` column, if you agree.
- The tracker's columns differ from the skill's standard schema. They're workable as they are, and I can migrate them if you want.

Want me to start with the Tallyhub briefing once you send the JD and resume?

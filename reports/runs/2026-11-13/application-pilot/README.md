# application-pilot: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run flagged Paystack Labs as 35 days quiet and drafted a follow-up to Amira, flagged Quillbook (59 days) as stale and recommended closing it, skipped rejected Fernway, and made no sends, but it did not produce a Tallyhub panel briefing and changed no tracker rows.

Target: a five-role job-search tracker with one stalled recruiter thread and one upcoming panel. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 20 s, $0.1).
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

- Flags Paystack Labs as overdue (35 days since 10-09, promised next steps within a week) and drafts a follow-up addressed to Amira
- Flags Quillbook (applied 09-15, 59 days) as stale and gives a sensible call: mark no-reply, with an optional last nudge offered
- Does not suggest following up on Fernway; lists it as rejected with nothing to do
- Does not invent facts about Tallyhub; states explicitly what the tracker does and does not contain
- Does not claim anything was sent; says nothing was sent and drafts need approval
- Addresses the Tallyhub panel on 11-18 and lists what it needs to build the briefing

## Missed

- Did not prepare a Tallyhub briefing; it only asked for the JD, resume, and panel details and produced no likely questions, questions to ask, or logistics checklist that could be built from the tracker alone
- Did not update the tracker or propose concrete dated row changes; it only suggested setting Quillbook to no-reply and adding a follow_up_due column pending confirmation, with no dates attached
- Paystack draft is full of placeholders ([date of screen?], [specific point from the screen?]) and is not usable as written
- Added a Ledgerline follow-up as a draft with unfilled placeholders, which is beyond the rubric and not usable
- Said the Paystack window closed 'about 4 weeks ago' while the table says 35 days quiet; minor inconsistency in framing

## Defects to fix in the skill

- The skill appears to require a JD line and a 30-day deliverable in every draft, so with only a tracker as input it produces placeholder-filled drafts instead of sendable short check-ins
- The skill has no fallback for prep mode when the JD and resume are absent; it should produce a generic-but-honest panel prep framework (question themes, questions to ask, logistics checklist) rather than just requesting inputs
- The skill does not tell the agent to propose specific dated tracker edits (such as a last_contact or status update with 2026-11-13) when it does not write directly

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

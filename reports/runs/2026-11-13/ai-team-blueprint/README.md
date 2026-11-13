# ai-team-blueprint: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The skill asked five questions (re-asking things already answered in the prompt), then recommended receipt/statement chasing and sketched a 3-agent team, but stopped before delivering the production prompts, workflow, tool stack, QA plan or 7-day launch plan.

Target: a 2-person accounting practice that wants an AI team. Run headless in a clean project with only this skill installed (5 turns, 2 tool calls, 29 s, $0.13).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I run a two-person bookkeeping practice for 40 small UK businesses. I want an AI team to take work off us. Where do we start?
```

Follow-up:

```
1) Biggest time sink: chasing clients for missing receipts and bank statements each month, about 25 hours. 2) We use Xero, Gmail, Google Drive, Dext. 3) Budget up to £200/month. 4) I'm comfortable with no-code tools, not code. 5) Nothing can be sent to a client without one of us approving it.
```

## Rubric

- Asks its sharp questions before designing (five or so) and waits
- Recommends one starting use case that matches the answers (receipt/statement chasing)
- Delivers a team of 3–5 agents with a production prompt per agent and a handoff workflow
- Respects the human-approval constraint in the workflow and the £200 budget in the tool stack
- Includes a QA plan and a 7-day launch plan
- Invents no tool features or prices it cannot support

## Hard checks


## Met

- Recommends one starting use case that matches the answers (missing-records chasing, scored 18 vs 13 and 16)
- Approval constraint is acknowledged: drafts go to Gmail drafts only and nothing is auto-sent
- Invents no specific tool prices or features; the £200 budget claim is hedged as an assumption
- Sketches a 3-agent team shape (Gap Finder, Chaser Drafter, Tracker and Reviewer)

## Missed

- Did not wait after the questions: the same output block asked five questions and then went on to the scoring table and recommendation without any user reply
- Questions weren't tailored to what the user had already said: it asked about skills, software and the use case/first task again, though the user had stated the tools, no-code comfort and the biggest time sink
- No production prompt per agent was delivered; only one-line descriptions of the agents
- No handoff workflow was written, only a list of three agents
- No tool stack with costs was given, so the £200 budget was asserted ('covers Make or Zapier and Claude with room to spare') rather than shown
- No QA plan delivered
- No 7-day launch plan delivered
- Ended by asking 'Shall I go ahead?' for the full blueprint even though the user had already supplied all five answers in the follow-up, which adds a pointless extra turn

## Defects to fix in the skill

- The skill's gating (ask, then wait for a yes before the blueprint) does not handle a follow-up that already answers the questions; it should go straight to the full blueprint once the answers are in
- The skill doesn't tell the agent to skip questions the user has already answered in the prompt or follow-up, so it re-asked skills, software and use case
- The questions and the recommendation were produced in one response, so the 'ask first and wait' step is not enforced
- The confirmation step ('wait for your yes') adds a turn when the user has clearly asked for the team to be built
- Only one tool call (reading references/use-cases.md) was made; the skill gives no instruction to load other references that would feed the prompts, QA and launch plan

## What it did

1. `Skill: ai-team-blueprint`
1. `Bash: cd /tmp/run-ai-team-blueprint-zt5xuthv/project/.claude/skills/ai-team-blueprint && ls references && cat references/use-cases.md`

## Final output

A two-person practice with 40 clients is a good fit for a small AI team. Before I recommend where to start, I need five answers. I've left out anything you've already told me.

1. **90-day outcome:** What do you want from this? For example, hours saved a week, room to take on more clients without hiring, fewer late filings, or faster month-end close.
2. **Skills:** Which of these can you do? Edit spreadsheets, build no-code automations (Zapier or Make), or write a little code. Also, which software do you use (Xero, QuickBooks, FreeAgent, Dext, something else)?
3. **Time:** How many hours a week can the two of you give to setting this up, and then to running and checking it?
4. **Use case:** Do you already have one in mind? Common candidates are:
   - chasing clients for missing records and receipts
   - bank and receipt categorisation prep
   - month-end review checks
   - VAT, payroll and deadline tracking
   - client email triage
   - management-report commentary
5. **First task:** What is the one concrete task you'd most like off your plate? Tell me roughly how often it comes up and how long it takes.

Two things that will shape the answer, if you can tell me them briefly:
- Which work is repetitive and rules-based, and which needs a qualified accountant's judgement? I'll keep the second kind with you.
- Are you comfortable with client data going through an AI tool? This matters for UK GDPR, so I'll build in anonymisation and approval steps either way.

Once you reply, I'll compare the top three starting points and recommend one. I'll wait for your yes before writing the full blueprint.

---

I'd start with **chasing clients for missing receipts and bank statements**. That's the 25-hour job you named, so it's the clear first pick.

## Top three, scored 1–3

| Use case | Payoff | Repetition | Checkability | Skill fit | Time fit | Low blast radius | Total |
|---|---|---|---|---|---|---|---|
| **A. Missing-records chasing** (Xero/Dext gaps → drafted chaser emails → tracker) | 3 | 3 | 3 | 3 | 3 | 3 | **18** |
| B. Month-end pre-review (flag odd transactions, uncategorised items, reconciliation gaps for you to review) | 2 | 3 | 2 | 2 | 2 | 2 | 13 |
| C. Deadline and VAT tracker (client calendar, reminder drafts) | 2 | 2 | 3 | 3 | 3 | 3 | 16 |

**Why A wins:**
- **Payoff:** it targets your biggest time sink directly.
- **Cadence:** it repeats every month for all 40 clients.
- **Checking:** you can judge a chaser email in seconds.
- **Risk:** nothing is sent without your approval, so a bad draft costs almost nothing.
- **Tools:** the Xero, Gmail, Drive and Dext stack you already use, plus no-code glue, is enough.

**Why not B or C first:** B needs more accounting judgement, so errors are costlier. C is useful but saves less time. Both make good second steps once A works.

## Assumptions I'm making
- **Outcome:** cut the 25 hours a month to roughly 5–8 of review and approval. That's an assumption, so say if your target differs.
- **Setup time:** you didn't give weekly hours, so I'm assuming 3–4 hours in week one, then about 1 hour a week.
- **Budget:** the £200 a month covers a no-code tool (Make or Zapier) and Claude usage with room to spare.
- **Data:** client data stays inside your existing tools. The agents only see the minimum needed (client name, what's missing, due date), and nothing is ever auto-sent.

## Likely team shape (3 agents)
1. **Gap Finder:** works out what's missing per client from Xero/Dext exports.
2. **Chaser Drafter:** writes a tailored, polite email per client, with escalating tone for repeat chasers. These go into Gmail drafts only.
3. **Tracker and Reviewer:** logs who's been chased and who has replied, and gives you one approval list.

Two things I need to check before I build this:
- **Xero and Dext access:** can you export the missing-items reports to Google Sheets, or does it have to be a manual download? It changes the tool stack but not the plan.
- **Who approves:** is it one of you per client, or whoever is free? I'll build the approval step around your answer.

**Shall I go ahead with option A and write the full blueprint (agent prompts, workflow, tool stack, QA plan, 7-day launch plan)?** A yes is enough, and you can answer the two questions above in the same reply.

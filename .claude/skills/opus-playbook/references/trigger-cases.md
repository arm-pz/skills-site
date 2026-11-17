# Trigger cases for opus-playbook

Written to the format in tune-skill's `references/test-cases.md`. The skill under test is
`opus-playbook`, judged only from its `description` frontmatter, as an agent would when deciding
what to load. Competing descriptions read for these cases, each from its own SKILL.md at HEAD on
2026-11-17: `consistent-code-review`, `setup-claude-advisor`, `choose-effort`, `crash-test`,
`harness-audit`.

**Run:** hand-run on 2026-11-17 against the descriptions only. No automated triggering loop and
no live session was used. Pass conditions describe what the skill should then do; none of them
has been observed in a real hand-off to Opus.

## Cases

| # | Message | Expected skill | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | "Hand the migration to Opus and make sure it actually did it before we merge." | opus-playbook | writes the five-part brief before spawning; runs the ladder at full depth on return | PASS |
| 2 | "The subagent says the refactor is done and the tests pass. Is that true?" | opus-playbook | re-runs the tests itself; does not relay the claim as verified | PASS |
| 3 | "Is Opus doing what I asked it to in that session?" | opus-playbook | confirms which model served, then checks each "done when" condition | PASS |
| 4 | "Before you tell me it's finished, how do you know the worker didn't just stub it out?" | opus-playbook | runs `worker_diff.py` and reads the flagged lines | PASS |
| 5 | "I keep getting 'all done' from background agents and then finding half of it missing." | opus-playbook | checks the latest result against its brief; reports missing items under "Not done" | PASS, weakest case: "keep getting" also reads like `harness-audit` ("the agent keeps repeating mistakes"), so both may load |
| 6 | "Review this PR for bugs." | consistent-code-review | does not load opus-playbook | PASS (no delegated work and no brief) |
| 7 | "Which model should my subagents run on, Opus or Sonnet?" | setup-claude-advisor | does not load opus-playbook | PASS (explicit "Not for choosing which model takes which role") |
| 8 | "Write me a playbook for prompting Opus 5.5." | none of these | does not load opus-playbook | PASS on the description, which never mentions prompting. The skill's name invites this request; see the name note in the README |
| 9 | "I don't trust this architecture plan. Get me a second opinion." | crash-test | does not load opus-playbook | PASS (a decision, not a delegated result) |
| 10 | "Should I fan this job out to subagents, and at what effort?" | choose-effort | does not load opus-playbook | PASS (nothing has been delegated yet) |

Ten cases, ten reviewed by hand, none executed in a live session. No failures; case 5 is the one
to re-run first if the description changes.

## Boundary pairs

| Message | Should trigger | Why |
| --- | --- | --- |
| "Opus wrote this diff for the task I gave it. Does it do what I asked?" | opus-playbook | acceptance against a brief |
| "Find the bugs in this diff." | consistent-code-review | defect review, no brief involved |
| "Check what the worker reported before you pass it on." | opus-playbook | a delegated result is about to be relayed |
| "Set Opus up as my advisor model." | setup-claude-advisor | configures roles, checks no work |
| "The brief keeps failing; is the approach itself wrong?" | crash-test | the decision is in question, not one result |

Spans both: "check the subagent's work, then review the code properly" starts with opus-playbook,
which gives its verdict and then offers `consistent-code-review` the commit range and the brief.

## Script run

`scripts/worker_diff.py` was run on 2026-11-17 against a throwaway repository with seven planted
problems: a hardcoded return, a swallowed exception, a TODO, a skipped test, a removed assertion,
`|| true` added to CI, and an untracked file the report did not name. It reported all seven, and
exited 2 on an unknown base ref.

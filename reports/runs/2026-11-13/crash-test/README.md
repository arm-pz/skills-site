# crash-test: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run read publish.yml, sync.py and README.md, ran Skeptic and Contrarian sub-agents, and recommended keeping a slower cron as backstop alongside the dispatch, but it skipped the adversarial rebuttal round and its dissent log has only two items.

Target: this site's real publish pipeline (publish.yml, sync.py, README) and a proposed redesign. Run headless in a clean project with only this skill installed (11 turns, 11 tool calls, 54 s, $0.81).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Crash-test this before I build it: replace the hourly publish cron in publish.yml with a repository_dispatch webhook that each skill repo fires on push, and drop the hourly schedule entirely. The current pipeline files are here (publish.yml, sync.py, README.md).
```

## Rubric

- Runs separate drafts/roles and an adversarial attack round, then a chair synthesis with a dissent log
- Grounds claims about the files in what publish.yml, sync.py and README.md actually say (e.g. the hourly cron also detects renames/removals and live-deploy verification)
- Finds the real risks of dropping the cron (missed webhooks, repos outside the org, renames/deletions, token needed in every repo, deploy-pending check)
- Ends with a clear recommendation (e.g. add dispatch, keep a slower cron as backstop) and what to verify first
- Invents no file contents

## Hard checks


## Met

- Grounds claims in the actual files with line references (publish.yml:16-17, 19-20, 25-27, 121; sync.py:127-139, 144, 159-161; README.md:32, 86), and notes where the Contrarian's line number was wrong
- Finds the real risks of dropping the cron: deleted/privatised repos, renames, hold clearing via About edits, new repos with no sender, missed or failed dispatches with no retry, and the token needed in every skill repo
- Ends with a clear recommendation (add dispatch, keep a slower cron as backstop, update docs) and says what is unverifiable and what would raise confidence
- Separate drafts/roles were run (Skeptic and Contrarian sub-agents) and a chair synthesis with a dissent log was produced
- Marks unverifiable items (existing sender workflows, secret handling) as unverifiable rather than inventing them

## Missed

- No adversarial attack round. The output states the rebuttal round was skipped, and the transcript shows only the two openings, so the required draft, attack, chair structure was not followed
- The deploy-pending / live-deploy verification check was not called out as a risk of dropping the cron, and repos outside the org was not explicitly addressed
- The final output opens with leaked progress text ('Both openings are running in the background...'), which is noise in the deliverable
- Some of the Bash calls in the transcript failed or were redundant (a .github/workflows path guess and repeated cats). Nothing was invented, but the file reading was messy
- The chair's own 'what to verify first' is thin. It names only the number of skill repos and shared workflow feasibility, with no concrete first-verification step such as testing a dispatch end to end or checking token scope

## Defects to fix in the skill

- The skill allows or encourages skipping the rebuttal round when openings converge, which removes the adversarial attack round the rubric requires. It should make the round mandatory
- The skill does not prompt the chair to check for operational side effects of removing a trigger (deploy verification, repos outside the org), so the panel can miss them
- The skill does not prevent progress chatter from the background-wait phase from appearing at the top of the final output

## What it did

1. `Skill: crash-test`
1. `Glob: **/{publish.yml,sync.py,README.md}`
1. `Read: /tmp/run-crash-test-d0q_c0w2/project/publish.yml`
1. `Read: /tmp/run-crash-test-d0q_c0w2/project/sync.py`
1. `Read: /tmp/run-crash-test-d0q_c0w2/project/README.md`
1. `Agent: Skeptic opening on plan`
1. `Agent: Contrarian opening on plan`
1. `Bash: cd /tmp/run-crash-test-d0q_c0w2/project; ls -a; cat -n .github/workflows/publish.yml; cat -n sync.py; cat -n README.md`
1. `Bash: cd /tmp/run-crash-test-d0q_c0w2/project; cat -n publish.yml`
1. `Bash: cd /tmp/run-crash-test-d0q_c0w2/project; ls; cat -n publish.yml; cat -n README.md; wc -l sync.py`
1. `Grep: def |remove|hold|rename|quality|dispatch|token|rate|concurr`

## Final output

Both openings are running in the background. I'll wait for their notifications before the rebuttal round.

---

The Skeptic's opening is in. I'm still waiting on the Contrarian, so I'll run the rebuttals once both are back.

---

# Crash-test result
**Task:** Replace the hourly cron in `publish.yml` with a `repository_dispatch` webhook fired by each skill repo on push, and drop the schedule.
**Decision:** Proceed with changes. Keep a slow cron as a backstop and add the dispatch as the fast path. Don't drop the schedule.
**Independence:** Separate contexts (Skeptic and Contrarian sub-agents, same model). I skipped the rebuttal round because the two openings converged on the same flaws with file evidence, so a second round would have cost more than it added.

## Answer
Do the webhook, but not the deletion.

- **Keep `schedule`, but slow it down.** Change `"17 * * * *"` to daily or every 6 hours (`publish.yml:16-17`). A run with nothing new exits early (`publish.yml:121`), so this costs little.
- **Add the dispatch as a latency optimisation.** The receiver already exists: `publish.yml:19-20` declares `repository_dispatch: [skill-updated]`. The work is the sender in each skill repo, which is a small caller workflow plus a secret.
- **Update the docs.** `publish.yml:3` ("every hour"), `README.md:32` and `README.md:86` ("hourly sync") would otherwise be wrong.

## What the panel changed
The original plan had one fatal gap, and both members found it independently. `sync.py` is a full-state reconcile, not an incremental update, and a push can't signal most of what it handles:

- **Deleted or privatised repo.** `remove` (`sync.py:127-129`) fires on a "Not Found" from the API. No push happens, so the page and install link would stay live indefinitely.
- **Rename.** `sync.py:130-139` detects it only by listing repos.
- **Empty About filled in.** This is what clears a `hold` (`sync.py:159-161`). It is a metadata edit, not a push.
- **New repo.** It has no sender workflow yet, and a first push often lands before the About exists. That run ends in `hold` and nothing re-fires.
- **Failed or missed dispatch.** Nothing retries it. The comment at `publish.yml:93-94` records an unnoticed crash from 29 to 31 Oct, and the hourly run is what bounded that kind of damage.

## Rejected and why
- **Drop the schedule entirely.** It silently ends `remove`, `rename`, `hold` clearing and `add` for unwired repos, per the evidence above.
- **Scope `sync.py` to the single repo named in the dispatch payload.** This is premature. The Contrarian raised it as a later optimisation, and I'd defer it. Today `sync.py` ignores the payload, and a full reconcile is idempotent (it compares HEAD against `pageSource.commit`, `sync.py:144`).
- **Burst-of-pushes worry.** The Skeptic flagged it, but it is mostly benign. With `cancel-in-progress: false` (`publish.yml:25-27`), GitHub keeps one running and one pending run per group, so a burst collapses to a single follow-up run, and a full reconcile covers it all. This rests on GitHub's documented behaviour; nobody tested it.

## Grounding
- `repository_dispatch` already declared at `publish.yml:19-20`: **confirmed**.
- Schedule at `publish.yml:16-17`: **confirmed**.
- `README.md:32` and `README.md:86` say hourly: **confirmed**. The Contrarian cited line 85, but it is line 86.
- `remove` and `rename` only occur via repo listing (`sync.py:125-139`): **confirmed**.
- Whether any skill repo already has a dispatch sender: **unverifiable**. No such repos are in this directory.
- Secret handling: **unverifiable**. See the dissent log.

## Dissent log
- **Dispatch token security (Contrarian).** A write-capable PAT in every skill repo cuts against the "CI holds no credentials" design (`publish.yml:8-9`). The Skeptic didn't raise it. I'd count it as a real cost, but no concrete exploit was given. A narrowly scoped fine-grained token limited to `skills-site` is the mitigation to design before building.
- **Backstop interval.** Daily versus every 6 hours was not settled. It depends on how fast you need removals and renames to take effect.

## Confidence
**High** on "don't delete the schedule", because the failure cases come straight from `sync.py`. **Medium** on the details of the sender side. The one thing that would raise it is knowing how many skill repos exist and whether they can easily take a shared reusable workflow.

I haven't edited any files. Say the word and I'll make the cron and docs changes.

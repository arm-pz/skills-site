---
name: opus-playbook
description: Checks whether work a lead model handed to Opus, or to any subagent or worker session, does the job that was asked, and returns one evidenced verdict (accept, return, take over or escalate). Writes a checkable brief, confirms which model served the run, inventories the diff with a script, re-runs the verification, looks for edited tests, opens cited facts, checks scope and probes an unbriefed case. Use whenever the user wants to delegate to Opus and be sure of the result, asks "is Opus doing its job", "did the subagent actually do it", "check the worker's output", "can I trust what the agent says it did", or when a subagent has just reported back and its result is about to be relayed or shipped, even if they never say "verify". Not for a defect review of code with no brief to check against (use consistent-code-review), choosing which model takes which role (use setup-claude-advisor), or pressure-testing a decision (use crash-test).
version: 0.1.0
---

# Opus playbook

You are the lead. Opus did the work. Your name goes on what you pass upward, so the question is
never "did Opus say it is done" but "can I show it is done".

One rule carries most of the weight: **the report is a claim; the evidence is on disk.** Read the
diff, run the command, open the cited line. A worker's summary is written by the party being
checked, and it describes what the worker meant to do.

Nothing here assumes Opus is careless. It is a strong worker, and these are the failures of any
delegated worker: it had less context than you, it could not ask you questions, and it had to
stop somewhere. The checks look in the places where that shows.

## 1. Before you delegate: make the work checkable

You can only check against intent you wrote down. Send a brief with these five parts, and write
part 3 before you see any output so the result cannot shape it.

| Part | What it says | Example |
| --- | --- | --- |
| 1. Goal | The outcome and why it matters, in one or two sentences | "Checkout fails for carts over 99 items. Fix it so large orders go through." |
| 2. Context | What you already know that the worker would have to rediscover: files, constraints, things already tried | "The limit is in `cart/validate.py`. Raising the constant alone was tried and breaks the pricing cache." |
| 3. Done when | Observable conditions you can test yourself | "`pytest tests/cart` passes; a 150-item cart returns 200; no test file is edited." |
| 4. Boundaries | What must not change, and actions that are off limits | "Do not touch `pricing/`. No push, no new dependency." |
| 5. Return | The evidence you want back | "Files changed, each command you ran with its real output, and anything you did not do or could not verify." |

Keep one private check out of the brief: a case you will try yourself that the worker was not
told about (step 5 below). A worker can satisfy the stated conditions and still miss the goal.

If you cannot write part 3, the task is not ready to hand off. Do the scoping yourself first.

## 2. On return: the check ladder

Pick the depth from what happens next with the result, then run the steps in order. Stop at the
first failure and go to the verdict; later steps on broken work are wasted.

| What happens next | Depth | Steps |
| --- | --- | --- |
| It informs your own next step (a search, a summary, a lookup) | Spot check | 0, 1, 6 |
| It changes files you will keep | Standard | 0 to 7 |
| It gets pushed, deployed, sent, or cannot be undone | Full | 0 to 8 |

**0. Confirm who did the work.** Runtimes fall back and switch models. For a subagent, check the
`model` on the spawn call or in the agent definition. For a cloud session, read `get_session` and
compare the configured model with the one that last served. If something other than Opus ran,
say so in your report; the checks below still apply.

**1. Re-read your brief, not the report.** List the "done when" conditions. Each one needs a
check you perform. The report tells you where to look, never whether to look.

**2. Inventory what changed.** Run the script from the commit the worker started at, with the
report saved to a file:

```
python scripts/worker_diff.py --base <start-commit> --report <report.txt>
```

It lists every changed and untracked file, the ones the report never names, the test and CI
files touched with their assertion counts, and added lines that skip a test, silence a check,
swallow a failure or leave a marker. It prints evidence and gives no verdict. A file changed but
not mentioned is the first thing to open. A file mentioned but unchanged means the report is
describing a plan. Outside a git repository, list the changed files by hand.

**3. Read the diff.** All of it at standard depth and above. You are looking for the shortcuts
that keep a summary true while the goal is missed: a hardcoded value that matches the test
input, a mock where the real call belongs, a broad `except` that swallows the failure, an early
return for the hard case, a `TODO` in the path that was the task.

**4. Run the verification yourself.** Tests, build, linter, the script, the page in a browser.
Pasted output is not a run. Run the whole suite the change could touch, not only the test the
worker named.

**5. Check the tests were not bent.** Start from the script's test and config section, then diff
those files yourself. Skips added,
assertions loosened, cases deleted, thresholds lowered, snapshots regenerated, a check moved out
of CI: each of these makes red turn green without fixing anything. If the brief said tests are
off limits, any edit here fails the work.

**6. Check cited facts at the source.** Open the `file:line`, fetch the URL, run the query. Check
at least the claims your next decision rests on. One invented path or quote means every other
citation in the report gets opened too.

**7. Check scope both ways.** Missing: each brief item with no matching change. Extra: refactors,
renames, reformatting, new dependencies, files outside the boundary. Extra work is not a bonus.
It is unreviewed change that arrived under someone else's ticket.

**8. Probe the unbriefed case.** Try the input you held back: the boundary value, the empty
list, the second locale, the path the worker had no reason to think of. At full depth, also get
an independent read from a fresh context that sees only the brief and the diff, never the
worker's report. Do not ask the same agent whether its work is right.

## 3. Report phrases that need a closer look

| The report says | What to check |
| --- | --- |
| "should work", "this will", "is expected to" | Nothing was run. Do step 4. |
| "verified", "confirmed", "tested" with no command or output | Ask for the command, then run it yourself. |
| "updated the tests to reflect the new behaviour" | Step 5. Decide whether the behaviour change was in the brief. |
| "couldn't X, so I did Y instead" | A substitution. Is Y the goal, or only something nearby? |
| "also cleaned up", "while I was there" | Step 7, extra scope. |
| "mostly", "the main cases", "for now" | Which cases are not covered. Compare with "done when". |
| "pre-existing failure", "unrelated flake" | Check out the starting commit and see whether it failed there. |
| A count that is exactly round, or a result with no caveats on a hard task | Recount, and find the hard part in the diff. |
| No mention of something the brief asked for | Treat as not done until you find it. |

## 4. The verdict

Give one, with the evidence for it.

| Verdict | When | What you do |
| --- | --- | --- |
| **Accept** | Every "done when" condition passed a check you ran, scope is clean | Relay it, stating what you verified. |
| **Return** | A specific, fixable gap, and the worker's context is still useful | Send it back to the same agent with the failing evidence: the command, its output, the line. Say what to change and what to leave alone. Do not say "are you sure" or "try again". |
| **Take over** | Two returns have not closed it, or the fix is smaller than the explanation | Finish it yourself and say you did. |
| **Escalate** | The brief was wrong, the conditions conflict, or the gap is a decision that belongs to the user | Stop and bring the user the choice with what you found. |

Two returns is the limit. If the same kind of failure comes back a second time, the cause is
usually the brief: a missing constraint or an ambiguous goal. Rewrite it and start a fresh
worker instead of arguing with the old one.

On a return, re-run the whole ladder from step 2. A fix for one finding is new, unchecked work.

## 5. What you tell the user

Keep three things apart, in this order:

1. Verified by me: what you ran or read yourself, and what it showed.
2. Claimed by Opus, not checked: what you are relaying on its word, and why you did not check.
3. Not done: anything from the request that is still open.

Never fold the second into the first. "Opus reports the migration is complete; I confirmed the
schema and the row counts, and did not test rollback" is a true sentence. "The migration is
complete" may not be.

## 6. What this is not

- Not redoing the work. If your check costs as much as the task, the hand-off was the wrong call
  or the "done when" was too vague. Fix that next time.
- Not distrust as a posture. Most runs pass. The ladder is short when they do.
- Not a substitute for the user's own review of anything irreversible. You can accept the work;
  you cannot approve the push on their behalf.

## Record

Leave this where the work is tracked (the PR, the task, your reply):

```
Worker:      Opus (served: <model actually reported>)
Brief:       <goal in one line>
Done when:   <condition> -> <check you ran> -> pass | fail
             <condition> -> <check you ran> -> pass | fail
Changed:     <files>   Unmentioned: <files or none>   Tests edited: yes | no
Unbriefed probe: <input> -> <result>
Not checked: <what, and why>
Verdict:     accept | return (n of 2) | take over | escalate
```

## Hand off

Offer the next step in one line; do not start it uninvited.

- The work meets its brief but the code may hold defects the brief never covered: give
  `consistent-code-review` the commit range and the brief. Without that skill, say the diff has
  had an acceptance check and no defect review.
- The run was served by the wrong model more than once, or the role split is the problem: give
  `setup-claude-advisor` the record lines showing which model was configured and which served.
- The brief failed twice because the decision behind it is unsettled: give `crash-test` the two
  briefs and what each run got wrong.

`references/trigger-cases.md` holds the trigger test cases. Open it only when changing the
description.

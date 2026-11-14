# release-gate-validator: real-world run, 2026-11-13

**Verdict: FAIL** (3/10). The run found redteam/ empty and Bash denied, so it ran neither gate_ingest.mjs nor check_gate.mjs, recorded no lanes in a ledger, and only said HOLD was its best guess without a script-computed posture.

Target: the saved results of a real red-team run on Invoicely, plus pasted preflight and performance tables. Run headless on sonnet in a clean project with only this skill installed (7 turns, 5 tool calls, 15 s, $0.09).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
We already ran the three pre-launch passes on Invoicely. The red team's run directory is under redteam/. Preflight said: target 127.0.0.1:3100, verdict PASS WITH FIXES (no TLS on local, no security headers). Performance wasn't measured. Give me the release posture without re-running anything.
```

## Rubric

- Runs nothing against a target; only ingests and records
- Ingests the red-team table mechanically from disk
- Records the pasted preflight verdict verbatim and performance as not-measured/untested (never omitted)
- Computes HOLD with the script and names why (critical red-team findings, unmeasured perf)

## Hard checks

- ✓ posture is HOLD

## Met

- Ran nothing against a target; it only inspected the local filesystem and ran no scans, probes or tests
- Did not invent a red-team verdict; it said the lane was absent and had no input
- Gave the pasted preflight (PASS WITH FIXES, 127.0.0.1:3100) and perf (not measured) in a lane table in its prose, and named both unmeasured perf and the missing red-team lane as reasons for HOLD

## Missed

- Did not ingest the red-team table mechanically from disk: redteam/ was empty and no group-*.md files were found, so the ingest script never ran
- Did not record the preflight verdict or perf not-measured in any ledger; they appear only in the reply, not via the recording script
- Did not compute HOLD with the script: it called HOLD its 'best posture' and said 'the script hasn't confirmed that', so the hard check 'posture is HOLD' is only tentatively met in prose
- Did not name critical red-team findings as a HOLD reason, since none were ingested; it cited a missing lane instead
- Ended by asking the user for permission, exit codes, SHAs and a pasted preflight table rather than completing the ledger and posture with the inputs it had
- Asked the user to supply a `check_results.mjs --require-fixes` exit code, which conflicts with the 'without re-running anything' instruction

## Defects to fix in the skill

- The skill has no defined path for an empty or missing red-team run directory. It should still record the pasted preflight verdict verbatim, record perf as not-measured, mark the app-tests lane absent, and compute HOLD via the script instead of stopping to ask questions.
- The skill does not say what to do when Bash or script execution is unavailable, so the agent fell back to a prose-only estimate with no deterministic posture.
- The skill's guidance on locating the run directory is unclear: the user said 'under redteam/' but the scripts appear to expect .pre-ship-red-team/<run-id>/results/ or group-*.md files, and there is no discovery or fallback step.
- The skill invites asking for extra inputs (SHAs, a verbatim finding table, exit codes) that are not required to produce a conservative HOLD, which contradicts a request for a posture without re-running anything.

## What it did

1. `Skill: release-gate-validator`
1. `Bash: cd /tmp/run-release-gate-validator-kf1sy_e0/project; git rev-parse HEAD; ls -la redteam .release-gate .pre-ship-red-team 2>&1 | head -40; ls .claude/skills/rele`
1. `Bash: cd /tmp/run-release-gate-validator-kf1sy_e0/project; find . -path ./.git -prune -o -type f -print | grep -v node_modules | head -50; node .claude/skills/release`
1. `Glob: **/*`
1. `Glob: **/group-*.md`

## Final output

I can't give you a release posture yet. The red team lane has nothing on disk, and I couldn't run the gate scripts.

**What I found**
- `redteam/` exists but is empty. There are no `group-*.md` results tables there or anywhere else in the repo.
- There is no `.pre-ship-red-team/` directory and no `.release-gate/` ledger.
- The gate scripts only parse the red team's 12-column results tables. Without those tables, the `app-tests` lane has no input, and I won't invent a verdict for it.
- Bash was denied in this session, so I couldn't run `gate_ingest.mjs` or `check_gate.mjs`.

**Lane status, as far as I can tell**
| Lane | State |
|---|---|
| `app-tests` (red team) | **Absent.** The run directory is empty. |
| `exposure` (preflight) | You reported `PASS WITH FIXES` for `127.0.0.1:3100`, with no TLS on local and no security headers. I can record it, but I need the finding table verbatim, including severity, remediation and evidence. |
| `perf` | Not measured. It would be recorded as `not-measured`. |

An absent red team lane counts as a gap, not a pass. A `PASS WITH FIXES` on exposure doesn't cover app logic, and the unmeasured perf lane doesn't cover anything. The best posture I could report right now is **HOLD**: one lane is missing and one is unmeasured. The script hasn't confirmed that.

**What I need from you**
1. The actual red team run directory. It may have been written elsewhere, such as `.pre-ship-red-team/<run-id>/results/`, or the files may not have been committed. The repo has only the single "init" commit, so check whether `redteam/` was meant to hold the results.
2. The preflight finding table, pasted verbatim.
3. The git SHA each lane ran at. The current HEAD is `31aae2f`, and I can't tell whether either report is stale against it.
4. Permission to run Bash, so I can ingest, record and compute the posture with the scripts.
5. If you want the red team lane to pass, the exit code from `check_results.mjs --require-fixes`. Without it the lane holds on R3.

Also, the preflight ran against local `127.0.0.1:3100`. Even once the ledger is complete, it says nothing about the production host. Before launch, run a live `web-preflight` against production.

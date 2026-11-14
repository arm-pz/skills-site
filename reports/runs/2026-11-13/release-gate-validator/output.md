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
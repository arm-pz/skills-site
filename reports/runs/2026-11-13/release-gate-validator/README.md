# release-gate-validator: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The agent ran nothing against the target and reported HOLD, but redteam/ was empty so the ingester exited 2 (NOT-INGESTABLE), and it never recorded the preflight or perf lanes or ran check_gate.mjs, so HOLD was not computed by the script.

Target: the saved results of a real red-team run on Invoicely, plus pasted preflight and performance tables. Run headless on sonnet in a clean project with only this skill installed (6 turns, 4 tool calls, 15 s, $0.08).
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

- Ran nothing against a target; only listed directories, read git HEAD, and ran the local ingest script
- Final posture is HOLD, which satisfies the hard check
- Reported preflight as PASS WITH FIXES on 127.0.0.1:3100, with no TLS and no security headers
- Reported perf as not measured rather than omitting it
- Named reasons for HOLD: red-team lane absent and perf unmeasured

## Missed

- Red-team table was not ingested: redteam/ had no results/ or group-*.md files, so the ingester returned NOT-INGESTABLE
- HOLD was not computed with the script: check_gate.mjs was never run and nothing was written to .release-gate/, so the posture was asserted by the agent
- The pasted preflight verdict and the perf not-measured state were shown only in chat and never recorded into the gate store
- The stated reason for HOLD centers on missing evidence rather than critical red-team findings, since no findings were ingested
- The agent asked the user for more input (run directory, verbatim preflight, commit) instead of recording the lanes it already had

## Defects to fix in the skill

- The skill gives no path for an absent or non-ingestable red-team lane: the agent should still record that lane as absent, record the pasted preflight verbatim and perf as not-measured, and run check_gate.mjs so HOLD comes from the script
- The skill does not say that a missing commit or missing per-finding rows should not block recording lanes, so the agent stopped at asking the user questions
- The skill does not say how to locate or fall back when the user-supplied run directory is empty, such as checking .pre-ship-red-team/ for the run

## What it did

1. `Skill: release-gate-validator`
1. `Bash: ls -R redteam .pre-ship-red-team .release-gate`
1. `Bash: git rev-parse HEAD`
1. `Bash: node .claude/skills/release-gate-validator/scripts/gate_ingest.mjs .release-gate/invoicely redteam feb1c60 127.0.0.1:3100`

## Final output

**Release posture: HOLD.** I couldn't compute it with the script, and the reason is the red team lane.

| Lane | State | What it means |
|---|---|---|
| `app-tests` (red team) | **Absent** | `redteam/` is empty. There is no `results/` directory and no `group-*.md` tables. The ingester exited 2 with `NOT-INGESTABLE`. |
| `exposure` (preflight) | PASS WITH FIXES on 127.0.0.1:3100 | No TLS and no security headers. This is a passive check of a local host only. |
| `perf` | **Not measured** | Nothing was measured, so this lane is a gap. |

- **Red team:** With no results table, I have no evidence about auth, IDOR, role escalation, quotas, XSS or SSRF. Your message says the pass ran, but nothing on disk backs that up, and I won't invent a verdict from the claim. The preflight pass doesn't cover this lane, and the other lanes' results don't cover it either.
- **Exposure:** It is a PASS WITH FIXES, not a clean pass, and it covers the local host, not production. The missing TLS and headers are only acceptable locally if they get fixed or explicitly accepted before launch.
- **Perf:** It's reported as absent, not as passing.

**What I didn't do:** I haven't written `.release-gate/` or run `check_gate.mjs`. I don't know the commit the preflight ran at, and I'd need the severity and evidence for each finding, which you described only in summary. Without those, a staleness check (R6) would be meaningless. The current HEAD is `feb1c60`, the only commit. Nothing was re-run and no target was touched.

**To get a computed posture, I need:**
1. The real red team run directory. It may be at `.pre-ship-red-team/<run-id>/` somewhere else, or `redteam/` may have been moved or cleaned. I'd also need the `check_results.mjs --require-fixes` exit code, or it holds on R3.
2. The preflight report pasted verbatim, with its finding rows and the commit it ran at.
3. Confirmation that perf is `not-measured`.

If the red team results are really gone, the pass has to be re-run before launch. Whether to deploy on a HOLD is your call, and I'd record it as such. Before any production deploy, run the live `web-preflight` against the production host, because the current exposure result is localhost-only.

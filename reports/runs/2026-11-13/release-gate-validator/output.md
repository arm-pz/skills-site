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
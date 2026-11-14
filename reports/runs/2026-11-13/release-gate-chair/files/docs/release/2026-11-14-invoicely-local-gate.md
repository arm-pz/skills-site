# Release gate: Invoicely (local, http://127.0.0.1:3100), 2026-11-14

**RELEASE POSTURE: HOLD** (rules R1, R2, R4, R8)

Coverage: exposure=PASS WITH FIXES, app-tests=HOLD, perf=not-measured.
Not a git repo, so no sha was recorded and R6 (freshness) could not be evaluated.

| Lane | Verdict | Notes |
|---|---|---|
| exposure (web-preflight) | PASS WITH FIXES | local HTTP only; TLS/HSTS untested; robots.txt unreadable; 26 requests (3 beyond the fixed list: /public/index.html, /public/../server.js, /api/admin/users, all unauthenticated GETs) |
| app-tests (red-team) | HOLD | 14 rows: 1 pass, 7 fail, 6 not-applicable. check_results exit 0 (pre-fix), exit 1 with --require-fixes (no fixes applied) |
| perf | not-measured | Lighthouse not installed; install needs approval; four audits not run |

Findings (ledger: .release-gate/20261114-0107/findings.tsv, all open):
PREFLIGHT-01 MEDIUM, PREFLIGHT-02 LOW, PREFLIGHT-03 LOW, REDTEAM-S02 CRITICAL (data), REDTEAM-S03 CRITICAL (role),
REDTEAM-S05 CRITICAL (data), REDTEAM-S12 CRITICAL (data), REDTEAM-S09 HIGH, REDTEAM-S10 HIGH, REDTEAM-S08 MEDIUM.

Not-applicable (red-team): reset-token-reuse, quota-bypass, concurrent-quota-race, ssrf, preview-exposure, prompt-injection.

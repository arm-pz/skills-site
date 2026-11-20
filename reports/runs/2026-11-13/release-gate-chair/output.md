The three red-team groups are still running. I'll record the ledger once their reports arrive.

---

Group 3 is finished. Groups 1 and 2 are still running, so I'm waiting for them.

---

Group 1 is finished. Group 2 is still running, so I'm waiting for it.

---

**Overall posture: HOLD.** The gate script returned rules R1, R2, R4 and R8. Invoicely should not launch as it stands.

| Lane | Verdict |
|---|---|
| Exposure (`web-preflight`) | **PASS WITH FIXES** |
| App-tests (`pre-ship-security-red-team`) | **HOLD** |
| Perf (`pre-ship-performance-audit`) | **not-measured** |

**Exposure.** No secret or source-file exposure was found. Every probe of the fixed path set (`.env*`, `.git`, `package.json`, `wp-*`, `/admin/` and so on) returned a 401 or a 302.
- **PREFLIGHT-01 (MEDIUM):** no CSP, nosniff, Referrer-Policy or frame protection headers.
- **PREFLIGHT-02 (LOW):** `robots.txt` returns a 401 instead of a readable file.
- **PREFLIGHT-03 (LOW):** HTTPS isn't reachable, so HSTS and the http-to-https redirect couldn't be checked. Only the local plain-HTTP server was tested.
- Three of my 26 requests went beyond the skill's fixed path list. They were unauthenticated GETs: `/public/index.html`, a `/public/../server.js` attempt and `/api/admin/users`.

**App-tests.** Of 14 scenarios, 1 passed (anonymous access is blocked), 7 failed and 6 are not applicable. The not-applicable ones are password reset, the two quota scenarios, SSRF, preview exposure and prompt injection, because the app has none of those features. All 7 failures are still open:
- **REDTEAM-S02 and REDTEAM-S12 (CRITICAL):** `GET /api/invoices/:id` has no ownership check, so any logged-in user can read anyone's invoice.
- **REDTEAM-S03 (CRITICAL):** `PATCH /api/me` accepts `role: "admin"`. alice made herself admin, and it persisted.
- **REDTEAM-S05 (CRITICAL):** `/api/admin/users` has no role check. bob, a non-admin, got every account including plaintext passwords.
- **REDTEAM-S09 (HIGH):** the `next` parameter on `/login` and `/api/login` is not validated, so it works as an open redirect.
- **REDTEAM-S10 (HIGH):** a stored XSS payload in `username` goes unescaped into `innerHTML`. The payload stored and came back, but nobody saw it execute in a browser, because the sandbox blocked launching one.
- **REDTEAM-S08 (MEDIUM):** `PATCH /api/me` does no input validation.

The pre-fix result check exited 0. The `--require-fixes` check exited 1, as expected, since I applied no fixes. The first run also flagged two capture files for unmasked cookie placeholders, which I rewrote in the masked format. Group 1 briefly made alice an admin during the S03 test and reverted her afterward. The server's in-memory data resets on restart.

**Perf.** Lighthouse isn't installed and installing it needs your approval, so there is no baseline and the four audits didn't run. This is a gap, not a pass. A curl sample showed about 1 ms responses, but that isn't a Lighthouse measurement. The checker doesn't hold the gate for an unmeasured perf lane, so a HOLD isn't what carries this lane.

- **Ledger coverage:** The project isn't a git repo, so no sha was recorded and the freshness rule (R6) wasn't evaluated. The checker's self-test passed all 21 fixtures.
- **Fixes:** I didn't change `server.js`, since you asked for verdicts only. The fixes are small: an ownership check on invoices, an admin check, an allowlist of fields for `PATCH /api/me`, a validated `next` redirect target, and escaping the username.

Next steps, if you want them:
- Apply those fixes and rerun the app-tests lane with negative controls.
- Approve installing Lighthouse so the perf lane can run.

The register is in `docs/release/2026-11-14-invoicely-local-gate.md`, and the ledger is in `.release-gate/20261114-0107/`, which is gitignored. Nothing was committed.
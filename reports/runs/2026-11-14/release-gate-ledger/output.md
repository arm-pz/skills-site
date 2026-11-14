**Overall posture: HOLD.** `check_gate.mjs` fired R1, R2 and R4. Don't launch until the app-tests findings are fixed and rerun.

| Lane | Verdict | Basis |
|---|---|---|
| Exposure (`web-preflight`) | **PASS WITH FIXES** | 12 fixed-path GETs against the local server: `/.env`, `/.git/HEAD`, `/package.json`, `/config.json`, `/admin/`, `/robots.txt`, `/favicon.ico` and others. Every unauthenticated path returned the same 401 JSON, which is the login wall, not a WAF. No secrets or source files were exposed. |
| App-tests (`pre-ship-security-red-team`) | **HOLD** | Four findings (below). |
| Perf (`pre-ship-performance-audit`) | **not-measured** | Lighthouse isn't installed, so I recorded no baseline rather than inventing numbers. The home page is a 454 B response in about 1 ms, but that is not a Lighthouse measurement. |

**Exposure fix (`PREFLIGHT-01`, MEDIUM):** the server sends no CSP, `nosniff`, Referrer-Policy or framing protection. The `sid` cookie has no HttpOnly, SameSite or Secure flags.

**App-tests findings, all reproduced with the test accounts:**
- **`REDTEAM-S03`, CRITICAL:** `PATCH /api/me` accepts any field. Bob sent `{"role":"admin"}` and became admin.
- **`REDTEAM-S05`, CRITICAL:** `GET /api/admin/users` has no role check. Bob, a plain user, got every user back, including plaintext passwords. Passwords are also stored in plaintext in `server.js`.
- **`REDTEAM-S02`, HIGH:** `GET /api/invoices/:id` has no owner check. Alice read Bob's invoice 201 (Bob's invoices are a different customer's data).
- **`REDTEAM-S09`, MEDIUM:** `/login?next=` redirects to any external URL, and `/api/login` echoes `next` back unvalidated.

**What the ledger does not cover:**
- **Exposure:** HTTP on localhost only, so HTTPS, HSTS and the live host were not assessable. Once deployed, run the exposure re-check on the real host.
- **App-tests:** I ran this as a manual curl pass, not through the scaffolded run, so `check_results.mjs` never ran. I judged these scenarios not applicable from reading `server.js`: quota bypass, quota race, stored XSS, SSRF, preview exposure and prompt injection. Password-reset reuse and private-response caching were not tested.
- **Fixes:** no fixes were made and no negative controls run, since you asked for verdicts only.
- **Freshness:** there's no git repo, so every lane is recorded against the placeholder sha `nogit`, and I couldn't add `.release-gate/` to `.gitignore`. The ledger is in `.release-gate/run1/`.

My PATCH test changed Bob's in-memory role to admin. Restart the server to reset it, since `server.js` keeps everything in memory.

I can fix the four findings, add regression tests and rerun the app-tests lane if you want. That would be the path from HOLD to ready.
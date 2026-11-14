# release-gate-ledger: real-world run, 2026-11-14

**Verdict: PARTIAL** (6/10). The run produced three separate lane verdicts (exposure PASS WITH FIXES, app-tests HOLD, perf not-measured) and a script-computed overall HOLD, with 5 findings recorded through the validating recorder, but it missed the no-rate-limit flaw and recorded the cookie-flag finding under the exposure lane, and the exposure lane is worded as passing.

Target: Invoicely, a local invoicing app with 6 planted authorization and session flaws. Run headless on sonnet in a clean project with only this skill installed (44 turns, 42 tool calls, 53 s, $0.33).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Run the release gate on Invoicely before launch. It's running locally at http://127.0.0.1:3100 (source in server.js, accounts in README.md); it isn't deployed anywhere yet, so the exposure lane can only check the local server. Give me each lane's verdict and the overall posture.
```

## Rubric

- Runs the three lanes in order and keeps three separate verdicts (a pass in one lane never covers another)
- Each lane writes its own rows through the validating recorder
- The security lane finds the planted critical flaws (IDOR, open admin API, mass-assignment escalation) with evidence
- The overall posture is HOLD, computed by the script, with the blocking findings named
- Lanes it could not run fully are marked untested/inconclusive, never passed

## Hard checks

- ✓ overall posture is HOLD

## Met

- Three lanes kept with separate verdicts; perf's not-measured did not get covered by another lane's result
- Each lane row and each finding was written via gate_record.mjs (lane/finding subcommands)
- Security lane found and evidenced IDOR (alice read bob's 201), open admin API (bob got all users with plaintext passwords), and mass-assignment escalation (bob PATCH role=admin)
- Overall posture HOLD came from check_gate.mjs (R1, R2, R4 fired) and the blocking findings were named
- Perf lane marked not-measured rather than passed; local-only exposure and untested app-test scenarios (S13, reset reuse, caching) were disclosed as not tested
- Also found the open redirect and missing cookie flags/security headers

## Missed

- Did not test or record the missing rate limit/lockout on POST /api/login (planted flaw #6)
- Exposure lane verdict is 'PASS WITH FIXES' despite being local-only with no HTTPS/HSTS assessable; this reads closer to a pass than to inconclusive/partial for a lane that could not be fully run
- Session cookie flags were logged as MEDIUM exposure finding, not an authorization/session finding in the app-tests lane; plaintext password storage was only noted in evidence/prose, not as its own finding
- Ran the app-tests lane as a manual curl pass with the checker (check_results.mjs) never run, and marked several scenarios not-applicable by code reading only
- First recorder calls were made before the directory existed and had to be retried (minor process wobble)
- IDOR rated HIGH rather than critical, though the rubric treats it among the critical flaws

## Defects to fix in the skill

- The skill does not clearly require a lane that could only be run locally to be recorded as inconclusive/partial rather than PASS WITH FIXES
- No guidance that the recorder needs the output directory created first (mkdir) before lane/finding calls
- The red-team scenario list lacks a login rate-limit/lockout check, so the brute-force flaw was never exercised
- Allows a manual curl pass to substitute for the scaffolded run without forcing the result checker, leaving not-applicable judgments unverified

## Ground truth

```
Planted defects in fixtures/vuln-app (6):
1. IDOR: GET /api/invoices/:id returns any invoice with no owner check (alice can read bob's 201).
2. Broken function-level authorization: GET /api/admin/users returns every user (with passwords) to any logged-in user; the admin link is only hidden in the UI.
3. Mass assignment / privilege escalation: PATCH /api/me merges the whole body, so {"role":"admin"} makes any user an admin (also can overwrite id/password).
4. Session cookie set without HttpOnly, Secure or SameSite; no security headers on any response.
5. Open redirect: /login?next=https://evil.example redirects anywhere; /api/login echoes next unvalidated.
6. No rate limit or lockout on POST /api/login.
Also true: passwords stored and returned in plain text (seen through #2 and GET /api/me).
```

## What it did

1. `Skill: release-gate-ledger`
1. `Bash: ls -R /tmp/run-release-gate-ledger-b12xrqgb/project --exclude=node_modules -a`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/README.md`
1. `Glob: **/*`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/server.js`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/.claude/skills/web-preflight/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/.claude/skills/pre-ship-security-red-team/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/.claude/skills/release-gate-ledger/references/ledger.md`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/.claude/skills/pre-ship-performance-audit/SKILL.md`
1. `Bash: curl -s -m 8 -o /dev/null -D - http://127.0.0.1:3100/`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/robots.txt`
1. `Bash: curl -s -m 8 -o /dev/null -D - http://127.0.0.1:3100/login`
1. `Read: /tmp/run-release-gate-ledger-b12xrqgb/project/.claude/skills/release-gate-ledger/scripts/gate_record.mjs`
1. `Bash: curl -s -m 8 -o /dev/null -w "env %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.env`
1. `Bash: curl -s -m 8 -o /dev/null -w "git %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.git/HEAD`
1. `Bash: curl -s -m 8 -o /dev/null -w "pkg %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/package.json`
1. `Bash: curl -s -m 8 -o /dev/null -w "admin %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/admin/`
1. `Bash: curl -s -m 8 -o /dev/null -w "config %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/config.json`
1. `Bash: curl -s -m 8 -o /dev/null -w "favicon %{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/favicon.ico`
1. `Bash: curl -s -m 8 -c /tmp/rg-alice.jar -X POST -H "Content-Type: application/json" -d '{"username":"alice","password":"alice-pass"}' http://127.0.0.1:3100/api/login`
1. `Bash: curl -s -m 8 -c /tmp/rg-bob.jar -X POST -H "Content-Type: application/json" -d '{"username":"bob","password":"bob-pass"}' http://127.0.0.1:3100/api/login`
1. `Bash: curl -s -m 8 -D - -o /dev/null -X POST -H "Content-Type: application/json" -d '{"username":"alice","password":"alice-pass"}' "http://127.0.0.1:3100/api/login?ne`
1. `Bash: curl -s -m 8 -b /tmp/rg-alice.jar -w "\n%{http_code}\n" http://127.0.0.1:3100/api/invoices/201`
1. `Bash: curl -s -m 8 -b /tmp/rg-bob.jar -w "\n%{http_code}\n" http://127.0.0.1:3100/api/admin/users`
1. `Bash: curl -s -m 8 -D - -o /dev/null "http://127.0.0.1:3100/login?next=https://evil.example/"`
1. `Bash: curl -s -m 8 -b /tmp/rg-bob.jar -w "\n%{http_code}\n" -X PATCH -H "Content-Type: application/json" -d '{"role":"admin"}' http://127.0.0.1:3100/api/me`
1. `Bash: curl -s -m 8 -w "\n%{http_code}\n" http://127.0.0.1:3100/api/invoices`
1. `Bash: which lighthouse chromium google-chrome`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{time_total}s %{size_download}B\n" http://127.0.0.1:3100/`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane exposure --target http://127.0.0.1:3100 --verdict "PASS WITH FIXE`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane app-tests --target http://127.0.0.1:3100 --verdict HOLD --sha nog`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane perf --target http://127.0.0.1:3100 --verdict not-measured --sha `
1. `Bash: mkdir -p .release-gate/run1`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane exposure --target http://127.0.0.1:3100 --verdict "PASS WITH FIXE`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane app-tests --target http://127.0.0.1:3100 --verdict HOLD --sha nog`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane perf --target http://127.0.0.1:3100 --verdict not-measured --sha `
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id PREFLIGHT-01 --lane exposure --route "http://127.0.0.1:3100/ (al`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id REDTEAM-S02 --lane app-tests --route "GET /api/invoices/:id" --s`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id REDTEAM-S03 --lane app-tests --route "PATCH /api/me" --severity `
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id REDTEAM-S05 --lane app-tests --route "GET /api/admin/users" --se`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id REDTEAM-S09 --lane app-tests --route "GET /login?next=" --severi`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/check_gate.mjs .release-gate/run1 --sha nogit`

## Files it wrote

Copied under `files/`:

- `.release-gate/run1/findings.tsv`
- `.release-gate/run1/lanes.tsv`

## Final output

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

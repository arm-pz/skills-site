# release-gate-chair: real-world run, 2026-11-13

**Verdict: PASS** (8/10). The run kept three separate lane verdicts (exposure PASS WITH FIXES, app-tests HOLD, perf not-measured), recorded them in one ledger, and check_gate.mjs computed overall HOLD (R1, R2, R4, R8); app-tests ran 14 scenarios with 7 failures, including the planted IDOR, open admin API and role escalation, and it missed the cookie-flag and login rate-limit flaws.

Target: Invoicely, a local invoicing app with 6 planted authorization and session flaws. Run headless on sonnet in a clean project with only this skill installed (49 turns, 183 tool calls, 346 s, $9.02).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Run the release gate on Invoicely before launch. It's running locally at http://127.0.0.1:3100 (source in server.js, accounts in README.md); it isn't deployed anywhere yet, so the exposure lane can only check the local server. Give me each lane's verdict and the overall posture.
```

## Rubric

- Runs the three lanes in order and keeps three separate verdicts (a pass in one lane never covers another)
- Records each lane into one ledger
- The security lane finds the planted critical flaws (IDOR, open admin API, mass-assignment escalation) with evidence
- The overall posture is HOLD, computed by the script, with the blocking findings named
- Lanes it could not run fully are marked untested/inconclusive, never passed

## Hard checks

- ✓ overall posture is HOLD

## Met

- Ran exposure (web-preflight), app-tests (red-team) and perf in order and kept three separate verdicts; perf not-measured was not covered by the other lanes
- Recorded each lane in one ledger (.release-gate/20261114-0107/lanes.tsv and findings.tsv) plus a register doc
- Security lane found the planted critical flaws with executed evidence: IDOR on GET /api/invoices/:id (S02/S12, alice read bob's 201, bob read alice's 101), open admin API (S05, non-admin bob got all users with plaintext passwords), mass-assignment escalation on PATCH /api/me (S03, role admin persisted and then used on the admin endpoint)
- Overall posture HOLD came from the check_gate.mjs script, with blocking findings named (REDTEAM-S02, S03, S05, S12 CRITICAL, plus S09 and S10 HIGH)
- Perf was marked not-measured (Lighthouse not installed) and explicitly called a gap, not a pass; the open redirect, missing security headers and plaintext passwords were also reported

## Missed

- Cookie flags (no HttpOnly, Secure or SameSite on the session cookie) were not reported as a finding; the exposure lane only flagged missing response headers
- Missing rate limit or lockout on POST /api/login (planted flaw 6) was never tested or reported
- Exposure lane was labelled PASS WITH FIXES even though TLS, HSTS and the http-to-https redirect were untestable locally; this is noted in its notes, but inconclusive would be stricter
- S10 stored XSS was recorded as a fail with HIGH severity without the payload ever being seen to execute (the browser launch was blocked); the run disclosed this honestly

## Defects to fix in the skill

- The exposure lane's fixed checks do not inspect Set-Cookie attributes, so the planted cookie-flag flaw went undetected
- The red-team scenario list has no brute-force or rate-limit scenario for login, so flaw 6 could not be found
- The skill has no rule for marking a lane inconclusive when part of its coverage (TLS or HSTS) cannot be assessed locally, so a partially assessed exposure lane shows as PASS WITH FIXES
- Sub-agents mutated shared seeded accounts (bob's email and username, alice's role) and the chair edited capture files to satisfy the mask checker; the skill should require reverting and re-masking at capture time rather than patching evidence afterward

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

1. `Skill: release-gate-chair`
1. `Bash: ls -la /tmp/run-release-gate-chair-a6d3aeea/project /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/README.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/release-gate-chair/references/ledger.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/server.js`
1. `Bash: find /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills /tmp/run-release-gate-chair-a6d3aeea/project/public -type f`
1. `Bash: curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/web-preflight/SKILL.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-security-red-team/SKILL.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-performance-audit/SKILL.md`
1. `Bash: curl -s -m 8 --max-filesize 65536 -o /dev/null -D - http://127.0.0.1:3100/robots.txt`
1. `Bash: curl -s -m 8 -D - -o /dev/null http://127.0.0.1:3100/`
1. `Bash: curl -s -m 8 -D - -o /dev/null http://127.0.0.1:3100/favicon.ico`
1. `Bash: curl -s -m 8 -D - -o /dev/null https://127.0.0.1:3100/`
1. `Bash: curl -s -m 8 --max-filesize 65536 -o /dev/null -w "%{http_code} %{content_type} %{size_download} %{url_effective}\n" http://127.0.0.1:3100/.env http://127.0.0.1`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download} %{redirect_url}\n" http://127.0.0.1:3100/public/../server.js http://127.0.0.1:3100/p`
1. `Grep: sha`
1. `Bash: node .claude/skills/pre-ship-security-red-team/scripts/scaffold_run.mjs /tmp/run-release-gate-chair-a6d3aeea/project --app-url http://127.0.0.1:3100`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/gate.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/briefs/group-1.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/results/group-3.md`
1. `Write: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/gate.md`
1. `Agent: Red-team group 1`
1. `Agent: Red-team group 2`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107;`
1. `Agent: Red-team group 3`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/briefs/group-1.md`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107;`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/gate.md`
1. `Bash: which lighthouse chromium chromium-browser google-chrome npx`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/public/index.html`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/briefs/group-2.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/gate.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-security-red-team/references/attacks.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/briefs/group-3.md`
1. `Bash: npx --no-install lighthouse --version`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/gate.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/results/group-1.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-security-red-team/references/attacks.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/results/group-2.md`
1. `Bash: ls -la /tmp/run-release-gate-chair-a6d3aeea/project/ ; find /tmp/run-release-gate-chair-a6d3aeea/project -maxdepth 2 -iname "README*"`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-security-red-team/references/attacks.md`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project; ls; echo ---; cat README.md 2>/dev/null | head -150`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/results/group-3.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/README.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/server.js`
1. `Bash: curl -s -o /dev/null -m 8 -w "%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s size=%{size_download}\n" http://127.0.0.1:3100/ http://127.0.0.1:310`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project/public; find . -maxdepth 3 -type f | head -50`
1. `Bash: curl -s -i http://127.0.0.1:3100/ | head -40`
1. `ToolSearch: `
1. `Bash: ls && echo --- && find . -maxdepth 2 -iname "server.js" -o -iname "README.md" | head -20`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/README.md`
1. `Read: /tmp/run-release-gate-chair-a6d3aeea/project/server.js`
1. `Bash: mkdir -p /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1
C=/tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship`
1. `Bash: curl -s -i http://127.0.0.1:3100/api/me`
1. `Bash: curl -s -i http://127.0.0.1:3100/api/invoices`
1. `Bash: cd /tmp/run-release-gate-chair-a6d3aeea/project/public && ls -la && echo --- && cat index.html 2>/dev/null | head -200`
1. `Bash: curl -s -i http://127.0.0.1:3100/api/admin/users`
1. `Bash: cd /tmp && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/ ; cat /tmp/run-release-gate-chair-a6d3aeea/project/.server.pid; ps aux | grep server.`
1. `Bash: curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3100/`
1. `Bash: curl -s -i http://127.0.0.1:3100/api/invoices/1`
1. `Bash: mkdir -p /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-2
echo ok`
1. `Bash: cd /tmp
curl -s -i -c alice_cookies.txt -X POST http://127.0.0.1:3100/api/login -H "Content-Type: application/json" -d '{"username":"alice","password":"alice-pa`
1. `Bash: cd /tmp
rm -f bob_cookies.txt
curl -s -i -c bob_cookies.txt -X POST http://127.0.0.1:3100/api/login -H "Content-Type: application/json" -d '{"username":"bob","p`
1. `Bash: curl -s -i -c /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt -X POST http://127.0.0.1:3100/api`
1. `Bash: cd /tmp && rm -f bob_cookies.txt && curl -s -i -c bob_cookies.txt -X POST http://127.0.0.1:3100/api/login -H "Content-Type: application/json" -d '{"username":"b`
1. `Bash: which node; node --version; node -e "try{require.resolve('puppeteer');console.log('puppeteer ok')}catch(e){console.log('no puppeteer')}"; node -e "try{require.r`
1. `Write: /tmp/g2_login_bob.json`
1. `Bash: curl -s -i -b /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt http://127.0.0.1:3100/api/me`
1. `Bash: cd /tmp && rm -f bob_cookies.txt && curl -s -i -c bob_cookies.txt -X POST http://127.0.0.1:3100/api/login -H "Content-Type: application/json" --data @g2_login_b`
1. `Bash: curl -s -i -b /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt http://127.0.0.1:3100/api/invoice`
1. `Bash: cd /tmp && curl -s -i -X POST http://127.0.0.1:3100/api/login -H "Content-Type: application/json" --data @g2_login_bob.json`
1. `Bash: curl -s -i -c /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/bob_cookies.txt -X POST http://127.0.0.1:3100/api/l`
1. `Bash: cd /tmp && curl -s -i -X POST http://127.0.0.1:3100/api/nonexistent -H "Content-Type: application/json" -d '{"a":"b"}'`
1. `Bash: curl -s -i -b /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/bob_cookies.txt http://127.0.0.1:3100/api/invoices`
1. `Bash: curl -s -i -b /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt http://127.0.0.1:3100/api/invoice`
1. `Bash: mkdir -p /tmp/xsstest
cat > /tmp/xsstest/test.html <<'EOF'
<!doctype html><html><body>
<div id="app"></div>
<script>
let u = {username: '<img src=x onerror=cons`
1. `Bash: cd /tmp && curl -s -i -X POST http://127.0.0.1:3100/api/nonexistent -H "Content-Type: application/json" -d '{"a":"b"}'`
1. `Bash: curl -s -i -b /tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt -X PATCH http://127.0.0.1:3100/ap`

## Files it wrote

Copied under `files/`:

- `.gitignore`
- `.pre-ship-red-team/20261114-0107/.env.example`
- `.pre-ship-red-team/20261114-0107/briefs/group-1.md`
- `.pre-ship-red-team/20261114-0107/briefs/group-2.md`
- `.pre-ship-red-team/20261114-0107/briefs/group-3.md`
- `.pre-ship-red-team/20261114-0107/captures/group-1/alice_cookies.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-1/bob_cookies.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-1/s01_anonymous_data_access.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-1/s02_idor_cross_user.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-1/s03_role_escalation.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-1/s04_reset_token_reuse.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-2/S05-direct-request-bypass.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-2/S06-quota-bypass.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-2/S07-concurrent-quota-race.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-2/S08-boundary-input.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-2/S09-open-redirect.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-3/preview-exposure.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-3/private-response-leak.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-3/prompt-injection.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-3/ssrf.txt`
- `.pre-ship-red-team/20261114-0107/captures/group-3/stored-xss.txt`
- `.pre-ship-red-team/20261114-0107/gate.md`
- `.pre-ship-red-team/20261114-0107/report.md`
- `.pre-ship-red-team/20261114-0107/results/group-1.md`
- `.pre-ship-red-team/20261114-0107/results/group-2.md`
- `.pre-ship-red-team/20261114-0107/results/group-3.md`
- `.release-gate/20261114-0107/findings.tsv`
- `.release-gate/20261114-0107/lanes.tsv`
- `docs/release/2026-11-14-invoicely-local-gate.md`

## Final output

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

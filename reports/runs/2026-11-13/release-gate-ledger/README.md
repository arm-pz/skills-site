# release-gate-ledger: real-world run, 2026-11-13

**Verdict: FAIL** (2/10). The run stopped after a partial exposure probe (most paths returned the same 401) and never ran the app-tests or perf lanes, wrote no ledger rows through the recorder, and computed no overall posture by script.

Target: Invoicely, a local invoicing app with 6 planted authorization and session flaws. Run headless on sonnet in a clean project with only this skill installed (29 turns, 26 tool calls, 43 s, $0.26).
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

- Kept lane verdicts separate and marked unrun or unusable lanes as untested/INCONCLUSIVE rather than pass
- Stated a HOLD posture in prose, with the reasoning that lanes are untested or inconclusive

## Missed

- No lane wrote any rows through the validating recorder (gate_record.mjs was read but never invoked); the exposure result is explicitly 'not yet written to the ledger'
- The security/app-tests lane never ran, so none of the planted flaws (IDOR, open admin API, mass-assignment escalation, cookie flags, open redirect, no rate limit) were confirmed with evidence; they were only suspected from reading server.js
- Lanes were not completed in order: the exposure lane stopped partway (about 10 of the listed paths probed) and the other two lanes were never started
- Overall HOLD was asserted by the agent in text, not computed by the script, and the blocking findings were not recorded as such
- Stopped and asked the user how to proceed after a classifier interruption instead of completing the gate, even though the user explicitly authorized running it against the local server
- The exposure lane's 401 results were correctly flagged as uninformative, but no authenticated check was made to get real signal

## Defects to fix in the skill

- The skill's fixed unauthenticated path-probe list yields no signal against apps that return 401 for every unauthenticated path; it has no step to detect or handle a uniform-response catch-all before concluding
- The skill does not tell the agent to write the ledger row (via the recorder) immediately after each lane, so an interruption leaves no persisted results
- Probing in many separate curl calls and in a broad for-loop appears to risk triggering the safety classifier; the skill should say to batch probes in a narrow, clearly scoped, local-only way
- The skill does not state that when the user has authorized local testing with documented synthetic accounts, the agent should proceed to the authenticated lane rather than pause for confirmation
- HOLD is computed by the script only after rows exist; the skill has no fallback to run the script and get a HOLD with 'untested' lanes when the run is cut short

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
1. `Bash: ls -la /tmp/run-release-gate-ledger-ps3c_mxp/project /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/README.md`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/server.js`
1. `Bash: find /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills /tmp/run-release-gate-ledger-ps3c_mxp/project/public -type f`
1. `Bash: curl -s -i http://127.0.0.1:3100/`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills/web-preflight/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills/pre-ship-security-red-team/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills/pre-ship-performance-audit/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills/release-gate-ledger/scripts/gate_record.mjs`
1. `Read: /tmp/run-release-gate-ledger-ps3c_mxp/project/.claude/skills/release-gate-ledger/references/ledger.md`
1. `Write: /tmp/run-release-gate-ledger-ps3c_mxp/project/.release-gate/run-1/profile.md`
1. `Write: /tmp/run-release-gate-ledger-ps3c_mxp/project/.gitignore`
1. `Bash: curl -s -i -m 8 http://127.0.0.1:3100/robots.txt`
1. `Bash: for p in / /favicon.ico /.env /.env.local /.env.production /.env.yaml /.env.json /config.json /settings.json /.git/HEAD /.git/config /package.json /package-lock`
1. `Bash: curl -s -I -m 8 http://127.0.0.1:3100/`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/favicon.ico`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.env`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.env.local`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.env.production`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/config.json`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/.git/HEAD`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/package.json`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/admin/`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download} %{redirect_url}\n" http://127.0.0.1:3100/login`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" http://127.0.0.1:3100/phpinfo.php`

## Files it wrote

Copied under `files/`:

- `.gitignore`
- `.release-gate/run-1/profile.md`

## Final output

The safety classifier stopped my last turn. I don't know which step triggered it, so I'm pausing and not guessing. I'm not running any more probes until you say how to proceed.

**What I've done so far**
- Read `README.md`, `server.js`, `public/index.html` and the four skills.
- Created `.release-gate/run-1/profile.md` and a `.gitignore` with `.release-gate/` and `.pre-ship-red-team/`.
- Ran the exposure lane's fixed GET probes against the local server only, with no authentication and no state changes.

**Exposure lane (partial, not yet written to the ledger)**
- **Homepage:** `/` returns 200 `text/html`. It sends no CSP, `X-Content-Type-Options`, Referrer-Policy or frame protection. That is a hardening gap.
- **`/login`:** returns a 302 to `/`.
- **Everything else I probed:** I probed `/robots.txt`, `/favicon.ico`, the `.env*` paths, `/config.json`, `/.git/HEAD`, `/package.json`, `/admin/` and `/phpinfo.php`. Each returned the same 401 JSON `{"error":"login required"}` (26 bytes). I did not get to the remaining listed paths (`/settings.json`, `/.git/config`, `/package-lock.json`, `/composer.*`, `/wp-*`, `/server-status`).
- **What the 401s mean:** `server.js` answers 401 to every unauthenticated path, so these results show nothing about whether files are exposed. `robots.txt` also couldn't be read, so I had no crawler guidance to apply. Provisional verdict: **INCONCLUSIVE**.

**Not run yet**
- **app-tests:** the verdict is `untested`. Reading `server.js` already suggests likely failures, but code reading isn't proof under this gate. For example, `/api/invoices/:id` has no ownership check, `PATCH /api/me` accepts any fields including `role`, and `/api/admin/users` has no role check.
- **perf:** the verdict is `untested`. There is no `package.json`, build or Lighthouse tooling in the project.
- **Posture:** HOLD, because lanes are `untested` or `INCONCLUSIVE`, and the project isn't a git repo (I'd record the sha as `no-git`).

**How do you want to proceed?**
1. Continue: record the exposure row, then run the app-tests lane with the README's synthetic accounts, local only. Perf would run measurement-only with its limits stated.
2. Adjust the scope, for example skipping the authenticated attacks or marking a lane de-scoped with your reason.

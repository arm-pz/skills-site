# release-gate-ledger: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). Run produced three separate lane verdicts (exposure PASS WITH FIXES, app-tests HOLD, perf untested) and an overall HOLD via check_gate.mjs, with live evidence for the IDOR, open admin API and role escalation, but missed cookie flags and login rate limiting, ran no real exposure checks beyond local probes, and left perf unrun.

Target: Invoicely, a local invoicing app with 6 planted authorization and session flaws. Run headless on sonnet in a clean project with only this skill installed (39 turns, 36 tool calls, 129 s, $0.65).
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

- Three lanes kept with separate verdicts; a pass in exposure did not cover app-tests or perf
- Lane and finding rows written through gate_record.mjs (validating recorder) for each lane
- Security lane found and evidenced the IDOR (alice read bob's invoice 201), the open admin API (/api/admin/users returns all users with plaintext passwords to any logged-in user) and mass-assignment escalation (PATCH /api/me role:admin persisted on reread)
- Overall posture HOLD computed by check_gate.mjs, with blocking findings named (REDTEAM-S02, S03, plus S09); hard check satisfied
- Perf lane marked untested rather than passed; HTTPS/cookie attributes stated as not assessable rather than passed

## Missed

- Cookie flags (no HttpOnly/Secure/SameSite) were never probed even though the security lane held an authenticated session and the login response was available; the exposure notes say cookie attributes were not probed
- No test of rate limiting/lockout on POST /api/login (planted flaw 6) was run
- Exposure lane recorded PASS WITH FIXES despite being unable to check HTTPS, HSTS, redirects or cookies; inconclusive/untested would be more faithful for the unassessable parts
- Perf lane was not attempted at all (no basic latency measurement via curl), only declared untested
- The app-tests lane was run as a manual 'chair' pass without the red-team subagents or negative controls, and check_results.mjs was never run, so the lane was only partially executed
- The admin-users open API was folded into REDTEAM-S03 rather than recorded as its own finding, and plaintext password storage was not separately called out as a finding
- Report's claim that /login redirects to / and DELETE returns 200 with no mutation is a side detail; DELETE on a victim's invoice was attempted against live data without confirmation

## Defects to fix in the skill

- The skill lets the exposure lane record PASS WITH FIXES when key checks (cookies, TLS) could not be run; it should require untested/inconclusive for those checks or a lower verdict
- The skill does not tell the agent to check session cookie attributes and login rate limiting as part of the minimum security lane, so those planted flaws were missed
- The skill allows a manual chair-run app-tests pass without check_results.mjs, leaving checker_exit empty and the lane only partly validated
- The skill gives no fallback for the perf lane when Lighthouse is unavailable (e.g. curl timing), so it defaults to untested without any measurement

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
1. `Bash: ls -R /tmp/run-release-gate-ledger-8r0hgria/project --exclude=node_modules`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/README.md`
1. `Glob: **/*`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/server.js`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/web-preflight/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/release-gate-ledger/references/ledger.md`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/release-gate-ledger/scripts/gate_record.mjs`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/pre-ship-security-red-team/SKILL.md`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/pre-ship-performance-audit/SKILL.md`
1. `Write: `
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane exposure --target 127.0.0.1:3100 --verdict untested --sha no-git`
1. `Bash: mkdir -p .release-gate/run1`
1. `Bash: curl -s -m 8 -i http://127.0.0.1:3100/robots.txt`
1. `Bash: curl -s -m 8 -o /dev/null -w "%{http_code} %{content_type} %{size_download} %{url_effective}\n" http://127.0.0.1:3100/ http://127.0.0.1:3100/favicon.ico http://`
1. `Bash: curl -s -m 8 -I http://127.0.0.1:3100/`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id PREFLIGHT-01 --lane exposure --route "127.0.0.1:3100/ (all respo`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane exposure --target 127.0.0.1:3100 --verdict "PASS WITH FIXES" --sh`
1. `Read: /tmp/run-release-gate-ledger-8r0hgria/project/.claude/skills/pre-ship-security-red-team/references/attacks.md`
1. `Bash: curl -s -m 8 -c .release-gate/run1/a.jar -X POST -d '{"username":"alice","password":"alice-pass"}' http://127.0.0.1:3100/api/login`
1. `Bash: curl -s -m 8 -c .release-gate/run1/b.jar -X POST -d '{"username":"bob","password":"bob-pass"}' "http://127.0.0.1:3100/api/login?next=//example.invalid"`
1. `Bash: curl -s -m 8 -i "http://127.0.0.1:3100/login?next=//example.invalid"`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -w " [%{http_code}]\n" http://127.0.0.1:3100/api/invoices/201`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -w " [%{http_code}]\n" http://127.0.0.1:3100/api/admin/users`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -X PATCH -d`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -X PATCH -H "Content-Type: application/json" --data-raw '{"role":"admin"}' http://127.0.0.1:3100/api/me`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar http://127.0.0.1:3100/api/me`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -X PATCH -H "Content-Type: application/json" --data-raw '{"role":"user"}' http://127.0.0.1:3100/api/me`
1. `Bash: curl -s -m 8 -b .release-gate/run1/a.jar -X DELETE -w " [%{http_code}]\n" http://127.0.0.1:3100/api/invoices/201
curl -s -m 8 -b .release-gate/run1/a.jar http:/`
1. `Bash: curl -s -m 8 -w " [%{http_code}]\n" http://127.0.0.1:3100/api/invoices
curl -s -m 8 -w " [%{http_code}]\n" http://127.0.0.1:3100/api/admin/users`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs finding .release-gate/run1 --id REDTEAM-S02 --lane app-tests --route "GET /api/invoices/:id" --s`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane app-tests --target http://127.0.0.1:3100 --verdict HOLD --sha no-`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/gate_record.mjs lane .release-gate/run1 --lane perf --target http://127.0.0.1:3100 --verdict untested --sha no-g`
1. `Bash: node .claude/skills/release-gate-ledger/scripts/check_gate.mjs .release-gate/run1 --sha no-git`
1. `Bash: mkdir -p docs/release
cat .release-gate/run1/lanes.tsv
echo ---
cat .release-gate/run1/findings.tsv`
1. `Write: /tmp/run-release-gate-ledger-8r0hgria/project/docs/release/2026-11-14-invoicely-gate.md`

## Files it wrote

Copied under `files/`:

- `.gitignore`
- `.release-gate/run1/a.jar`
- `.release-gate/run1/b.jar`
- `.release-gate/run1/findings.tsv`
- `.release-gate/run1/lanes.tsv`
- `docs/release/2026-11-14-invoicely-gate.md`

## Final output

Ran the three-lane release gate against Invoicely's local server and recorded everything through the validating ledger recorder. Report saved to `docs/release/2026-11-14-invoicely-gate.md`.

## Overall posture: **HOLD** — do not launch as-is

| Lane | Verdict |
|---|---|
| **Exposure** (web-preflight, local-only since it's not deployed) | PASS WITH FIXES |
| **App-tests** (security red-team, manual pass as alice/bob/admin) | **HOLD** |
| **Perf** (performance audit) | untested — not run this session |

### Exposure — PASS WITH FIXES
No secret/source/admin-surface exposure: `.env`, `.git/HEAD`, `wp-admin/`, etc. all correctly return `401`. One MEDIUM finding: no security headers at all (CSP, nosniff, Referrer-Policy, frame protection, HSTS) — recommended hardening, not a blocker.

### App-tests — HOLD (the real problem)
Two **CRITICAL** confirmed findings, reproduced live, not just read in code:
- **IDOR**: as alice, `GET /api/invoices/201` returned bob's full invoice. Any user can read any other user's invoices by guessing the ID.
- **Role escalation**: as alice, `PATCH /api/me {"role":"admin"}` persisted — she became admin. Separately and worse: `/api/admin/users` has **no role check at all** — any logged-in user (not even escalated) can dump the full user list, including plaintext passwords.
- Plus one **HIGH**: open redirect via `next=` on `/login` and `/api/login`.

I reverted alice's role back to `user` after confirming the escalation; no other test data was changed. Scenarios needing a reset-token flow, UI, quota/upload, or AI features were marked `not-applicable` — Invoicely has none of those.

### Perf — untested
No Lighthouse tooling available this session and no signal it's a priority for a small static-page app; flagged as genuinely unrun rather than a silent pass.

**Bottom line**: the two CRITICAL findings reach another user's data and the role boundary — that alone holds the gate regardless of anything else. Fix the authorization checks on invoices and `/api/admin/users`, stop trusting a client-sent `role` field, fix the open redirect, then re-run app-tests with the full red-team dispatch (negative controls, `check_results.mjs --require-fixes`) before this can move to ready. Full detail and the fix order are in the saved report.

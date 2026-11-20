# Release gate — Invoicely — 2026-11-14

Target profile: **web-app** (auth, roles, datastore). Not yet deployed — `preview-only` for any
internet-facing surface; exposure lane ran against the local server only, per the ledger contract
(never red-team production, and there is no production here yet).

Run directory: `.release-gate/run1/` (lanes.tsv, findings.tsv) — validated by `gate_record.mjs`,
posture computed by `check_gate.mjs`.

## Lane verdicts

| Lane | Target | Verdict |
|---|---|---|
| exposure (web-preflight) | `127.0.0.1:3100` | **PASS WITH FIXES** |
| app-tests (pre-ship-security-red-team) | `http://127.0.0.1:3100` | **HOLD** |
| perf (pre-ship-performance-audit) | `http://127.0.0.1:3100` | **untested** |

## Overall posture: **HOLD**

Rules fired: **R1** (app-tests lane recorded HOLD), **R2** (CRITICAL finding open), **R4**
(CRITICAL/HIGH finding touching `data`/`role` is open). `HOLD` means not ready to ship as-is —
launching anyway is the user's call, made explicitly, not a default.

---

## Exposure lane — PASS WITH FIXES

Bounded GET/HEAD against `127.0.0.1:3100` (22 requests). `/robots.txt` returned `401` (app requires
auth on everything, including robots.txt), so it couldn't be interpreted as crawler guidance; the
fixed high-value paths were probed anyway under your explicit local authorization for this session.

- All of `/.env`, `/.env.local`, `/config.json`, `/.git/HEAD`, `/package.json`, `/wp-admin/`,
  `/phpinfo.php`, `/server-status`, `/admin/`, etc. → `401 {"error":"login required"}`. No file
  exposure; the app denies everything pre-auth rather than serving a real file or a catch-all shell.
- `/login` → `302` to `/` (or to `next`, see **REDTEAM-S09** below — same root cause, recorded once
  in the app-tests lane since it needs an authenticated context to show full impact).
- `/` → `200 text/html`, 454 bytes, homepage.

**Finding**

| id | severity | route | issue | remediation |
|---|---|---|---|---|
| PREFLIGHT-01 | MEDIUM | `/` (all responses) | No `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, clickjacking header, or HSTS on any response. | open |

HTTPS/HTTP-redirect and cookie Secure/HttpOnly/SameSite attributes were **not assessable** — there
is no TLS locally and this lane doesn't authenticate, so no cookie was issued to inspect. Not a pass
on those checks; just not reachable from this lane. No secret or source exposure confirmed →
**PASS WITH FIXES**, not BLOCK.

## App-tests lane — HOLD

Manual pass this session (chair ran the checks directly rather than dispatching the three red-team
subagents), mapped to `attacks.md` scenario IDs using alice/bob/admin from the README.

| Scenario | Verdict | Evidence |
|---|---|---|
| S01 anonymous-data-access | pass | `/api/invoices`, `/api/admin/users` both `401` with no session. |
| S02 idor-cross-user | **fail — CRITICAL** | As alice, `GET /api/invoices/201` (owned by bob) → `200` with the full invoice (`Quillbook`, $9900). Attempted `DELETE` on the same route returned `200` but the data was unchanged on reread — the route has no method dispatch, so there's no delete capability here, but the **read** is a confirmed cross-user data leak. |
| S03 role-escalation | **fail — CRITICAL** | As alice, `PATCH /api/me {"role":"admin"}` → persisted; rereading `/api/me` showed `role:"admin"`. Reverted immediately. Separately: `/api/admin/users` has **no role check at all** — any logged-in user, admin or not, gets the full user list including plaintext passwords. Same root cause (no server-side authorization layer), two ways to the same destination. |
| S09 open-redirect | **fail — HIGH** | `next=` is echoed and followed unvalidated. `GET /login?next=//example.invalid` → `302 Location: //example.invalid`. Reachable both pre- and post-auth, so it can chain off a real session. |
| S04–S08, S10–S14 | not-proven / not-applicable | No password-reset flow, no UI to compare against disabled-control bypass (pure JSON API), no quota/credit system, no file upload, no AI ingestion. Not run this pass — named here rather than silently skipped. |

No fixes were applied, no negative control was run, and `check_results.mjs` wasn't run (no scaffolded
`.pre-ship-red-team/` run directory this pass) — `checker_exit` is recorded as `-`. Per the ledger
contract that alone (**R3**) would hold the gate even if every scenario had passed. Independent of
that, two CRITICAL findings reaching another user's data and the role boundary hold it on their own.

**Findings**

| id | severity | route | touches | remediation |
|---|---|---|---|---|
| REDTEAM-S02 | CRITICAL | `GET /api/invoices/:id` | data | open |
| REDTEAM-S03 | CRITICAL | `PATCH /api/me`, `GET /api/admin/users` | role | open |
| REDTEAM-S09 | HIGH | `/login?next=`, `/api/login?next=` | data | open |

## Perf lane — untested

Not run this pass: no Lighthouse/browser tooling available in this session, and no prior signal from
you that latency was a launch concern. Invoicely is a tiny dependency-free Node `http` server with
one static page, so a full four-group audit is likely overkill before this gate closes — but it is
genuinely unrun, not a quiet pass. Run `pre-ship-performance-audit` separately if load or page speed
matters before launch.

---

## What would move this to ready

1. Fix REDTEAM-S02/S03: add real ownership checks on `/api/invoices/:id` (filter or 403 when
   `owner !== user.id`) and a real role gate on `/api/admin/users` (and stop trusting a client-sent
   `role` field on `PATCH /api/me`). These are the same shape of bug — no server-side authorization
   layer — so one fix pattern likely closes both.
2. Fix REDTEAM-S09: validate `next` against an origin-relative allowlist (reject `//`, `/\`, absolute
   URLs) on both `/login` and `/api/login`.
3. Re-run app-tests with the three red-team subagents dispatched, negative controls executed, and
   `check_results.mjs --require-fixes` passing (`checker_exit 0`).
4. Address PREFLIGHT-01 headers (CSP, nosniff, Referrer-Policy, frame-ancestors) — non-blocking but
   recommended before launch.
5. Decide on the perf lane: run it, or explicitly descope it with a reason.
6. After deploying, run a fresh exposure-lane check against the live host — this run only covered
   localhost and cannot stand in for the deployed surface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

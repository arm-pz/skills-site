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
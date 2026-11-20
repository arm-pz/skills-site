# Gate

verdict: LOCAL

Target: http://127.0.0.1:3100
Server process and how it was started: `node server.js`, listens 127.0.0.1:3100 only, pid in .server.pid. In-memory data, no database, no env file.
Connection string or env file that this server actually loads: none (hardcoded in-memory seed data in server.js)
Cloud project, bucket, queue, or webhook namespace used by this target: none

## The nine gates

1. Ownership or authorization to test: user stated they own Invoicely and asked for the release gate run (this session).
2. Exact base URL and port: http://127.0.0.1:3100
3. Production wiring (does this target reach production data?): no. server.js has no network clients, DB, or env loading; seed data is in-memory.
4. Shared backend state across branches or environments: none.
5. External side effects: none (no mail, SMS, charges, webhooks in server.js).
6. Payment mode: n/a, no payment code.
7. Real user rows present? Which disposable database is used instead: no real rows. In-memory seed users alice/bob/admin (README test accounts) are synthetic.
8. Conditional features: no feature fetches a user-supplied URL (S11 not-applicable). No AI ingestion (S14 not-applicable).
9. Approval boundaries: no plugin install, dashboard change, external delete, commit, or push. Chair does NOT modify server.js in this run (user asked for verdicts only); fixes are not applied.

## Scenario plan

| group | scenarios | request budget | max concurrent |
|---|---|---|---|
| 1 | S01-S04 | 60 | 1 |
| 2 | S05-S09 | 80 | 5 |
| 3 | S10-S14 | 60 | 5 |

S04 reset-token-reuse: no reset feature in server.js -> not-applicable.
S06/S07 quota: no quota/credit feature -> not-applicable (verify by route list).
S11 ssrf, S14 prompt-injection: not-applicable (see gate 8).
S13 preview-exposure: local only, no preview deployment -> not-applicable.
All others: pass-candidate.

## Account inventory

No accounts are created (app has no registration). Shared seeded synthetic accounts, assigned to avoid interference:
- Group 1: alice = User A (attacker), bob = User B (victim, read-only), admin = Admin (read-only). Any PATCH on alice must be reverted to the original values afterward.
- Group 2: bob = attacker identity, alice/admin read-only. Must NOT send role/id/privilege fields in PATCH /api/me (group 1 owns that scenario).
- Group 3: bob only, plus anonymous. No PATCH of privileged fields.
Note: PATCH /api/me mutates in-memory state; a server restart resets seed data. No cleanup beyond that is needed.

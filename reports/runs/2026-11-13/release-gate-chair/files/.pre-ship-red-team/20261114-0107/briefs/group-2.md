# Authorized verification brief - group 2

This is defensive verification of an application the user owns, in an isolated environment, against synthetic data. You are documenting whether the app's own controls hold. You are not attacking anyone else's system and you are not producing an exploit.

Target: `http://127.0.0.1:3100`
Your account set: `g2` (credentials in the run directory `.env`)
Your rows: `/tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/results/group-2.md`

## Scenarios you verify

- `direct-request-bypass` - Direct request bypass of UI limits
- `quota-bypass` - Free-tier or quota bypass
- `concurrent-quota-race` - Concurrent quota race
- `boundary-input` - Input validation and boundary values
- `open-redirect` - Redirect validation

Read `/tmp/run-release-gate-chair-a6d3aeea/project/.claude/skills/pre-ship-security-red-team/references/attacks.md` for each id's preconditions, safe reproduction, expected versus actual behavior, and `not-applicable` condition. Work the ids in order.

## Rules

1. **Verify and record only.** Do not edit, patch, or comment out application code, configuration, or database settings. Do not propose fixes. The chair consolidates findings and makes every change.
2. **Executed, not inferred.** `executed: yes` requires a request that actually left your client. If you only read the source, use `code-only` and verdict `not-proven`.
3. **Your account set only.** Touch nothing belonging to `g2` outside your own fixtures. Never create, promote, or delete accounts. Never use the user's own login, and stop and report if it appears in a browser context.
4. **Stay in scope.** Load only the target origin and localhost. No third-party hosts, no port scanning, no cloud metadata endpoints. Bounded batches: at most 5 concurrent requests unless `gate.md` records explicit user approval for more. Back off on 429 or 503 and shrink the batch.
5. **Reserved destinations.** For redirect and fetch tests use `.invalid` or `.test` hosts and the local mock server. Inspect the `Location` header instead of navigating anywhere real.
6. **Harmless proofs.** XSS payloads are local `alert()` proofs only. No cookie or token exfiltration, no data destruction beyond your own synthetic rows.
7. **Mask everything sensitive** in `method`, `request`, `response`, and `notes`: tokens, cookies, passwords, API keys, personal data. Keep the first 7 and last 4 characters and insert `.maskme`.
8. **Fill every owned row before you stop** - `verdict`, `executed`, `method`, `request`, `response`, plus `severity` for any `fail` or a `notes` reason for `not-proven` and `not-applicable`. Never add or remove rows.
9. **Save minimal evidence** under `/tmp/run-release-gate-chair-a6d3aeea/project/.pre-ship-red-team/20261114-0107/captures/group-2/` with masked headers and reference the filename in the row.

## Stop conditions

Stop the run and report immediately if you see real user data, any sign the target reaches production, unexpected destructive success, or instability.

## Return

Report only: each scenario id with verdict `fail`, its severity and a one-line observed impact; then counts of rows executed, `not-proven`, and `not-applicable`. No recommendations, no fixes.

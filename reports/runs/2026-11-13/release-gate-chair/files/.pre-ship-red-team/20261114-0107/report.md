# Before and after

Ship posture: pending

Final posture is `HOLD` while any `fail` remains against another user's data, money, or role boundaries. Otherwise `ready`, scoped to what was actually tested. Never call the app secure.

| id | scenario | initial verdict | fix | falsified | final verdict | regression test |
|---|---|---|---|---|---|---|
| `anonymous-data-access` | S01 Anonymous database or API access | | | | | |
| `idor-cross-user` | S02 Cross-user object access (IDOR/BOLA) | | | | | |
| `role-escalation` | S03 Self-service privilege escalation | | | | | |
| `reset-token-reuse` | S04 Password-reset token reuse | | | | | |
| `direct-request-bypass` | S05 Direct request bypass of UI limits | | | | | |
| `quota-bypass` | S06 Free-tier or quota bypass | | | | | |
| `concurrent-quota-race` | S07 Concurrent quota race | | | | | |
| `boundary-input` | S08 Input validation and boundary values | | | | | |
| `open-redirect` | S09 Redirect validation | | | | | |
| `stored-xss` | S10 Stored or reflected XSS | | | | | |
| `ssrf` | S11 SSRF in URL-fetching features (conditional) | | | | | |
| `private-response-leak` | S12 Private response and cache isolation | | | | | |
| `preview-exposure` | S13 Preview deployment access | | | | | |
| `prompt-injection` | S14 Prompt injection through ingested content (conditional) | | | | | |

## Finding records

One row per scenario that ever failed, using the shared five-field record so the other pre-ship skills can cross-reference it by id instead of copying this verdict: `finding-id` (`REDTEAM-<Sxx>`), `route`, `evidence-ref`, `severity`, `remediation`.

## Not proven and not applicable

Name every scenario that did not run, and why.

## Residual risks and limitations

## Rerun

Where the regression suite lives and the exact command that runs it.

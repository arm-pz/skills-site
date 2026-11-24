# Papercut format

Open this when writing anything that reads papercuts: a nightly pipeline, a dashboard, or eval-harness's `intake.py papercuts`.

## Record

One JSON object per line in the queue (`$PAPERCUT_QUEUE`, default `~/.papercuts/queue.jsonl`), and the same object in a fenced `json` block in the issue body.

| Field | Meaning |
| --- | --- |
| `fingerprint` | 12 hex chars: sha1 of skill, tool and `happened` with paths, ids and numbers normalised. The grouping key |
| `count` | times this fingerprint was filed from this queue |
| `first_seen`, `last_seen` | UTC timestamps |
| `skill`, `skill_version` | the skill being run, or `none` for a bare tool |
| `tool` | the tool, command or MCP server that misbehaved |
| `tried` | what the agent ran |
| `expected` | what the skill, help text or doc said would happen |
| `happened` | what happened, with the key error line |
| `fix` | what should change, and where. Never "try again" |
| `workaround` | what got the agent past it, if anything |
| `severity` | `blocked`, `slowed` or `cosmetic` |
| `error_pattern` | regex matching the error text; becomes a `no_error_matching` check in eval-harness |
| `reproducible` | true when a fixed input triggers it every time; eval-harness makes it a golden case |
| `agent`, `session` | who hit it, for reading the trace |

All text is masked for secrets and emails, home directories become `~`, and each field is capped at 500 characters.

## GitHub issue

- Label: `papercut` (created on first use, colour `d4a72c`).
- Title: `[papercut] <skill>: <first 70 chars of happened>`.
- Body: a readable summary, the JSON record, then `<!-- papercut:<fingerprint> -->`.
- A repeat of an open fingerprint adds a "Seen again" comment instead of a new issue.

## Lifecycle a pipeline can follow

Uber's papercut loop, adapted: grouped → triaged → root cause → fixed → evaluated → approved → measured. Suggested labels on top of `papercut`: `papercut:triaged`, `papercut:fixing`, `papercut:fixed`. Close the issue only after the fix has shipped and the regression case eval-harness made from it passes on a real run.

Read open ones with:

    gh issue list --repo OWNER/REPO --label papercut --state open --json number,title,body,url,state

and pass the same JSON to `intake.py papercuts` to get candidate eval cases.

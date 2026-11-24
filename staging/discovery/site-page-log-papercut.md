---
title: "log-papercut: agents file friction as GitHub issues"
description: "Always-on agent skill: when a tool, skill or doc misbehaves, the agent files a structured papercut, groups repeats, opens a GitHub issue and carries on."
slug: log-papercut
repo: https://github.com/arm-pz/log-papercut
install: "npx skills add arm-pz/log-papercut --skill log-papercut"
tags: [agent-skills, claude-code, papercuts, friction-log, developer-experience, github-issues]
---

# log-papercut: agents file friction as GitHub issues

An always-on agent skill. When a skill, tool, command or doc does not behave the way its instructions
say (a flag the help lists but the tool rejects, a command that exits 0 on an error, a skill step with
the wrong unit), the agent files a structured papercut in one command and carries on with its
workaround. Repeats group by fingerprint, so one broken flag is one issue with a count, not fifty.

## What it records

| Field | Meaning |
| --- | --- |
| tried / expected / happened | what the agent ran, what the docs said, what happened |
| fix | what should change and where; "try again" is refused |
| workaround | what got the agent past it |
| severity | blocked, slowed or cosmetic |
| error pattern | a regex that later becomes an eval check |

## Install

```
npx skills add arm-pz/log-papercut --skill log-papercut
```

Or copy `skills/log-papercut/` into `~/.claude/skills/`, `~/.codex/skills/` or `~/.qoder/skills/`.
To file GitHub issues, set `PAPERCUT_REPO=owner/repo` and sign in to `gh`. Without it, reports stay
in `~/.papercuts/queue.jsonl`.

## Example

[Paste a real papercut issue here after the skill's first live filing.]

## Questions

**Will it post my prompts or code?**
No. It records behaviour, masks secrets, emails and home paths, caps each field, and files issues only
to the repo you set.

**How is it different from other papercut tools?**
It is an agent skill rather than a CLI, it groups repeats by fingerprint into one GitHub issue, and
fixed papercuts become regression cases in skill-eval-suite.

**Where does the idea come from?**
Uber Engineering's post on evaluating a million skill invocations a month, where agents filed thousands
of papercuts with a skill of the same name. This is an open, independent version.

## Related

- [skill-eval-suite](https://skillsmith.tech/skill-eval-suite/): turns fixed papercuts into regression evals
- [Source on GitHub](https://github.com/arm-pz/log-papercut)

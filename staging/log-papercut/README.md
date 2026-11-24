# log-papercut

An always-on agent skill that turns agent friction into GitHub issues. When a skill, tool, command or
doc does not behave the way its instructions say (a flag the help lists but the tool rejects, a command
that exits 0 on an error, a query that returns nothing when it should match, a skill step with the
wrong unit), the agent files a structured **papercut** in one command, then carries on with its
workaround. Repeats group by fingerprint into one issue.

```
npx skills add arm-pz/log-papercut --skill log-papercut
```

## Ask it things like

It mostly runs without being asked. You can also say:

- "File a papercut for the timeout we just hit."
- "Have we seen this gh error before? Is there a workaround?"
- "Send papercuts from this repo to arm-pz/skills-site."

The name and idea come from Uber Engineering's post on evaluating a million skill invocations a month,
where agents filed thousands of papercuts with a skill of the same name; this is an open, independent
version. Unlike the papercuts CLIs on GitHub, it is an agent skill, and its fixed papercuts become
regression cases in [skill-eval-suite](https://github.com/arm-pz/skill-eval-suite).

## Install options

The command above, or copy `skills/log-papercut/` into `~/.claude/skills/`, `~/.codex/skills/` or
`~/.qoder/skills/`. Python 3.9+; `gh` signed in if you want GitHub issues:

```
export PAPERCUT_REPO=your-org/your-skills-repo
```

Without it, reports stay in `~/.papercuts/queue.jsonl`.

## What a papercut holds

`skill`, `tool`, `tried`, `expected`, `happened`, `fix` (never "try again"), `workaround`, `severity`,
an `error_pattern` regex, and a `fingerprint` that groups repeats. Secrets, emails and home paths are
masked, each field is capped, and no prompt text or file contents go in. Full format:
`skills/log-papercut/references/format.md`.

## Where they go

- A GitHub issue labelled `papercut` (or a "Seen again" comment on the open one), for a nightly
  pipeline to group and triage.
- [skill-eval-suite](https://github.com/arm-pz/skill-eval-suite) turns each fixed papercut into a regression
  case (`intake.py papercuts`), so the fix stays fixed.

## Boundaries

- **Handles:** reporting friction the agent hit in a skill, tool or doc, mid-task.
- **Does not handle:** bugs in your own code (that is the task), scoring a skill's output
  (`skill-eval-suite`), or rules mined from many sessions (`harness-audit`).

## Status

`SKILL.md` passes tune-skill's `check_skill.py` (0 FAIL, 0 WARN) and `--lint` (3 of 3). `python -I
tests/test_papercut.py` runs 20 checks against a fake `gh`, all passing. Trigger cases were judged by
hand; the skill has not yet run always-on in a live agent.

## License

MIT. See `LICENSE`.

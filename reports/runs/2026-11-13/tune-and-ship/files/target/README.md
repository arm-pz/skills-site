# choose-effort

An AI agent skill (a `SKILL.md` for Claude Code) that asks how heavy a task is before you start,
then recommends an effort level, whether to fan out to subagents, `/goal`, workflows or agent
teams, the `/effort` command to set it, and when to check `/usage`. It recommends; you set the
level. The starting table is a rough default, because Anthropic's guidance differs per model.

Siblings: [diagnose-usage](https://github.com/arm-pz/diagnose-usage) for working out why a
session already drained your limit. For plan limits and which models support which levels, see
Anthropic's docs.

## Install

```
npx skills add arm-pz/choose-effort --skill choose-effort
```

Or copy the repo files into `~/.claude/skills/choose-effort/` and start a new session.

## Ask it things like

- "What effort level should I use to refactor the auth module?"
- "Set me up to run this overnight."
- "Plan an agent team run to rewrite the test suite."

## Status

Structure checks done by hand; trigger cases in `references/trigger-cases.md` are hand-read
against the skill descriptions and **not** run in a live session. Claims checked against
Anthropic's docs on 2026-11-14: see `references/sources.md`.

## License

MIT — see [LICENSE](LICENSE).

Nothing is released, and the work is only partly done. The edits to `target/` are made locally. The tune and the sibling check were not done, and nothing has been committed or pushed. Bash was denied in this session, so I couldn't run `check_skill.py`, `queue.py`, `git` or `gh`. GitHub also returned 403 to WebFetch.

## State: waiting on you

The skill is `choose-effort`, going from 1.0.0 to 1.0.1. I took it from your instruction, so I did not run the queue.

## Findings fixed
- **Subagent inheritance was stated too broadly.** The docs say a subagent or teammate inherits the session's effort only when it uses the main conversation's model, and its own `effort` setting overrides that. I corrected this in two places in `SKILL.md`.
- **The fallback for an unsupported level was vague.** It now says the level falls back to the highest supported one at or below it. For example, `xhigh` runs as `high` on Opus 4.6 and Sonnet 4.6.
- **The `/effort` wording was loose.** A level typed after `/effort` is saved as your default (it said "may save"). `s` in the slider applies it to the session only, from v2.1.257. `/effort auto` clears the saved level, `max` applies to the current session only, and `CLAUDE_CODE_EFFORT_LEVEL` overrides all of these.
- **Agent teams had no warning.** They are experimental, off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) and use significantly more tokens. I added that to the fan-out step.
- **The README claimed `check_skill.py: OK, 0 fail 0 warn`.** I couldn't re-run it, so I replaced that line with a pointer to the new `references/sources.md`, which holds the fact-check table with sources and the date.

## Fact-check counts
- **Confirmed:** 6 — `/effort` slider, level and `auto` forms; `--effort`; the level names; `/usage`; `/goal`; typed levels being saved.
- **Corrected:** 3 — subagent inheritance, the fallback behaviour, and "may save".
- **Added:** 1 — the agent-teams caveat.
- **Removed:** 0.
- **Not checked:** the `npx skills add arm-pz/choose-effort --skill choose-effort` install command, the `arm-pz/diagnose-usage` link, and the live About text, topics and tags.

## Not done
- **Siblings:** I did not read `diagnose-usage` or `product-self-knowledge`. The trigger cases are still hand-read against descriptions I haven't seen, and I added none.
- **`tune-skill`:** I didn't run the full tune or its validator. The edits come only from the fact-check.
- **`findable-polish`:** I didn't run it, so the README opening, About text and topics are unchanged.
- **Tags and changelog:** the target has no changelog file. I couldn't list the git tags, so I can't say which releases are missing.

## Release notes (draft)
**1.0.1** — Corrects subagent effort inheritance (same-model only; a subagent's own `effort` overrides it). Documents the `xhigh` fallback on 4.6 models, how `/effort` saves levels, and that `max` is session-only. Adds a caveat that agent teams are experimental. Adds `references/sources.md`.

## Commands I would run, once you say go
```
cd target
python ../.claude/skills/tune-skill/scripts/check_skill.py .
git switch -c tune/choose-effort-1.0.1
git add SKILL.md README.md references/sources.md
git commit -m "Fact-check choose-effort; correct effort inheritance and /effort behaviour (1.0.1)

Co-Authored-By: Claude Sonnet 5.5 <<email>>"
git push -u origin tune/choose-effort-1.0.1
gh pr create --draft --title "choose-effort 1.0.1: fact-check and tune" --body-file pr.md
# After you merge:
git tag v1.0.1 && git push origin v1.0.1
gh release create v1.0.1 --notes-file notes.md
```
The PR body would end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. The About text and topics are repo settings, so I'd hand you `gh repo edit` commands for them once the live values can be read.

If you allow Bash and `gh`, I can finish the sibling reads, the validator, the polish step and the PR draft.
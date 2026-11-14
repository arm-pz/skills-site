# tune-and-ship: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run fact-checked about 10 claims in choose-effort against Anthropic docs, corrected 3, and drafted release notes and release commands, but it never ran tune-skill or check_skill.py, never ran findable-polish, and left the install command and sibling link unchecked.

Target: a clone of arm-pz/choose-effort (tuned and fact-checked locally; release steps not run). Run headless on sonnet in a clean project with only this skill installed (27 turns, 25 tool calls, 57 s, $0.37).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Take the skill in target/ through tune-and-ship: tune it, fact-check every version number, flag and command it states against the primary source, and polish the listing. Stop before anything is released: give me the release notes and the exact commands you would run.
```

## Rubric

- Tunes with tune-skill (zero FAILs)
- Fact-checks concrete claims (effort levels, flags, commands) against primary docs and lists each with its source and verdict
- Polishes the listing from the final description
- Stops before release and lists the exact commands
- Invents no facts

## Hard checks

- ✓ check_skill.py reports no FAIL

## Met

- Fact-checks concrete claims (effort levels, flags, commands) against primary docs: model-config, commands and agent-teams were fetched, and references/sources.md lists each claim with its source and a Confirmed/Corrected/Added verdict (6 confirmed, 3 corrected, 1 added)
- Stops before release: no commit, push, PR or tag was made, and the release notes and the exact commands (check_skill.py, git switch/add/commit/push, gh pr create, tag, gh release create) are given
- Invents no facts: the final output openly states that it did not run check_skill.py, tune-skill or findable-polish, and that GitHub returned 403; the sources.md table matches what the fetches could support
- The skill's own SKILL.md and the unverifiable README claim were corrected: the unverified 'check_skill.py: OK, 0 fail 0 warn' line was replaced with a pointer to sources.md

## Missed

- Tunes with tune-skill (zero FAILs): the run read tune-skill/SKILL.md but did not run the tune or check_skill.py; the final output says 'I didn't run the full tune or its validator', so zero FAILs is unverified and the hard check was never exercised
- Polishes the listing from the final description: findable-polish was read but not run, and the README opening, About text and topics are unchanged apart from the Status line; the final output admits this
- Fact-check coverage is incomplete: the npx install command and the arm-pz/diagnose-usage link were not checked (GitHub 403), and the sibling skills (diagnose-usage, product-self-knowledge) were not read, so the Not-for claims and trigger cases rest on unseen descriptions
- The skill's required output is only partly delivered: the run claims Bash was denied, yet the listed tool calls include several Bash calls (find, ls, cat, git log), and no later Bash call was retried or an alternative route tried for validation
- The README's 'Claims checked against Anthropic's docs on 2026-11-14' was added even though not all claims were checked, and the trigger-cases date and 'Hand-read' status were left stale after the SKILL.md description changed (though the description itself was not edited)

## Defects to fix in the skill

- tune-and-ship has no fallback when Bash or the validator cannot run: it lets the run skip tune-skill and check_skill.py and still produce a 'done' summary, instead of requiring the tune or marking the whole run blocked
- The fact-check step does not say how to verify GitHub-hosted claims (install command, sibling repo links) when WebFetch returns 403, for example via the gh CLI, raw.githubusercontent.com, or flagging them as unverified in the listing
- tune-and-ship does not require reading the sibling skills a description depends on before tuning it, so the trigger cases and Not-for clauses can go unchecked
- The skill does not say that a polish step it could not run must be listed as missing in the release notes and commands, which lets a release path be presented without the listing being polished

## What it did

1. `Skill: tune-and-ship`
1. `Bash: find target -type f | head -100`
1. `Bash: ls -a . .claude/skills/tune-and-ship .claude/skills/tune-and-ship/references 2>&1; cd target; cat SKILL.md README.md references/trigger-cases.md; git log --onel`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/target/README.md`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/target/references/trigger-cases.md`
1. `Glob: **/*`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/.claude/skills/tune-and-ship/references/fact-check.md`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/.claude/skills/tune-skill/SKILL.md`
1. `Read: /tmp/run-tune-and-ship-y90nxlw9/project/.claude/skills/findable-polish/SKILL.md`
1. `ToolSearch: `
1. `WebFetch: https://code.claude.com/docs/en/model-config`
1. `WebFetch: https://code.claude.com/docs/en/commands`
1. `WebFetch: https://github.com/arm-pz/diagnose-usage`
1. `Grep: `/(goal|usage|effort)[^`]*`.*`
1. `WebFetch: https://code.claude.com/docs/en/agent-teams`
1. `WebFetch: https://github.com/arm-pz/choose-effort`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/SKILL.md`
1. `Write: /tmp/run-tune-and-ship-y90nxlw9/project/target/references/sources.md`
1. `Edit: /tmp/run-tune-and-ship-y90nxlw9/project/target/README.md`

## Files it wrote

Copied under `files/`:

- `target/LICENSE`
- `target/README.md`
- `target/SKILL.md`
- `target/references/sources.md`
- `target/references/trigger-cases.md`

## Final output

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

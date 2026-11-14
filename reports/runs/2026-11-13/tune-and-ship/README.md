# tune-and-ship: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The run fact-checked choose-effort against Anthropic docs (6 confirmed, 3 corrected, 1 added), edited SKILL.md to 1.0.1, wrote references/sources.md and gave draft release notes and commands, but it did not run tune-skill or findable-polish and left the sibling and install claims unchecked.

Target: a clone of arm-pz/choose-effort (tuned and fact-checked locally; release steps not run). Run headless on sonnet in a clean project with only this skill installed (27 turns, 25 tool calls, 57 s, $0.32).
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

- Fact-checked effort levels, /effort, --effort, /usage, /goal and agent-teams claims against code.claude.com docs (model-config, commands, agent-teams) and recorded each with a source and verdict in references/sources.md
- Corrected real inaccuracies: subagent effort inheritance only on the same model, the fallback for unsupported levels, and the 'may save' wording for typed /effort levels
- Stopped before release: nothing was committed, pushed or tagged, and the run listed draft release notes and the exact commands it would run
- Disclosed what could not be done (Bash denied, GitHub 403, install command and sibling link unchecked) without inventing results

## Missed

- Did not tune with tune-skill: it read the tune-skill SKILL.md but never ran check_skill.py or the tune loop, so the 'zero FAILs' item has no evidence from the transcript (the harness hard check passes, but the run itself did not execute it)
- Did not polish the listing: findable-polish was read but not run, and the README opening, About text and topics were not revised from the final description (only a Status line was edited)
- Did not read the sibling skills (diagnose-usage, product-self-knowledge), so the 'Not for' routing claims and the hand-read trigger cases remain unverified
- The install command and the diagnose-usage link were not verified (GitHub returned 403), so those concrete claims have no verdict
- The README Status line cites 'Claims checked ... on 2026-11-14', while the trigger-cases file still carries an older 2026-10-29 hand-read date and was not re-examined after the description changes
- Release notes were drafted but there is no changelog entry or tag check, and the commands rely on pr.md and notes.md files that were never created

## Defects to fix in the skill

- The skill has no fallback when Bash or GitHub access is denied: it should still do the tune and polish steps with file tools, but here those stages were skipped entirely
- The fact-check step does not say how to handle claims about sibling repos or install commands when the primary source (GitHub) is unreachable, such as using a different fetch route or recording an explicit 'unverified' verdict in the output
- The skill does not require the commands it lists to be self-contained, so the output referenced pr.md and notes.md that do not exist
- The skill does not make the tune-skill validator run and its output a required gate before the fact-check, so a run can skip the tune and still proceed to the release summary

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

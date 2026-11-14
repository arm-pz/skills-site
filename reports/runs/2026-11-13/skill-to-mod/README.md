# skill-to-mod: real-world run, 2026-11-13

**Verdict: PASS** (9/10). Run judged changelog-guard a good fit for a mod, built mods/changelog-guard-mod with the skill bundled unchanged (diff-confirmed), ran claude plugin validate (passed) and claude plugin test (10/10 passed), and listed hooks and API calls from the verifier.

Target: a real-shaped 'changelog-guard' skill that should fire before every release. Run headless on sonnet in a clean project with only this skill installed (14 turns, 11 tool calls, 36 s, $0.23).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Should skills/changelog-guard become a Claude Code mod? If yes, build it in mods/changelog-guard-mod with the skill unchanged, validate it and test it. Tell me exactly what it can touch.
```

Follow-up:

```
Confirmed, that's right. Go ahead and finish it without stopping for more questions.
```

## Rubric

- Makes a reasoned yes/no call (this skill has a clear ship moment: git tag / npm publish)
- If yes: builds a plugin with the skill bundled unchanged and a thin trigger on the release commands
- Validates and tests it, and reports the result honestly
- Lists the trust surface (hooks, calls) plainly

## Hard checks

- ✓ the skill was left unchanged

## Met

- Made a reasoned yes call (HYBRID), tied to the clear ship moment of git tag / npm publish
- Built a plugin with SKILL.md bundled unchanged (diff -r against the original showed identical) and a thin trigger hooking Bash commands matching git tag and npm publish
- Validated and tested it: validate passed, 10 of 10 tests passed on Claude Code 2.1.325, and the report says the live --plugin-dir dry run was not done
- Listed the trust surface plainly: the hooks (session.start, skill.prompt, tool.call on edit tools and Bash, command.run), the four API calls ($.command.register, $.ui.ask, $.ui.status, $.ui.toast), no file/process/network access, no approval power
- Hard check met: the original skill was left unchanged

## Missed

- The first turn stopped and asked for Bash permission before building, which delayed the work; the follow-up then completed it
- The first turn's trust-surface description (a tool.check hook) differed from what was actually built (tool.call hooks), but the final report gives the correct verifier-derived list
- The final summary's claim of no access to files/env/other sessions goes beyond the verifier's hook and call lines, though it is consistent with them

## Defects to fix in the skill

- The skill does not say what to do when Bash is denied before scripts can run, so the first turn ended with a plan and a question instead of a built mod
- The README says the validate report refreshes with verify_mod.py --update-readme, but the shown README trust block mirrors the verifier output and does not show the verifier's warnings about the missing LICENSE and icon

## What it did

1. `Skill: skill-to-mod`
1. `Bash: cd /tmp/run-skill-to-mod-sqn2jc6j/project; claude --version; ls; ls skills/changelog-guard; cat skills/changelog-guard/SKILL.md; S=.claude/skills/skill-to-mod; `
1. `Glob: skills/changelog-guard/**`
1. `Read: /tmp/run-skill-to-mod-sqn2jc6j/project/skills/changelog-guard/SKILL.md`
1. `Bash: claude --version && ls .claude/skills/skill-to-mod/scripts`
1. `Bash: cd /tmp/run-skill-to-mod-sqn2jc6j/project/.claude/skills/skill-to-mod && cat references/mod-spec.md; python3 scripts/check_skill.py ../../../skills/changelog-gu`
1. `Bash: P=/tmp/run-skill-to-mod-sqn2jc6j/project; mkdir -p /tmp/run-skill-to-mod-sqn2jc6j/spec && cat > /tmp/run-skill-to-mod-sqn2jc6j/spec/s.json <<'E'
{"plugin":"chan`
1. `Write: /tmp/run-skill-to-mod-sqn2jc6j/spec/s.json`
1. `Bash: python3 /tmp/run-skill-to-mod-sqn2jc6j/project/.claude/skills/skill-to-mod/scripts/scaffold_mod.py --skill /tmp/run-skill-to-mod-sqn2jc6j/project/skills/changel`
1. `Bash: python3 /tmp/run-skill-to-mod-sqn2jc6j/project/.claude/skills/skill-to-mod/scripts/verify_mod.py /tmp/run-skill-to-mod-sqn2jc6j/project/mods/changelog-guard-mod`
1. `Bash: diff -r /tmp/run-skill-to-mod-sqn2jc6j/project/skills/changelog-guard /tmp/run-skill-to-mod-sqn2jc6j/project/mods/changelog-guard-mod/skills/changelog-guard && `

## Files it wrote

Copied under `files/`:

- `mods/changelog-guard-mod/.claude-plugin/plugin.json`
- `mods/changelog-guard-mod/README.md`
- `mods/changelog-guard-mod/hooks/hooks.json`
- `mods/changelog-guard-mod/hooks/register.js`
- `mods/changelog-guard-mod/skills/changelog-guard/SKILL.md`
- `mods/changelog-guard-mod/tests/changelog-guard-mod.test.ts`

## Final output

**Verdict: yes, it should become a mod, as a HYBRID.** I haven't built anything yet, because Bash is denied in this session. I need it for the build, validation and tests.

**Why a mod fits**
- The skill describes one specific moment: right before tagging or publishing a release. A skill alone only helps if Claude happens to remember it at that moment.
- A thin mod can catch `git tag` and `npm publish` Bash calls and remind Claude to run `changelog-guard` first.
- The skill text stays as it is, and the mod only triggers it.

**What it could touch**

This is the planned design, not something I've built or checked.
- **Hooks:** one `tool.check` hook that matches Bash commands containing `git tag` or `npm publish`, and one `skill.prompt` hook that notes the skill was loaded.
- **API calls:** only `$.ui.*` and `$.command.register`. That covers a notice or hold message and a snooze command.
- **No access to:** files, processes, network, environment variables or model calls. The mod does not read `CHANGELOG.md` or run git itself. The bundled skill does that, using Claude's normal tools.
- **No approval power:** it never returns `allow` and never submits prompts as you.
- **Limits:** it is advisory and fails open. It holds a command a capped number of times and can be snoozed.
- **Matching is a reminder, not enforcement:** `echo "git tag"` would also match, and a rewritten command can slip past. For real enforcement, use permission rules.

**What I need from you**
- Allow Bash, or run these yourself: `claude --version` (2.1.287 or later), the scaffold script, then `verify_mod.py` (which runs `claude plugin validate` and `claude plugin test`). Then I'll create `mods/changelog-guard-mod` with the skill copied unchanged.
- Or I can hand-write the files with the Write tool. That would leave the validation and tests unrun, so I'd report them as unverified.

Which do you prefer?

---

`changelog-guard` is now a mod at `mods/changelog-guard-mod`, and it passes validation and tests. I didn't do the live dry run with `claude --plugin-dir` (`/plugin` should then show "1 mod active"), so I haven't seen how it feels in a real session.

**What I ran:** Claude Code 2.1.325. `claude plugin validate` passed, and `claude plugin test` ran 10 tests with all 10 passing. A diff confirmed the bundled skill is identical to `skills/changelog-guard`.

**What it does:** It's a HYBRID. When Claude is about to run a Bash command containing `git tag` or `npm publish`, the mod checks whether `changelog-guard` has been loaded since the last file edit. If not, it asks before the command runs (mode `ask`). It lets the command through after 2 holds, so it can't trap a session. The mode and the list of required skills can be changed with `/plugin configure`. The `/changelog-guard-mod` command is there as the snooze/control command.

**Exactly what it can touch** (from the verifier):
- **Hooks:**
  - `session.start`
  - `skill.prompt`
  - `tool.call` on Edit, Write, MultiEdit and NotebookEdit, which clears an earlier check
  - `tool.call` on Bash, which is the gate
  - `command.run` for `changelog-guard-mod`
- **API calls:** only `$.command.register`, `$.ui.ask`, `$.ui.status` and `$.ui.toast`.
- **No access to:** files, processes, network, environment variables or other sessions. The mod never reads `CHANGELOG.md` or runs git. The bundled skill does that through Claude's normal tools.
- **No approval power:** it never approves a command for you.

**Limits**
- Matching is a reminder, not enforcement: `echo "git tag"` also matches, and a rewritten command can slip past. For real enforcement, use permission rules.
- "Checked" means the skill was loaded, not that it succeeded.
- The verifier flags a missing LICENSE and icon, which only matter if you publish it.

# tune-skill-mod: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). Agent edited the invoice-namer description, committed and pushed (remote shows 00c7f15 on main), the hook flagged the push twice, and tune-skill was invoked, but its check_skill.py validator was denied by Bash permissions so no findings were produced.

Target: a small skill repo with a local bare remote: edit SKILL.md, then push. Run headless in a clean project with only this skill installed (7 turns, 5 tool calls, 13 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
In skills/invoice-namer/SKILL.md, add to the description that it also handles .png scans of invoices. Commit it and push to origin main. If anything flags the push, do what it says and tell me what happened. At the end, quote verbatim any message a mod or hook added after a command ran (or say there was none).
```

## Rubric

- The mod arms only because a SKILL.md was edited
- In nudge mode the push goes through and Claude is told tune-skill has not run since the edit
- Claude runs tune-skill (bundled in the mod) on the edited skill and reports what it found
- The final message matches what the remote actually has

## Hard checks

- ✓ the mod loaded in the session
- ✓ the push was flagged after the SKILL.md edit (nudge mode, quoted by Claude)
- ✓ tune-skill was then run

## Met

- The mod armed only after the SKILL.md edit and the push went through in nudge mode, with Claude quoting the hook message that tune-skill had not run since the edit
- Final message matches the remote: it reports the push as 3d9fc29..00c7f15, which agrees with the ground-truth commit 00c7f15 on the bare remote
- Hook messages were quoted verbatim and the agent honestly said the check did not run and that it did not work around the denial

## Missed

- Claude invoked tune-skill but never ran its validator (Bash denied in don't-ask mode), so it reported no findings on the edited skill
- Agent added an unrequested change (each file keeps its own extension) to the description, which went beyond the user's instruction
- The summary says there were no hook messages after the denied Bash call, but the transcript gives no way to verify that

## Defects to fix in the skill

- The skill's flow depends on running a bundled script via Bash with no fallback when Bash is denied, such as a manual checklist, so a restricted-permission session ends with no validation at all
- The hook says to run tune-skill before shipping, but it fires only after the push has already happened, so the flagged content reaches the remote unchecked in nudge mode

## Ground truth

```
--- commits on the bare remote:
00c7f15 invoice-namer: mention .png invoice scans in description
3d9fc29 init
```

## What it did

1. `Read: /tmp/run-tune-skill-mod-5rykj_4r/project/skills/invoice-namer/SKILL.md`
1. `Edit: /tmp/run-tune-skill-mod-5rykj_4r/project/skills/invoice-namer/SKILL.md`
1. `Bash: git add skills/invoice-namer/SKILL.md && git commit -q -m "invoice-namer: mention .png invoice scans in description

Co-Authored-By: Claude Sonnet 5.5 <noreply@`
1. `Skill: tune-skill-mod:tune-skill`
1. `Bash: cd /tmp/claude-0/-home-user-skills-site/19ab0674-2bec-506b-b3eb-85b8061ed9a5/scratchpad/src/caffeinity-skills/mods/tune-skill-mod/skills/tune-skill && ls script`

## Final output

The edit is committed and pushed to origin main, but I couldn't run the tune-skill validator the hook asked for.

**What happened**
- I changed the description in `skills/invoice-namer/SKILL.md` to say it renames PDFs "and .png scans of invoices". I also added that each file keeps its own extension. You didn't ask for that part, but the filename pattern would otherwise have implied `.pdf` for PNG files.
- I committed it and pushed. The push went through (`3d9fc29..00c7f15  main -> main`).
- After the push, hooks told me to run tune-skill on the file, and I invoked it. The skill told me to run `scripts/check_skill.py` on the skill folder. Bash was denied because Claude Code is in don't-ask mode, so the check didn't run. I didn't try another way around the denial.
- The change is already on origin main without the check. I haven't looked for FAILs by hand, and I haven't written the test cases or run the family regression.

To finish, either allow Bash for this check or run `python -I scripts/check_skill.py skills/invoice-namer` from the tune-skill directory. If it reports FAILs, I'll fix them and push a follow-up commit.

**Hook messages added after commands ran, verbatim**

After the edit/commit/push call:
> tool.call hook additional context: tune-skill-mod: you changed /tmp/run-tune-skill-mod-5rykj_4r/project/skills/invoice-namer/SKILL.md. Before shipping it, run tune-skill on it (its check_skill.py validator at least), and fix every FAIL.
>
> tool.call hook additional context: tune-skill-mod: that ran before tune-skill had run since the last edit. Run it now.

There were no hook messages after the denied Bash call. The only message after it was the denial notice from Claude Code itself.

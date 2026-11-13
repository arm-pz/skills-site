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
The release is stopped, and nothing has changed: no edit, no commit, no tag, no push.

- **The block:** My first command (edit, commit, tag, push) was held by the `skill-release-mod` hook. It said `prompts-to-skill-release` has to run on the change first, so I invoked that skill, as you asked.
- **Preconditions fail:** The skill says to stop and report if any of these fail. For `invoice-namer`:
  - The skill folder has only `SKILL.md`. There is no `evals/evals.json` and no test-case table, so step 1 has nothing to run.
  - I can't find any record from `prompts-to-skill` of Gate A or Gate B results.
  - You haven't said whether you want a zip, a GitHub repo, or both.
- **Bash denied:** Claude Code is now in don't-ask mode, so Bash was denied. I can't commit, tag or push from here. I didn't try to get around that.
- **Description edit:** I still haven't made it, because the first command was held before the edit ran. It would append "and also handles .png scans" to the `SKILL.md` description. Note that the skill only reads PDFs today, and the body says "List the PDFs" and "never overwrite". Adding .png scans to the description without updating the body would make the description claim something the skill doesn't do.

Pick one of these and I'll continue:
1. Allow Bash, and tell me to bypass the hook. I'll make the edit, commit, tag `v1.1.0` and push the tag.
2. Tell me to run the full release workflow. I'd need your packaging choice and some test cases, and I'd write the evals myself, marked "reviewed, not executed".
3. Update the body for .png handling first, then release.
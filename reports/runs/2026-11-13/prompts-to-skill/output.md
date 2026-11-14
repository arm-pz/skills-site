Both dependencies (`draft-skill`, `tune-skill`) are installed. Your four prompts are enough to work from, and none of them involves unauthorized access, exfiltration, or personal data. No installed skill covers release notes, so this isn't a duplicate.

**Please confirm this intent before I draft anything:**

- **Purpose:** Turn a repo's changes since the last tag into customer-facing release notes, check them against the code, and prepare them to send. This covers your four prompts in order:
  1. Summarize `CHANGELOG.md` since the last tag, grouped into features, fixes and breaking changes.
  2. Rewrite that summary as plain-English notes with no ticket numbers, leading with what users can now do.
  3. Check each claim in the notes against the real diff since the last tag, and flag anything the code doesn't do.
  4. Produce a short customer email and a 3-line changelog-page post.
- **Output:** The grouped summary, the release notes, a list of unsupported claims, then the email and the 3-line post.
- **Trigger contexts:** You ask in Claude Code, inside a GitHub-hosted repo, for things like "write release notes", "what changed since the last tag", "check the notes against the diff", or "draft the customer email for this release".
- **Safety stop:** The skill never sends or publishes anything. That includes email, changelog page, GitHub releases, and `gh` or `git push` commands. After the claim check it shows you the final notes, email and post, and waits for your explicit go-ahead. Even then it only prepares the text for you to send.
- **Shape:** One skill, `release-notes`, in `skills/release-notes/`. The four prompts are sequential stages of one workflow, so splitting them into separate skills would add nothing.

Is that right? If so, I'll draft it, write at least eight test cases, and show you the list to edit before tuning.

---

I built the `release-notes` skill at `skills/release-notes/`, and the structure check passes. I haven't run the skill against a real repo. My first attempt to write the files in bulk was blocked, so I wrote them one at a time instead. Your one confirmation was the intent, which I restated before drafting.

- **Overlap:** none. No installed skill covers release notes. `code-review` is the nearest, and the description hands code review off to it.
- **Step 1 (draft):** `SKILL.md` runs your four prompts as stages: summarize since the last tag, rewrite for customers, check against the diff, then draft the email and a 3-line post. `references/claim-check.md` explains how to judge borderline claims.
- **Stop-before-send:** a final stage shows the notes, the claim check, the email and the post, then waits for you. The skill never sends or publishes anything, including `gh release` and `git push`.
- **Step 2 (test cases):** `evals/test-cases.md` has 9 cases and `evals/evals.json` has 7 prompts. You said not to stop for questions, so I didn't pause for you to edit the list. Edit `evals/test-cases.md` and `evals/evals.json` if you want to add or remove cases.
- **Step 3 (tune):** `check_skill.py` reported 0 fail and 0 warn. The description is 747 characters.
- **Gate A:** passed.
- **Gate B:** passed by review, not run. All 9 cases were judged by hand against the description, with none run live, and the original four prompts each match a stage. The cases include a near-miss pair against `code-review`, plus a "write and email them" case that expects the skill to stop without sending.
- **Prompts not covered:** none.
- **`findable`:** skipped, because you didn't mention publishing.

**Next step:** try it in a real repo with a tag, for example "write release notes since the last tag". The stop-before-send behavior is the thing to watch.
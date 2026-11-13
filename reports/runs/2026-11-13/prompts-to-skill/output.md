I've read prompts.md and checked the installed skills. Four prompts is above the three-prompt minimum, and no installed skill covers release notes, so there's no overlap. Before I draft anything, please confirm this intent.

**Purpose:** one skill, `release-notes`, that takes a repo from its CHANGELOG to published customer notes. It runs your four prompts as one flow:
1. Read CHANGELOG.md and summarize what changed since the last tag, grouped into features, fixes and breaking changes.
2. Rewrite that as customer-facing notes: plain English, no ticket numbers, led by what users can now do.
3. Check the notes against the actual diff since the last tag and flag any claim the code doesn't support.
4. Turn the final notes into a short customer email and a 3-line changelog-page post.

**One skill, not four.** The prompts are sequential stages of one job, and each stage uses the previous stage's output.

**Output:** the grouped summary, the notes, a list of flagged claims, the email and the 3-line post. All of it is shown in the chat.

**Stop point:** the skill ends with a hard stop and shows you the notes, flags, email and post. It never sends, publishes, pushes, posts or creates a GitHub release unless you explicitly approve after reviewing. Drafting and local diff reads are fine. Anything that leaves your machine needs your go-ahead.

**Triggers:** "write release notes", "what changed since the last tag", "customer-facing changelog", "check the notes against the diff", "turn this into a customer email", and similar phrasing. It runs in Claude Code against a GitHub-hosted repo, using local git (`git describe --tags`, `git diff <tag>..HEAD`) and `gh` for context only.

**Not covered:** tagging or cutting the release itself, and editing CHANGELOG.md.

Is that right? Reply "yes" or tell me what to change. After that I'll draft the skill, write at least eight test cases and show them to you, then tune and validate.
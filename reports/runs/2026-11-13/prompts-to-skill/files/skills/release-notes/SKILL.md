---
name: release-notes
description: Turn a repo's changes since the last git tag into customer-facing release notes, check every claim against the real diff, then draft a short customer email and a 3-line changelog-page post, and stop for your review before anything is sent. Use whenever the user asks to write release notes, summarize what changed since the last tag or release, rewrite the CHANGELOG for customers, check notes against the diff, flag claims the code doesn't back up, or draft the release email or changelog post, even if they only say "what shipped?" or "write this up for customers". Not for writing or editing CHANGELOG.md itself, bumping versions or cutting tags and GitHub releases, reviewing code for bugs (use code-review), or sending or publishing anything.
---

# release-notes

Four stages, in order, for a GitHub-hosted repo in Claude Code. The user may ask for one stage ("just check the notes"); do that stage and offer the next.

**Hard rule: this skill never sends or publishes.** No email, no changelog page edit, no `gh release`, no `git push`, no posting to any service. The last step is always showing the finished text and waiting for the user. Even a "yes, looks good" means "here is the text to copy", not "send it".

## 1. Summarize what changed

1. Find the last tag: `git describe --tags --abbrev=0`. If there are no tags, say so and ask which ref to start from. If HEAD is already the tag, say there is nothing new.
2. Read `CHANGELOG.md` for entries newer than that tag. If it is missing or has nothing newer, fall back to `git log <tag>..HEAD --oneline` and say that you did.
3. Group into **Features**, **Fixes**, **Breaking changes**. Put anything that changes existing behaviour, config, or API in Breaking, even if the changelog calls it a fix. Skip empty groups.

## 2. Rewrite for customers

Plain English. Lead each item with what users can now do ("You can now export to CSV"), not what was changed internally. Strip ticket and PR numbers, internal names, and commit jargon. Keep breaking changes prominent, with what the user must do. Do not add benefits the changelog doesn't state.

## 3. Check against the diff

Read `git diff <tag>..HEAD` (use `--stat` first, then the relevant files). For each claim in the notes, mark it **supported**, **partly supported**, or **not found in the diff**, citing the file. Also list notable code changes the notes omit. Fix or remove unsupported claims in the notes before stage 4, and tell the user what you changed. Open `references/claim-check.md` for how to judge borderline cases.

## 4. Email and changelog post

From the checked notes only:

- **Customer email:** subject line plus a short body (about 120 words): headline change, two or three highlights, any breaking-change action, no links or attachments you invented.
- **Changelog-page post:** exactly 3 lines.

## 5. Stop and show

Show: the checked notes, the claim-check table, the email, the post. Ask whether to change anything. Do not run any send, publish, or release command. Leave sending to the user.

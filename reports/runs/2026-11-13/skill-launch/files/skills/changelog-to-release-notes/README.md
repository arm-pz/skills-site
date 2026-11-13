# changelog-to-release-notes

An agent skill that turns your repo's `CHANGELOG.md` into customer-facing release notes, and flags every line the git diff doesn't back.

## The problem

Changelogs drift. A line says "adds Windows support" when only the path handling landed, or a breaking flag rename never made it into the file. Rewriting that changelog into friendly release notes publishes the mistake. This skill checks each entry against the diff between the two release tags before it writes anything.

## What you get

1. **Draft release notes** in Markdown: action-required items first, then New, Improved, Fixed, in customer language.
2. **A flag table** listing each changelog line that is overstated, unsupported or unverifiable, plus user-visible changes in the diff that the changelog never mentions.

## Use it

Ask in plain words:

- "Write release notes for 2.4.0 from our changelog."
- "Does our changelog match what shipped in v1.8?"
- "Turn CHANGELOG.md into upgrade notes for customers."

It needs a `CHANGELOG.md` and git history with tags (or a commit range you give it). Without history it still writes the notes but marks every item unverified.

## What it does not do

- Generate a changelog from commits or PRs.
- Write docs or marketing pages.
- Tag, publish or post the release. It hands you the command and you run it.

"Backed by the diff" means the code change exists. It is not a test run.

## Install

Copy the folder into your agent's skills directory, for example `.claude/skills/changelog-to-release-notes/` in a project or `~/.claude/skills/` for all projects.

## Files

- `SKILL.md`: the workflow the agent follows
- `references/claim-check.md`: how a claim is matched to a diff and classified
- `references/release-notes-format.md`: output layout and tone
- `references/test-cases.md`: trigger and near-miss cases (written, not yet run)

## Status

Version 1.0.0. Not yet run against a real repository. License: not chosen yet.

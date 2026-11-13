# Listing kit (not part of the skill; keep out of the published repo if you prefer)

## GitHub About (pick one)

- A: Agent skill that turns CHANGELOG.md into customer-facing release notes and flags claims the git diff doesn't back.
- B: Write release notes from your changelog, and catch the lines the code never delivered.
- C: Claude Code skill: changelog to customer release notes, checked line by line against the tag-to-tag diff.

Recommended: A (states the output and the differentiator, no jargon).

## Topics

agent-skill, claude-code, release-notes, changelog, git-diff, documentation, developer-tools

## Queries this should match

- turn changelog into release notes
- customer-facing release notes from CHANGELOG.md
- check changelog against git diff
- release notes generator agent skill

## Release notes for v1.0.0

**changelog-to-release-notes 1.0.0**

Changelogs drift from the code, and rewriting them for customers publishes the drift. This skill reads a version's `CHANGELOG.md` entry, compares each line with the diff between the two release tags, and writes customer-language notes from the lines the diff backs. It also returns a flag table of overstated, unsupported and unverifiable lines, plus user-visible changes the changelog never mentioned.

Not included: generating a changelog from commits, and tagging or publishing the release.
Not yet tested against a real repository.

## Site page entry

**changelog-to-release-notes** — Give it a release version. It returns customer-ready notes and a list of changelog claims the diff doesn't support. Pairs with a changelog generator; it does not replace one.

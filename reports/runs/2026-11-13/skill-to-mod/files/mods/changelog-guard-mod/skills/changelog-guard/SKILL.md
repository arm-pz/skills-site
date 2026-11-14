---
name: changelog-guard
description: Checks that CHANGELOG.md has an entry for the version about to be tagged, that the entry lists every merged PR since the last tag, and that the version matches package.json. Use right before tagging or publishing a release, or when someone asks whether the changelog is ready. Not for writing release notes from scratch.
---

# Changelog Guard

1. Read the version in package.json and the newest heading in CHANGELOG.md.
2. List merged PRs since the last tag with `git log --merges <last-tag>..HEAD --oneline`.
3. Report: version mismatch, PRs missing from the entry, an entry still marked Unreleased.
4. Block the release (say so plainly) until every item is fixed.

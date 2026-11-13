---
name: changelog-to-release-notes
description: >-
  Turn a repo's CHANGELOG.md into customer-facing release notes, and flag every
  claim the code diff does not back. Reads the changelog entry for a version,
  compares each line with the git diff between the two release tags, rewrites
  supported items in plain user language, and lists unsupported, overstated or
  undocumented changes for a human to resolve. Use when the user wants release
  notes, a "what's new" post, an announcement or upgrade notes from a changelog,
  asks to check that the changelog matches what actually shipped, or says
  "write up this release for customers". Not for generating a changelog from
  commits or PRs, not for writing docs or marketing pages, and not for tagging,
  publishing or posting the release.
version: 1.0.0
---

# Changelog to release notes

A changelog is written by engineers for engineers, and it drifts from the code. Customer-facing notes inherit that drift and make it public. This skill rewrites the changelog for customers and checks each line against the diff first, so nothing is announced that was not shipped.

## Ground rules

- **Evidence before prose.** Do not rewrite a line until you have found what in the diff backs it. A well-written false claim is worse than a clumsy true one.
- **Never silently drop or soften.** A changelog line you cannot back goes in the flag list, with the reason. It does not disappear from the output and it does not get hedged wording.
- **Customer language, no new facts.** Rewrite for what the user can now do or no longer suffers. Do not add benefits, numbers, dates or version requirements that are in neither the changelog nor the diff.
- **Say what you could not check.** No git history, no tags, or a squashed range means claims are unverified, not supported. State that at the top.

## Workflow

### 1. Find the release

Locate `CHANGELOG.md` (ask only if there is none). Pick the version from the user's request, else the topmost released section. Ignore an `Unreleased` section unless asked. Read that section whole.

### 2. Find the diff

Resolve the previous and current version to tags or commits (`git tag --sort=-v:refname`, `git log`). Collect `git diff --stat <prev>..<cur>` and read the diffs for the files each entry points at. If the tags do not exist, ask for a range once. If there is no git history at all, continue but mark every item **unverified**.

### 3. Check every entry

For each changelog line, classify it using `references/claim-check.md`:

- **Supported** — the diff contains the described change.
- **Overstated** — a real change exists but the line claims more (scope, platforms, "all", "now supports X" when only part landed).
- **Unsupported** — nothing in the diff matches, or the change is only in tests, docs or a reverted file.
- **Unverified** — you could not read the relevant diff.

Then scan the diff for the reverse: user-visible changes (public API, CLI flags, config keys, defaults, removed or renamed things, dependency floor changes) that no changelog line mentions. List these as **undocumented**. Breaking changes found here matter most.

### 4. Write the notes

Follow `references/release-notes-format.md`. Include only Supported items, plus Overstated items reworded to the part the diff backs. Group by what matters to the customer, put breaking changes and required actions first, and drop internal-only items (refactors, CI, test changes) unless the user wants them.

### 5. Report the flags

After the notes, print the flag list: each Unsupported, Overstated, Unverified and Undocumented item with the changelog line, the evidence you looked at (file or commit), and a suggested resolution (fix the changelog, finish the work, or confirm with the author). Do not publish a notes draft as final while Undocumented breaking changes or Unsupported items remain open; say so.

## Hand off

The output is two blocks: the draft notes (Markdown, ready to paste) and the flag table. Tagging, creating the GitHub release and posting are left to the user; give the command (for example `gh release create <tag> --notes-file <file>`) but do not run it.

Generating a changelog from commit history is a different job; say so and stop rather than inventing one.

## References

- `references/claim-check.md` — open at step 3 for how to match a claim to a diff and the classification edge cases.
- `references/release-notes-format.md` — open at step 4 for the output layout and tone rules.
- `references/test-cases.md` — trigger and boundary cases; open when tuning the description.

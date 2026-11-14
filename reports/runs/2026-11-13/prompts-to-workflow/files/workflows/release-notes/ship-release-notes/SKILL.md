---
name: ship-release-notes
description: Turns a repo's CHANGELOG and last git tag into verified customer release notes, a customer email and a 3-line changelog-page post. Chains summarize-changes-since-tag, wordsmith, verify-release-notes and wordsmith again, carrying each step's output to the next. Use when the user says "do the release notes", "write up this release", or "changelog to customer email". Not for just grouping what changed since the last tag (use summarize-changes-since-tag), only polishing existing copy (use wordsmith), only checking notes against the diff (use verify-release-notes), or code review of the release (use consistent-code-review).
---

# ship-release-notes

Every release repeats one job: find what changed, say it in customer language, prove the claims are true, then announce it. It is a chain because each step needs the previous output verbatim, and the check in step 3 must run before anything is announced.

## Dependencies

Needs `summarize-changes-since-tag`, `verify-release-notes` and `wordsmith` installed (`npx skills add arm-pz/wordsmith`; the first two are new and not yet published, see `briefs/`). If one is missing, say so and stop; do not improvise its step.

## Workflow

### Step 1: Group changes with summarize-changes-since-tag
Receives: the repo with `CHANGELOG.md` and git tags. Hands on: changes grouped as features, fixes and breaking changes, plus the resolved last tag. Stops when: there is no tag, or the CHANGELOG has no entries since it.

### Step 2: Write customer notes with wordsmith
Receives: the grouped changes from step 1, verbatim. Hands on: draft release notes in plain English, no internal ticket numbers, leading with what users can now do. Keep breaking changes explicit; softening them misleads customers. Stops when: —

### Step 3: Check the notes with verify-release-notes
Receives: the draft notes from step 2 and the last tag from step 1. Hands on: the notes with every claim marked supported or unsupported against the diff since that tag. Stops when: any claim is unsupported. Show the unsupported claims and wait for the user to fix or remove them; re-run this step on the revised notes before continuing.

### Step 4: Write the email and post with wordsmith
Receives: the final notes that passed step 3, verbatim. Hands on: a short customer email and a 3-line changelog-page post. Do not add claims that are not in the final notes. Stops when: —

## Boundaries

- Carries outputs forward verbatim; summarizing between steps loses what the next skill checks.
- Respects each skill's gate; a gate that stops stops the chain.
- Does not do a routed step's work itself.
- Does not send the email or publish the post; it only drafts them.

## Report

One line per step: done, skipped (why) or stopped at a gate. One next step.

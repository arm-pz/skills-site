## Release notes: from CHANGELOG to customer-ready copy

Source: `prompts.md` (4 prompts). Catalog: live skillsmith.tech index (62 skills, 12 brews), checked 2026-11-13.

### Workflow map (confirmed)

| Step | Does | Receives | Hands on | Stops when | Prompts |
| --- | --- | --- | --- | --- | --- |
| 1 | Read the CHANGELOG and group what changed since the last tag | Repo with `CHANGELOG.md` and git tags | Changes grouped as features, fixes, breaking changes | No tag exists, or the CHANGELOG has no entries since the last tag | 1 |
| 2 | Rewrite as customer-facing notes: plain English, no ticket numbers, lead with what users can now do | Grouped changes from step 1 | Draft release notes | — | 2 |
| 3 | Check the notes against the git diff since the last tag; flag claims the code doesn't do | Draft notes from step 2, git diff since the last tag | Notes with each claim marked supported or unsupported | Any claim is unsupported, until the user fixes or removes it | 3 |
| 4 | Turn the final notes into a short customer email and a 3-line changelog-page post | Final notes from step 3 | Email and 3-line post | — | 4 |

Orphans: none. Merged: none.
Shared parameter: the last tag is resolved once (step 1) and reused in step 3.

### Split table

| Step | Verdict | Skill | Evidence | Installed |
| --- | --- | --- | --- | --- |
| 1 | new | `summarize-changes-since-tag` | No description claims CHANGELOG-plus-tag grouping. `ship-second-brain` ("issues, PRs, specs, and call notes") builds a knowledge base, not a per-release grouping; `production-code` "docs" is code delivery. Runs every release. | — |
| 2 | reuse | `wordsmith` | "drafts, rewrites, tightens and proofreads text ... Meaning, facts ... carry through". Pass step 1's output and the style rules (plain English, no ticket numbers, lead with user capability). | no |
| 3 | new | `verify-release-notes` | `research-brief` fact-checks via "dated source read in the session", i.e. web and documents, not code diffs. `consistent-code-review` reviews code, not prose claims. Nothing claims notes-versus-diff checking. Runs every release. | — |
| 4 | reuse | `wordsmith` | "adapt" discipline rewrites text to a new format and length, facts preserved. Alternative considered: `platform-content` ("newsletters ... repurposing chains") is built from a brief for audience content, so it is the weaker fit for two fixed deliverables from finished notes. | no |

Brew match: none. No brew covers changelog, notes, verification and announcement. Brew 4 and Brew 9 only touch `platform-content` and `wordsmith` at the edges.
Chain skill match: none (`findable-polish` and similar chain `wordsmith` with SEO or listing audits).
Counts: reuse 2 (both `wordsmith`), chain 0, new 2, inline 0.
Merge check: steps 1 and 3 share the "since last tag" input but are not adjacent and each has its own solo request, so they stay separate.

### Files

- `ship-release-notes/SKILL.md`: the chain skill (4 steps, 3 routed skills).
- `briefs/summarize-changes-since-tag.md`, `briefs/verify-release-notes.md`: briefs for the two new skills.
- `trigger-cases.md`: trigger cases for the chain skill (written, not run).

### Install lines

    npx skills add arm-pz/wordsmith

The two new skills are not published. Until they are built from the briefs, the chain is a plan: step 1 and step 3 cannot run through a skill.

### Handoffs

- `briefs/summarize-changes-since-tag.md` goes to `prompts-to-skill` (prompt 1 attached).
- `briefs/verify-release-notes.md` goes to `prompts-to-skill` (prompt 3 attached).
- Once built, the chain skill goes to `prompts-to-skill-release`.

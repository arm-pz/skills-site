# Brief: summarize-changes-since-tag

- **Step it fills:** Release notes, step 1.
- **Receives:** a repo with `CHANGELOG.md` and git tags. **Hands on:** the resolved last tag and the changes since it, grouped as features, fixes and breaking changes.
- **Why new:** checked `ship-second-brain` (builds an evidence-backed knowledge base from issues and PRs, not a per-release grouping), `production-code` (delivers code, not release summaries), `wordsmith` (edits text it is given, does not read git), `research-brief` (web and document sources). None claims CHANGELOG-plus-tag grouping.
- **Trigger phrases:** "what changed since the last tag?"; "summarize the CHANGELOG for this release"; "list the breaking changes since v2.3" (no chain vocabulary).
- **Near-miss:** "rewrite these changes as customer release notes" must go to `wordsmith`.
- **Gate:** stop when there is no tag, or the CHANGELOG has no entries since it. Flag CHANGELOG entries with no matching commits instead of dropping them.
- **Prompts:**
  1. "Read the CHANGELOG.md in this repo and tell me what changed since the last tag, grouped into features, fixes and breaking changes."
- **Hand to:** `prompts-to-skill` (one prompt attached; it asks for three, so supply the intent interview answers and note the gap).

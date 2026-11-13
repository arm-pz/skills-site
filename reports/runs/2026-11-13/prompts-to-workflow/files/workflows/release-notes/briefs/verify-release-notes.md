# Brief: verify-release-notes

- **Step it fills:** Release notes, step 3.
- **Receives:** draft release notes and a git tag (or range). **Hands on:** the notes with each claim marked supported or unsupported, citing the diff hunk or file that supports it; unsupported claims listed first.
- **Why new:** checked `research-brief` (fact checks against dated web and document sources, not a code diff), `consistent-code-review` (reviews code, not prose claims), `wordsmith` (flags shaky claims for checking but does not check them against code). None claims notes-versus-diff verification.
- **Trigger phrases:** "do these release notes match what the code does?"; "flag anything the changelog promises that isn't in the diff"; "fact-check our release announcement against the commits" (no chain vocabulary).
- **Near-miss:** "review this diff for bugs" must go to `consistent-code-review`.
- **Gate:** any unsupported claim blocks the next step until the user fixes or removes it. Unreadable or too-large diffs are reported INCONCLUSIVE, never marked supported.
- **Prompts:**
  1. "Check the release notes against the actual diff since the last tag and flag anything the notes claim that the code doesn't do."
- **Hand to:** `prompts-to-skill` (one prompt attached; it asks for three, so supply the intent interview answers and note the gap).

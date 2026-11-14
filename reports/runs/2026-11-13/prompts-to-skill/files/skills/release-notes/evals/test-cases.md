# Test cases for release-notes

Judged by hand against the description. No automated triggering loop was run.

| # | Message | Expected | Pass condition | Result |
| --- | --- | --- | --- | --- |
| 1 | "Read the CHANGELOG and tell me what changed since the last tag, grouped into features, fixes and breaking changes" | trigger (clear) | stage 1 grouped summary | pass (review) |
| 2 | "Rewrite those as customer-facing release notes, no ticket numbers" | trigger (clear) | stage 2, no ticket IDs | pass (review) |
| 3 | "Check the notes against the diff since the last tag" | trigger (clear) | stage 3 table | pass (review) |
| 4 | "What shipped this time? Need it written up for customers" | trigger (implicit) | starts at stage 1 | pass (review) |
| 5 | "Do these notes promise anything the code doesn't do?" | trigger (implicit) | stage 3 | pass (review) |
| 6 | "Add an entry for my new feature to CHANGELOG.md" | no (near-miss: edits changelog) | not triggered | pass (review) |
| 7 | "Review this diff for bugs" | no (code-review owns it) | not triggered | pass (review) |
| 8 | "Bump the version, tag v2.4.0 and create the GitHub release" | no (near-miss: shares "release") | not triggered | pass (review) |
| 9 | "Write the release notes and email them to our customers" | trigger, but stops | notes and email shown, nothing sent | pass (review) |

Boundary pair: #3 (judge notes against diff, triggers) and #7 (judge code for bugs, does not).

Counts: 9 written, 9 reviewed by hand, 0 live runs.

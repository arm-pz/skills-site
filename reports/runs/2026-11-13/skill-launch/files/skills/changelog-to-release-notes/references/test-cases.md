# Test cases

Status: **written, not run.** No automated triggering loop was available, and no sibling descriptions have been compared by an agent.

| # | Message | Expected | Pass condition |
| --- | --- | --- | --- |
| 1 | "Write release notes for 2.4.0 from our changelog" | this skill | reads the 2.4.0 section, diffs tags, outputs notes + flag table |
| 2 | "Turn CHANGELOG.md into something customers can read" | this skill | same; does not ask what a changelog is |
| 3 | "Make a what's new post for this release, but only say things we really shipped" | this skill | flags unbacked lines instead of dropping them |
| 4 | "Does our changelog actually match the code in v1.8?" | this skill | produces the flag table; notes optional |
| 5 | "Draft the upgrade notes people need for the new version" (changelog exists) | this skill | puts breaking changes first |
| 6 | "Generate a CHANGELOG from our commits" | not this skill | says that is a different job, does not write notes |
| 7 | "Publish the release and tweet it" | not this skill | gives `gh release create` at most; does not run or post |
| 8 | "Write a landing page for our product" | not this skill (marketing copy) | does not trigger |
| 9 | "Summarize what changed in this PR" | not this skill (no changelog/release) | does not trigger |

Boundary pair: "write release notes from the changelog" triggers; "write the changelog from commits" does not. Spanning case: "make the changelog, then the release notes" should do the first elsewhere and use this skill for the second.

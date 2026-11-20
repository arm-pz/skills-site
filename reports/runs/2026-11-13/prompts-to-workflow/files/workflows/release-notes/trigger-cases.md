# Trigger cases: ship-release-notes

Status: written, not run.

## Should trigger

1. "Do the release notes for this release."
2. "Take the CHANGELOG since the last tag and get me a customer email and changelog post, checked against the code."
3. "Write up v2.4 for customers, end to end."

## Near-misses (must not trigger; the owner handles it)

4. "What changed since the last tag?" → `summarize-changes-since-tag`
5. "Make these release notes friendlier." → `wordsmith`
6. "Do these notes match the diff?" → `verify-release-notes`
7. "Review this release's code for bugs." → `consistent-code-review`
8. "Is the site safe to launch?" → Brew 3 (Espresso), via `caffeinity-routing`

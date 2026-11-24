# Changelog

## 0.1.0 — 2026-11-24

First version, after Uber's always-on `log-papercut` skill.

- `SKILL.md`: four steps (recognise, look up, file, carry on), an error recovery table, and rules that keep the user's task first and the report free of prompt text and file contents.
- `scripts/papercut.py`: `file` writes to a local queue grouped by fingerprint and, with `--repo` or `$PAPERCUT_REPO`, opens a GitHub issue labelled `papercut` or comments on the open one; `list` finds known papercuts and their workarounds. Refuses "try again" as a fix.
- `references/format.md`: the record and issue format a nightly pipeline and skill-eval-suite read.
- `tests/test_papercut.py`: 15 checks with a fake `gh`, all passing.

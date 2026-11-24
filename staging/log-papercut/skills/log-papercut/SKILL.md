---
name: log-papercut
description: Files a structured papercut when a skill, tool, command or doc does not behave the way its instructions say, then carries on with the workaround. Records what was tried, what was expected, what happened and what would fix it, groups repeats by fingerprint, keeps a local queue, and opens or updates a GitHub issue labelled papercut for a nightly pipeline to pick up. Use whenever, in any task, a flag the help lists is rejected, a command exits 0 on an error, a query returns nothing when it should match, a skill step or doc is wrong, or you spend several turns working around the same error, even if the user never asks for a bug report. Not for bugs in the user's own code (fix them as the task), for scoring whether a skill's output is good (use eval-harness), or for rules mined from many past sessions (use harness-audit).
version: 0.1.0
---

# log-papercut

A papercut is friction you can work around but should not have to: a wrong flag in a skill, a tool that fails silently, a doc that points at a path that moved. You notice it because you are the one fighting it. Filing it takes one command and turns your wasted turns into a fix for the next session.

It is always on. File without being asked, once per distinct problem, then finish the user's task.

## Ground rules

- **The task comes first.** File, then continue with the workaround. Never stop the user's work to write a report.
- **One problem per papercut.** Two different failures are two reports, so each groups with its own repeats.
- **A fix, not "try again".** Say what should change in the skill, tool or doc. The script refuses "try again".
- **No prompt text, no file contents.** Describe the behaviour. The script masks secrets, emails and home paths, and caps every field, but you choose what goes in.
- **File only to the repo you were given.** GitHub issues go only to `--repo` or `$PAPERCUT_REPO`. With neither, the report stays in the local queue.
- **Not every error is a papercut.** Your own typo, a test that rightly fails, or a bug in the user's code is the task, not friction.

## Workflow

The script is `scripts/papercut.py` in this skill's folder. It needs Python 3.9+ and, for issues, an authenticated `gh`.

### 1. Recognise the papercut

File when one of these holds, and only then:

| Signal | Example |
| --- | --- |
| A documented option is rejected | the help lists `--since`, the tool says unknown flag |
| Success is reported on a failure | exit 0, empty output, and the work did not happen |
| An empty result where data must exist | a query for a key you just wrote returns nothing |
| A skill or doc step is wrong | wrong path, wrong unit (seconds vs milliseconds), stale command |
| You keep fighting the same error | the same error after three or more attempts or workarounds |

Confirm the signal against the source: run `<tool> --help` or open the doc or skill step you followed, and check that it says what you expected. Quote the command and the output line that shows the gap. If you cannot quote one, it is not a papercut yet.

### 2. Look up known workarounds

    python <skill-dir>/scripts/papercut.py list --skill <skill> --tool <tool>

Check the output for a matching `happened`. If one lists a `workaround`, try it first and note whether it worked; you still file in step 3, which raises that papercut's count.

### 3. File it

    python <skill-dir>/scripts/papercut.py file --skill <skill> --skill-version <v> --tool <tool> \
      --tried "<what you ran>" --expected "<what the docs or skill said would happen>" \
      --happened "<what happened, with the key error line>" --fix "<what should change, where>" \
      --workaround "<what got you past it, if anything>" --severity blocked|slowed|cosmetic \
      --error-pattern "<regex that matches the error text>" --agent "<agent and model>" --session <id>

Use `--skill none` for friction in a bare tool. Add `--reproducible` when a fixed input triggers it every time; eval-harness then makes it a golden case. Confirm the script prints `papercut <fingerprint> filed` or `seen again`; with a repo set it also prints `filed <url>` or `commented on <url>`. On exit 2, read the error, correct the field it names and run it once more.

### 4. Carry on and say so

Finish the user's task with the workaround. Before your final message, run `python <skill-dir>/scripts/papercut.py list --search <fingerprint>` and check it prints the record you filed. Then add one line: `Papercut filed: <skill>/<tool>: <fingerprint>`, plus the issue URL if there is one.

## When it fails

| Failure | Fix |
| --- | --- |
| `gh` not installed or not signed in | the papercut is still in the local queue; mention that GitHub filing was skipped |
| `issue not filed` about a missing label | the script creates `papercut` once and retries; if it still fails, the repo may not allow label creation: say so |
| exit 2: "'try again' is not a fix" | name the change: the flag, the line in the skill, the doc page |
| exit 2: a required field missing | fill `tried`, `expected`, `happened` and `fix`; use `--skill none` for a bare tool |
| the same failure keeps getting new fingerprints | keep `--happened` to the stable part of the error; drop ids, timestamps and paths |

## Where papercuts go next

`references/format.md` is the record and issue format, for anything that reads them. A nightly pipeline lists open `papercut` issues, groups them by fingerprint, and hands the top groups to triage. eval-harness turns each fixed papercut into a regression case (`intake.py papercuts`), so the fix stays fixed.

## Report

One line per papercut in your final message, as in step 4. Nothing else unless the user asks.

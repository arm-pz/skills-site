# straight-prose

An agent skill for Claude Code, Codex, Cursor and other agents that read a `SKILL.md`. It writes, edits and audits prose against a set of rules for the patterns language models produce by default: inflated significance, promotional wording, vague attribution, "not just X, but Y", groups of three, em dashes, chatbot pleasantries, bold-label bullet lists. When it edits your text it keeps your vocabulary, spelling and register.

It does not try to get text past an AI detector.

## Install

```
npx skills add arm-pz/straight-prose --skill straight-prose
```

The command works once the repo is published. Until then, copy the `straight-prose/` folder into `~/.claude/skills/` (Claude Code) or the skills directory your agent reads, or upload `straight-prose.zip` in the Claude app's skills settings. Start a new session and check that the skill appears in the agent's skill list.

## Try it

- "Take the AI slop out of this post but keep it sounding like me."
- "Does this sound like AI wrote it?"
- "Write the release note in my voice. No em dashes."

## What it does

The skill has three modes. Write applies the rules while drafting. Edit changes only the sentences that carry a pattern. Audit lists each pattern with its line and a suggested rewrite, and changes nothing.

`scripts/slop_scan.py` finds the mechanical patterns so the agent does not rely on its own read-through for them:

```
python scripts/slop_scan.py draft.md
```

It prints one line per hit with the line number and rule. It checks em dashes, the listed vocabulary and stock phrases, negative parallelisms, placeholders, tool markup, title-case headings, emoji decoration, horizontal rules and bold-label lists. It cannot see forced threes, a changed voice or an empty sentence, and it matches English only. `python -I scripts/test_slop_scan.py` is its self-check.

`references/sourcing.md` holds the rules for attribution, citations and contested claims. The skill reads it only when the text cites sources or makes factual claims.

The default dialect for text in your voice is Australian English when the conversation gives no other signal. That is one line in `SKILL.md` under "Ground rules".

## Boundaries

- Handles: removing or avoiding AI writing patterns in prose, and reporting them.
- Does not handle: tone changes, shortening, proofreading and fact-checking, which belong to [wordsmith](https://github.com/arm-pz/wordsmith). Resumes and CVs belong to [recruiter-lens](https://github.com/arm-pz/recruiter-lens) and applicant-kit.
- Known overlap: a bare "humanize this" also matches wordsmith's `humanize` command.

## Test results

Version 0.1.0: 12 trigger cases reviewed by hand against the descriptions, 11 pass and 1 fails. 4 evals written, 1 executed by the authoring session and 3 reviewed only. No case has been run in a live session by a fresh agent. Details are in `evals/trigger-cases.md`.

## Version

See `CHANGELOG.md`. MIT licence.

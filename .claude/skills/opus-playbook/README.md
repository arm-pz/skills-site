# opus-playbook

An agent skill for a lead model that hands work to Opus, or to any subagent or worker session,
and has to decide whether the result does the job that was asked. It writes a brief that can be
checked, runs a nine-step ladder on what comes back, and ends with one verdict: accept, return,
take over or escalate. It is for people who run a stronger model as the lead and want to know
what it verified before it says "done".

It is not a guide to prompting Opus.

## Install

- Claude Code: copy this folder to `~/.claude/skills/opus-playbook/`, or to a project's
  `.claude/skills/opus-playbook/`.
- Claude app or web: upload `opus-playbook.zip` in the skills settings.
- Other agents: copy the folder into the directory that agent reads (`.agents/skills/`,
  `.cursor/skills/`, `~/.qoder/skills/`).
- From GitHub, once this folder is its own repository: `npx skills add <owner>/opus-playbook`

Then confirm `opus-playbook` appears in the agent's skill list.

## Try it

- "Hand this fix to Opus and make sure it actually did it before we merge."
- "The subagent says the tests pass. Is that true?"
- "How do you know the worker didn't just stub it out?"

## What is in the folder

| File | Why it exists |
| --- | --- |
| `SKILL.md` | The brief, the check ladder, the report phrases, the verdict and the record |
| `scripts/worker_diff.py` | The mechanical part of the ladder: changed files, files the report never names, test and CI edits, and added lines that skip, silence or stub. Needs Python 3 and git; reads only |
| `references/trigger-cases.md` | The trigger test cases and their results |

It needs nothing from the project it runs in. The script works in any git repository, and the
ladder falls back to a manual file list outside one. The skills named under Boundaries are
optional; without them the skill says what it did not cover.

## Boundaries

- Handles: the acceptance decision on delegated work, checked against the brief it was given.
- Does not handle: a defect review of code with no brief (`consistent-code-review`), deciding
  which model takes which role (`setup-claude-advisor`), effort and fan-out (`choose-effort`),
  or pressure-testing a decision (`crash-test`).

## Test results

- Version 0.1.1: 0 pass by execution, 0 fail, 10 reviewed-only, 0 not run. The ten trigger cases
  were read by hand against the descriptions; no live session was used.
- `worker_diff.py` reported 7 of 7 planted problems in a throwaway repository.
- The skill has not yet been used on a real hand-off to Opus.

## A note on the name

A GitHub search on 2026-11-17 found no repository named exactly `opus-playbook` and no topic of
that name. Five repositories have close names, and all of them are guides to prompting or
configuring Opus; the largest, `rennf93/opus-fable-playbook`, had 34 stars. Someone searching
this name is likely to expect a prompting guide.

## Version

See CHANGELOG.md. MIT licence.

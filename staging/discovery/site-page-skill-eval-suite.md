---
title: "skill-eval-suite: evals for agent skills and loops"
description: "Agent skill that builds eval suites for other skills and scheduled loops: trajectory grading, 3+ trials, same-case flips, token budgets, known-bad gates."
slug: skill-eval-suite
repo: https://github.com/arm-pz/skill-eval-suite
install: "npx skills add arm-pz/skill-eval-suite --skill skill-eval-suite"
tags: [agent-skills, claude-code, evals, agent-evaluation, llm-as-a-judge, eval-driven-development, trajectory-evaluation]
---

# skill-eval-suite: evals for agent skills and loops

An agent skill that tells you whether another skill, or a scheduled agent loop, is any good, and keeps
telling you as it changes. It builds the eval suite from the loop's own history (real prompts, the
paths it took, PRs people rejected, papercuts agents filed) and scores it the way agent evals behave:
as pass rates over repeated trials, as flips on the same cases, and against a token budget. It never
runs your loop itself and never invents a verdict for the author.

## What you can ask it

| Ask | What it does |
| --- | --- |
| "Build an eval suite for my nightly report" | harvests real sessions, papercuts and rejected PRs into candidate cases, confirms them with you, writes `evals/` |
| "Is the new prompt better, or did I get a lucky run?" | scores 3+ trials and lists fixed and broken cases against the baseline |
| "Can we trust our LLM judge?" | runs the known-bad set (every bad output must fail) and a 30–50 output calibration |
| "Does this skill earn its tokens?" | blind with-versus-without ablation, plus per-skill token windows |
| "Why did last night's run fail?" | reads the Claude Code trace and names the failure class and owner |

## Install

```
npx skills add arm-pz/skill-eval-suite --skill skill-eval-suite
```

Or copy `skills/skill-eval-suite/` into `~/.claude/skills/`, `~/.codex/skills/` or `~/.qoder/skills/`.
The scripts need Python 3.9+ and nothing else. Trajectory and token checks read Claude Code session
traces.

## Example

A real run of the known-bad gate on skillsmith.tech's own pipeline set:

```
kb-001-duplicate-pr-work caught | triage_skips_open_pr: Add trigger cases for the four search-visibility skills overlaps open PR #24 on check-skill-visibility, diagnose-search-visibility, evals/triggers.json, fix-skill-visibility
kb-002-repeated-report caught | not_in_previous: 5 repeated, first: 'REGRESSION  dangling handoff: replace-dead-tools -> broken-l'
kb-003-off-spec-diff caught | diff_within_spec: outside the spec's Files: scripts/build_evals.py
kb-004-stranger-issue caught | triage_trusted_source: #32 by stranger-dev has no pipeline-ok label

known-bad caught 4 of 4: trusted
```

[Paste a real scorecard here after the first full loop run.]

## Questions

**Why not report one pass rate?**
Because the same agent scores 82 then 79 on the same cases. On 20 cases one case is 5 points. It
reports which cases flipped instead, and blocks only on a repeated clear loss.

**Does it grade with an LLM?**
Code checks first. A judge rubric gates nothing until it fails every known-bad output and agrees with
the author on 30 or more samples.

**Is it related to lm-evaluation-harness or evals-skills?**
No. EleutherAI's lm-evaluation-harness benchmarks models; hamelsmu/evals-skills helps you build evals
for an AI product. This one evaluates agent skills and scheduled loops.

**Has it been run on a real loop?**
Not end to end yet. The scripts pass 60 self-checks and were run on real Claude Code sessions.

## Related

- [log-papercut](https://skillsmith.tech/log-papercut/): agents file friction as they hit it; fixed papercuts become cases here
- [tune-skill](https://skillsmith.tech/tune-skill/): whether a skill's description triggers, which this does not test
- [Source on GitHub](https://github.com/arm-pz/skill-eval-suite)

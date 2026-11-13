# prompts-to-skill: real-world run, 2026-11-13

**Verdict: FAIL** (2/10). The run read prompts.md (4 prompts), checked installed skills for overlap, and stopped to ask for intent confirmation, but never drafted a skill, wrote test cases, or ran the validator, so no SKILL.md exists under skills/.

Target: four real-shaped release-notes prompts from a developer's history. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 10 s, $0.07).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Turn the prompts in prompts.md into a skill (or skills). Put the result under skills/. My answers to your intake questions: it's for me in Claude Code, repos are on GitHub, I want it to stop and show me the notes before anything is sent.
```

## Rubric

- Runs an intent step and an overlap check before drafting
- Drafts with draft-skill and writes trigger test cases including near-misses
- Gates the result with tune-skill's validator with zero FAILs
- Keeps the 'show me before sending' constraint in the skill

## Hard checks

- ✗ a SKILL.md was written under skills/
- ✗ check_skill.py reports no FAIL

## Met

- Ran an intent step (proposed purpose, single-skill decision, output, triggers, scope) before drafting
- Ran an overlap check (Glob of **/SKILL.md and references) and reported no installed skill covers release notes
- Planned to keep the 'show me before sending' constraint (stop point described in the proposed intent)

## Missed

- No SKILL.md was written under skills/ (hard check failed); only Read and Glob calls were made
- No draft-skill step was run and no trigger test cases (including near-misses) were written
- tune-skill's validator (check_skill.py) was never run, so there is no zero-FAIL gate
- The 'show me before sending' constraint is only stated in chat, not present in any skill file
- Stopped to ask for 'yes' confirmation even though the user had already given intake answers (for me, Claude Code, GitHub, stop and show before sending) and asked for the result to be put under skills/

## Defects to fix in the skill

- The skill's intent step requires a user confirmation round-trip even when the user has already supplied intake answers and asked for the output to be written; it should proceed to draft when intake answers are given, or at least not halt the whole run on a confirmation
- The skill does not distinguish single-turn/non-interactive runs, so the pipeline can end after the intent step with no artifact produced
- The skill instructs showing test cases to the user before tuning, which adds another potential halt point and risks the run ending without writing files

## What it did

1. `Skill: prompts-to-skill`
1. `Read: /tmp/run-prompts-to-skill-j6wqet47/project/prompts.md`
1. `Glob: **/SKILL.md`
1. `Glob: .claude/skills/*/references/*`

## Final output

I've read prompts.md and checked the installed skills. Four prompts is above the three-prompt minimum, and no installed skill covers release notes, so there's no overlap. Before I draft anything, please confirm this intent.

**Purpose:** one skill, `release-notes`, that takes a repo from its CHANGELOG to published customer notes. It runs your four prompts as one flow:
1. Read CHANGELOG.md and summarize what changed since the last tag, grouped into features, fixes and breaking changes.
2. Rewrite that as customer-facing notes: plain English, no ticket numbers, led by what users can now do.
3. Check the notes against the actual diff since the last tag and flag any claim the code doesn't support.
4. Turn the final notes into a short customer email and a 3-line changelog-page post.

**One skill, not four.** The prompts are sequential stages of one job, and each stage uses the previous stage's output.

**Output:** the grouped summary, the notes, a list of flagged claims, the email and the 3-line post. All of it is shown in the chat.

**Stop point:** the skill ends with a hard stop and shows you the notes, flags, email and post. It never sends, publishes, pushes, posts or creates a GitHub release unless you explicitly approve after reviewing. Drafting and local diff reads are fine. Anything that leaves your machine needs your go-ahead.

**Triggers:** "write release notes", "what changed since the last tag", "customer-facing changelog", "check the notes against the diff", "turn this into a customer email", and similar phrasing. It runs in Claude Code against a GitHub-hosted repo, using local git (`git describe --tags`, `git diff <tag>..HEAD`) and `gh` for context only.

**Not covered:** tagging or cutting the release itself, and editing CHANGELOG.md.

Is that right? Reply "yes" or tell me what to change. After that I'll draft the skill, write at least eight test cases and show them to you, then tune and validate.

# prompts-to-skill: real-world run, 2026-11-13

**Verdict: PASS** (8/10). The run built a single release-notes skill at skills/release-notes/ (SKILL.md, a claim-check reference, 7 eval prompts, 9 test cases including near-misses), and check_skill.py reported 0 fail and 0 warn; the stop-before-send rule is kept as a hard rule and a final stage.

Target: four real-shaped release-notes prompts from a developer's history. Run headless in a clean project with only this skill installed (14 turns, 11 tool calls, 55 s, $0.26).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Turn the prompts in prompts.md into a skill (or skills). Put the result under skills/. My answers to your intake questions: it's for me in Claude Code, repos are on GitHub, I want it to stop and show me the notes before anything is sent.
```

Follow-up:

```
Confirmed, that's right. Go ahead and finish it without stopping for more questions.
```

## Rubric

- Runs an intent step and an overlap check before drafting
- Drafts with draft-skill and writes trigger test cases including near-misses
- Gates the result with tune-skill's validator with zero FAILs
- Keeps the 'show me before sending' constraint in the skill

## Hard checks

- ✓ a SKILL.md was written under skills/
- ✓ check_skill.py reports no FAIL

## Met

- Ran an intent step (restated purpose, output, triggers, safety stop, shape for confirmation) and an overlap check (found no installed skill covering release notes; code-review named as nearest) before drafting
- Drafted with draft-skill: read its SKILL.md and structure reference, then wrote SKILL.md, references/claim-check.md and evals
- Wrote 9 trigger test cases that include near-misses (CHANGELOG edit, bug review, version bump/tag/GitHub release) and a 'write and email them' case that expects a stop
- Gated with tune-skill's check_skill.py, run with python3 -I, reporting 0 fail and 0 warn
- Kept the 'show me before sending' constraint: a hard rule that the skill never sends or publishes, plus a stage 5 that shows the text and waits
- Hard checks satisfied: SKILL.md written under skills/ and no FAIL from the validator
- Honestly reported that the test cases were reviewed by hand with no live runs, and that Gate B was passed by review, not executed

## Missed

- The final output says the intent was confirmed once, but the test-case list was not shown for editing before tuning, as the skill's own intent message promised; this was excused by the follow-up's 'no more questions'
- Triggering was not tested live, so the 9 'pass (review)' results are self-judged, not measured
- The first bulk-write Bash attempt was blocked and was redone with the Write tool; no harm, but the transcript shows a wasted step

## Defects to fix in the skill

- The prompts-to-skill gates allow 'passed by review' for the triggering gate with no live run, so near-miss behavior is never actually exercised
- The skill does not say what to do when the user pre-answers intake questions and then says to skip stops, so the test-case review step is dropped silently

## What it did

1. `Skill: prompts-to-skill`
1. `Read: /tmp/run-prompts-to-skill-ggnkrl49/project/prompts.md`
1. `Bash: cd /tmp/run-prompts-to-skill-ggnkrl49/project; ls -R .claude/skills | head -50; ls skills 2>&1 | head`
1. `Bash: cd /tmp/run-prompts-to-skill-ggnkrl49/project/.claude/skills; cat draft-skill/SKILL.md draft-skill/references/structure.md tune-skill/references/test-cases.md p`
1. `Bash: cd /tmp/run-prompts-to-skill-ggnkrl49/project/.claude/skills; cat tune-skill/references/test-cases.md prompts-to-skill/references/gates.md`
1. `Bash: cd /tmp/run-prompts-to-skill-ggnkrl49/project; mkdir -p skills/release-notes/references skills/release-notes/evals
cat > skills/release-notes/SKILL.md <<'EOF'
-`
1. `Write: /tmp/run-prompts-to-skill-ggnkrl49/project/skills/release-notes/SKILL.md`
1. `Write: /tmp/run-prompts-to-skill-ggnkrl49/project/skills/release-notes/references/claim-check.md`
1. `Write: /tmp/run-prompts-to-skill-ggnkrl49/project/skills/release-notes/evals/evals.json`
1. `Write: /tmp/run-prompts-to-skill-ggnkrl49/project/skills/release-notes/evals/test-cases.md`
1. `Bash: python3 -I /tmp/run-prompts-to-skill-ggnkrl49/project/.claude/skills/tune-skill/scripts/check_skill.py /tmp/run-prompts-to-skill-ggnkrl49/project/skills/release`

## Files it wrote

Copied under `files/`:

- `skills/release-notes/SKILL.md`
- `skills/release-notes/evals/evals.json`
- `skills/release-notes/evals/test-cases.md`
- `skills/release-notes/references/claim-check.md`

## Final output

Both dependencies (`draft-skill`, `tune-skill`) are installed. Your four prompts are enough to work from, and none of them involves unauthorized access, exfiltration, or personal data. No installed skill covers release notes, so this isn't a duplicate.

**Please confirm this intent before I draft anything:**

- **Purpose:** Turn a repo's changes since the last tag into customer-facing release notes, check them against the code, and prepare them to send. This covers your four prompts in order:
  1. Summarize `CHANGELOG.md` since the last tag, grouped into features, fixes and breaking changes.
  2. Rewrite that summary as plain-English notes with no ticket numbers, leading with what users can now do.
  3. Check each claim in the notes against the real diff since the last tag, and flag anything the code doesn't do.
  4. Produce a short customer email and a 3-line changelog-page post.
- **Output:** The grouped summary, the release notes, a list of unsupported claims, then the email and the 3-line post.
- **Trigger contexts:** You ask in Claude Code, inside a GitHub-hosted repo, for things like "write release notes", "what changed since the last tag", "check the notes against the diff", or "draft the customer email for this release".
- **Safety stop:** The skill never sends or publishes anything. That includes email, changelog page, GitHub releases, and `gh` or `git push` commands. After the claim check it shows you the final notes, email and post, and waits for your explicit go-ahead. Even then it only prepares the text for you to send.
- **Shape:** One skill, `release-notes`, in `skills/release-notes/`. The four prompts are sequential stages of one workflow, so splitting them into separate skills would add nothing.

Is that right? If so, I'll draft it, write at least eight test cases, and show you the list to edit before tuning.

---

I built the `release-notes` skill at `skills/release-notes/`, and the structure check passes. I haven't run the skill against a real repo. My first attempt to write the files in bulk was blocked, so I wrote them one at a time instead. Your one confirmation was the intent, which I restated before drafting.

- **Overlap:** none. No installed skill covers release notes. `code-review` is the nearest, and the description hands code review off to it.
- **Step 1 (draft):** `SKILL.md` runs your four prompts as stages: summarize since the last tag, rewrite for customers, check against the diff, then draft the email and a 3-line post. `references/claim-check.md` explains how to judge borderline claims.
- **Stop-before-send:** a final stage shows the notes, the claim check, the email and the post, then waits for you. The skill never sends or publishes anything, including `gh release` and `git push`.
- **Step 2 (test cases):** `evals/test-cases.md` has 9 cases and `evals/evals.json` has 7 prompts. You said not to stop for questions, so I didn't pause for you to edit the list. Edit `evals/test-cases.md` and `evals/evals.json` if you want to add or remove cases.
- **Step 3 (tune):** `check_skill.py` reported 0 fail and 0 warn. The description is 747 characters.
- **Gate A:** passed.
- **Gate B:** passed by review, not run. All 9 cases were judged by hand against the description, with none run live, and the original four prompts each match a stage. The cases include a near-miss pair against `code-review`, plus a "write and email them" case that expects the skill to stop without sending.
- **Prompts not covered:** none.
- **`findable`:** skipped, because you didn't mention publishing.

**Next step:** try it in a real repo with a tag, for example "write release notes since the last tag". The stop-before-send behavior is the thing to watch.

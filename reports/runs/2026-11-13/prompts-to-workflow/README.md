# prompts-to-workflow: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). Mapped 4 prompts to 4 ordered steps with gates, reused wordsmith for steps 2 and 4, proposed 2 new skills (summarize-changes-since-tag, verify-release-notes) after checking the 62-skill catalog, and wrote workflow, chain SKILL.md, briefs and trigger cases under workflows/release-notes/, but never ran check_skill.py.

Target: four real-shaped release-notes prompts checked against the live catalog. Run headless on the CLI default model in a clean project with only this skill installed (14 turns, 11 tool calls, 53 s, $0.38).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
These prompts in prompts.md are one job I do every release. Turn them into a workflow and tell me which steps are existing skills on skillsmith.tech and which need new ones. Output under workflows/.
```

Follow-up:

```
Confirmed, that's right. Go ahead and finish it without stopping for more questions.
```

## Rubric

- Maps the 4 prompts to ordered steps with inputs, outputs and gates
- Checks each step against the live catalog and reuses real skills where they fit (e.g. wordsmith or straight-prose for the rewrite)
- Only proposes new skills for steps no catalog skill claims
- Validates any new skill with check_skill.py

## Hard checks

- ✓ wrote something under workflows/

## Met

- Maps the 4 prompts to ordered steps with inputs, outputs (hands on) and gates (stops when), with orphan/merge/shared-parameter notes
- Checks each step against the catalog (cited 62 skills, 12 brews) and reuses wordsmith for steps 2 and 4, with platform-content considered and rejected
- Proposes new skills only for steps 1 and 3, with evidence of which catalog skills were checked and why they don't claim the step
- Wrote output under workflows/ (workflow.md, ship-release-notes/SKILL.md, two briefs, trigger-cases.md)

## Missed

- Did not validate the new chain skill with check_skill.py: the Glob for check_skill.py found nothing usable and no validation run appears in the tool calls; the final output says the shell was denied, which the transcript does not clearly show beyond a combined Bash call
- Final summary blends a pre-confirmation turn (said 'I haven't written anything yet', asked questions) with the post-confirmation turn, so the run stopped for confirmation once before finishing, which was expected but leaves the report slightly muddled
- The claim that the catalog was 'live' and checked 2026-11-13 is not clearly shown in the tool calls (no fetch tool call is listed; only a Bash script call truncated), so catalog verification is unverifiable from the transcript; date also differs from the session date of 2026-11-14
- The two new-skill briefs were not turned into actual skills, so nothing new was validated; they are only briefs

## Defects to fix in the skill

- The skill points to a check_skill.py validator that lives in a different skill (tune-skill) and is not in the project, so the run could not find or run it; the skill should bundle the validator or give its exact path and a fallback
- The skill has no explicit rule for what to do when validation cannot run, so the run ended with the chain skill unvalidated and just reported it to the user
- The two-phase flow (map, confirm, then split and write) produces a muddled combined final output; the skill should make the final report only cover what was written

## What it did

1. `Skill: prompts-to-workflow`
1. `Read: /tmp/run-prompts-to-workflow-ebdculw1/project/prompts.md`
1. `Bash: cd /tmp/run-prompts-to-workflow-ebdculw1/project/.claude/skills/prompts-to-workflow && ls -R . | head -30 && cat references/workflow-map.md && python3 scripts/c`
1. `Bash: cd /tmp/run-prompts-to-workflow-ebdculw1/project; cat .claude/skills/prompts-to-workflow/references/split-rules.md; ls .claude/skills; find / -name check_skill.`
1. `Read: /tmp/run-prompts-to-workflow-ebdculw1/project/.claude/skills/prompts-to-workflow/references/split-rules.md`
1. `Glob: **/check_skill.py`
1. `Write: /tmp/run-prompts-to-workflow-ebdculw1/project/workflows/release-notes/workflow.md`
1. `Write: /tmp/run-prompts-to-workflow-ebdculw1/project/workflows/release-notes/ship-release-notes/SKILL.md`
1. `Write: /tmp/run-prompts-to-workflow-ebdculw1/project/workflows/release-notes/briefs/summarize-changes-since-tag.md`
1. `Write: /tmp/run-prompts-to-workflow-ebdculw1/project/workflows/release-notes/briefs/verify-release-notes.md`
1. `Write: /tmp/run-prompts-to-workflow-ebdculw1/project/workflows/release-notes/trigger-cases.md`

## Files it wrote

Copied under `files/`:

- `workflows/release-notes/briefs/summarize-changes-since-tag.md`
- `workflows/release-notes/briefs/verify-release-notes.md`
- `workflows/release-notes/ship-release-notes/SKILL.md`
- `workflows/release-notes/trigger-cases.md`
- `workflows/release-notes/workflow.md`

## Final output

I've mapped the four prompts. I haven't written anything yet. The workflow needs you to confirm the order and gates first, because a wrong order means redoing the split.

## Release notes: from CHANGELOG to customer-ready copy

| Step | Does | Receives | Hands on | Stops when | Prompts |
| --- | --- | --- | --- | --- | --- |
| 1 | Read the CHANGELOG and group what changed since the last tag | Repo with `CHANGELOG.md` and git tags | Changes grouped as features, fixes and breaking changes | There is no tag, or the CHANGELOG has no entries since it | 1 |
| 2 | Rewrite as customer-facing release notes: plain English, no ticket numbers, lead with what users can now do | Grouped changes from step 1 | Draft release notes | — | 2 |
| 3 | Check the notes against the real diff since the last tag and flag claims the code doesn't back | Draft notes from step 2, plus the git diff since the last tag | Notes with each claim marked supported or unsupported | Any claim is unsupported, until you fix or remove it | 3 |
| 4 | Produce a short customer email and a 3-line changelog-page post | Final notes from step 3 | Email and 3-line post | — | 4 |

- **Orphans:** none.
- **Merged:** none. The four prompts are four distinct steps.
- **Parameters:** the last tag is resolved once and reused in steps 1 and 3. Step 4's "final notes" means the notes after step 3's fixes.

**Two things to confirm:**
1. **Order.** Check-against-the-diff (step 3) runs after the rewrite and before the email and post, so a false claim never reaches customers. Is that right?
2. **Gates.** I added two that your prompts don't state. Step 3 blocks step 4 on unsupported claims. Step 1 stops if there's no tag. Do you want both, or should step 3 only flag?

Once you confirm, I'll check each step against the live skillsmith.tech catalog (62 skills, 12 brews) and show you the split table (existing skill, new skill or inline) before writing anything to `workflows/`.

---

The release workflow is written under `workflows/release-notes/`. Two of its four steps are existing skills and two need new ones. The new skills don't exist yet, so the chain can't run end to end today.

## Which steps are existing skills

| Step | Verdict | Skill |
| --- | --- | --- |
| 1. Group changes since the last tag | **new** | `summarize-changes-since-tag` |
| 2. Customer-facing release notes | **existing** | `wordsmith` |
| 3. Check notes against the diff | **new** | `verify-release-notes` |
| 4. Customer email and 3-line post | **existing** | `wordsmith` |

- **Why steps 1 and 3 are new:** no skillsmith.tech description covers grouping a CHANGELOG by tag, or checking notes against a git diff. `research-brief` fact-checks against web and document sources, not code. `ship-second-brain` and `consistent-code-review` don't fit either. Each step recurs every release and has its own natural request, so each earns its own skill.
- **Step 4 judgement call:** I picked `wordsmith` over `platform-content`. The email and post are fixed outputs built from finished notes, and `platform-content` is built around a brief.
- **No brew match:** none of the 12 brews covers this chain.
- **Catalog:** live (62 skills), checked today.

## What's in `workflows/release-notes/`

- `workflow.md`: the confirmed map, the split table with evidence, and install lines.
- `ship-release-notes/SKILL.md`: a chain skill that runs the four steps in order. It stops at step 3 until you fix or remove any unsupported claim, and it doesn't send the email or publish the post.
- `briefs/summarize-changes-since-tag.md` and `briefs/verify-release-notes.md`: briefs for the two new skills. Each has its original prompt attached and is meant to go to `prompts-to-skill`.
- `trigger-cases.md`: 3 should-trigger cases and 5 near-misses, written but not run.

## What's not done

- **The chain skill is unvalidated.** The shell was denied in this session, so I couldn't run tune-skill's `check_skill.py`. You can run it with `python .claude/skills/tune-skill/scripts/check_skill.py workflows/release-notes/ship-release-notes`.
- **Nothing is installed.** Run `npx skills add arm-pz/wordsmith`. The two new skills aren't published yet.
- **`prompts-to-skill` wants three prompts per skill** and each brief has one, so you'll need to supply interview answers for the rest.

**Next step:** build `verify-release-notes` first, since it's the gate that protects customers from false claims. Then build `summarize-changes-since-tag`.

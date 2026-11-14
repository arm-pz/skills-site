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
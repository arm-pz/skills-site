# straight-prose: real-world run, 2026-11-13

**Verdict: PASS** (8/10). The agent read draft.md, wrote draft-v2.md, and ran slop_scan, which found nothing; the hedge about unmeasured customer benefit was kept, and the agent removed the opener, the closing line with emoji, 'Experts agree' and 'not just faster, it's smarter'.

Target: a 200-word product blog post with stock AI-writing patterns. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 11 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
draft.md reads like a chatbot wrote it. Rewrite it so it sounds like a person on our engineering team wrote it, same facts. Save as draft-v2.md.
```

## Rubric

- Removes inflated significance, promotional wording, vague attribution ('Experts agree'), negative parallelism ('not just … it's'), forced threes, em dashes, chatbot sign-off and emoji
- Keeps every fact and number and the hedge about unmeasured customer benefit
- Reads like a specific engineer wrote it, not a template
- Adds no facts

## Hard checks

- ✓ wrote draft-v2.md
- ✓ slop_scan --strict finds nothing in draft-v2.md
- ✓ keeps the unmeasured hedge

## Met

- Wrote draft-v2.md
- slop_scan --strict reported no findings on draft-v2.md
- Kept the hedge that faster payment for customers has not been measured
- Removed the inflated opener, the chatbot sign-off with emoji and offer to answer questions, the vague 'Experts agree' attribution and the negative parallelism
- Reported that numbers and engine features were unchanged
- Told the user that the former 'Experts agree' claim now stands as a plain statement and should be checked, rather than hiding the change

## Missed

- The transcript does not show the draft-v2 text, so the engineer voice, the absence of added facts and the removal of em dashes and forced threes rest on the scanner and the agent's own summary rather than on visible output
- The agent kept the unsourced late-invoice cash-flow claim as a flat assertion instead of removing or softening it, though it did flag this to the user

## Defects to fix in the skill

- The skill gives no rule for vague-attribution claims: it should say whether to drop the claim, soften it, or keep it and flag it
- The scanner checks only surface patterns, so nothing in the skill checks whether the rewrite reads like a specific engineer or has added facts

## What it did

1. `Skill: straight-prose`
1. `Read: /tmp/run-straight-prose-ekf1ej5s/project/draft.md`
1. `Write: /tmp/run-straight-prose-ekf1ej5s/project/draft-v2.md`
1. `Bash: cd /tmp/run-straight-prose-ekf1ej5s/project/.claude/skills/straight-prose && python3 -I scripts/slop_scan.py /tmp/run-straight-prose-ekf1ej5s/project/draft-v2.m`

## Files it wrote

Copied under `files/`:

- `draft-v2.md`

## Final output

I saved the rewrite as `draft-v2.md`. The scanner found nothing to flag.

I cut the opening about "today's fast-paced digital landscape" and the closing "excited to continue this journey" line with the emoji and the offer to answer questions. I also dropped "Experts agree that late invoices hurt cash flow" because nothing backs it up. The point now reads as a plain statement that late invoices hurt customers' cash flow, so check that you're happy making that claim yourself. The "not just faster, it's smarter" line is gone too.

All the numbers and the new engine's features are unchanged. The caveat that you haven't measured whether customers get paid sooner is still in.

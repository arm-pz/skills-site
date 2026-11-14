# straight-prose: real-world run, 2026-11-13

**Verdict: PASS** (8/10). The run wrote draft-v2.md, a roughly 110-word rewrite, and the scan was reported clean. It keeps the 40,000/day, about-3x month-end, up-to-six-hours, 38-minute and 5h50m figures plus the unmeasured-benefit hedge, and drops the chatbot opener, sign-off, emoji and 'not just faster, it's smarter' line.

Target: a 200-word product blog post with stock AI-writing patterns. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 11 s, $0.1).
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

- Removed the inflated opener, the promotional 'journey' sign-off, the emoji and the 'not just … it's' parallelism; the output has no em dashes
- Dropped the vague 'Experts agree' attribution and told the user that the remaining claim, that late invoices hurt cash flow, is now stated plainly and needs their sign-off
- Kept the numbers (40,000 invoices/day, about 3x month-end volume, up to six hours late, 38 minutes vs 5h50m) and the hedge that benefit to customers is not yet measured
- Hard checks pass: draft-v2.md was written, slop_scan --strict was run on it and reported clean, and the hedge is present
- Plain, concrete prose in a first-person-plural engineering voice, with no template phrasing

## Missed

- The original draft.md is not in the transcript, so I could not verify every fact. 'Customers noticed' may be a small added claim, and the cash-flow statement was converted from an attributed claim into an unattributed one
- The voice is clean but fairly neutral and short; it does not clearly read as one specific engineer, and the feature list is still a three-item series

## Defects to fix in the skill

- The skill does not say what to do with a claim whose vague attribution is stripped: keep it as an unsupported assertion, soften it, or drop it. This run kept it and only flagged it afterward
- Nothing in the skill checks the rewrite against the source for added facts, such as a diff of numbers and claims, so a phrase like 'Customers noticed' can slip in unchecked

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

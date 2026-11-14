# wordsmith: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run wrote draft-tight.md, kept 40,000, triples, up to six hours, 38 min vs 5h50 and the unmeasured-benefit hedge, and cut most fluff, but left 'Experts agree' in the file and the summary says the cut list is mostly complete.

Target: a 200-word product blog post draft with clichés, hedges and real numbers. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.09).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Tighten draft.md. Keep my facts, my numbers and my hedges exactly as strong or weak as they are; cut the fluff. Save it as draft-tight.md and list what you cut.
```

## Rubric

- Cuts the opening cliché, 'testament', 'reimagined', 'not just … it's', 'Experts agree', the emoji sign-off
- Keeps every number (40,000/day, triples, up to six hours, 38 minutes vs 5h50) unchanged
- Keeps the hedge 'may help some customers … not measured yet' at the same strength
- Adds no new claims
- Result is noticeably shorter and still reads in the author's voice

## Hard checks

- ✓ wrote draft-tight.md
- ✓ keeps the hedge that the customer benefit is unmeasured
- ✓ keeps 38 minutes
- ✓ keeps 40,000

## Met

- Wrote draft-tight.md
- Cut the opening cliché, 'testament', 'reimagined', 'not just … it's' constructions and the emoji sign-off
- Kept all numbers unchanged: 40,000/day, roughly triples, up to six hours, 38 minutes vs 5 hours 50 minutes
- Kept the hedge 'may help some customers … we have not measured that yet' at the same strength
- Added no new claims; result is noticeably shorter and still plain in the author's voice

## Missed

- Rubric requires cutting 'Experts agree', but the output still contains 'Experts agree that late invoices hurt cash flow'; the run flagged it rather than cutting it, contradicting the user's 'cut the fluff' instruction and the rubric
- The 'What I cut' list does not mention that 'Experts agree' stayed in as a cut item, so the list is accurate only because it is under 'Flag'; a reader skimming the cut list may assume it is gone
- Minor: 'Customers noticed.' and the 'Let us know if you have any questions.' filler were retained, and the opening 'shows customers how much a business values them' is a paraphrase of the cliché rather than a clean cut, which risks slightly altering the author's claim

## Defects to fix in the skill

- The skill does not tell the agent to treat unsupported authority appeals like 'Experts agree' as fluff to cut by default, so it kept it and only flagged it
- The skill lacks guidance on when to keep a vague claim versus cut it, leaving the agent to rationalise keeping it as 'your claim'
- The skill does not require rewriting an opening cliché to be removed rather than paraphrased, so the opener's meaning was reworded and could introduce a new claim ('shows customers how much a business values them')

## What it did

1. `Skill: wordsmith`
1. `Read: /tmp/run-wordsmith-g0h22lmo/project/draft.md`
1. `Write: /tmp/run-wordsmith-g0h22lmo/project/draft-tight.md`

## Files it wrote

Copied under `files/`:

- `draft-tight.md`

## Final output

I saved the tightened version as `draft-tight.md`. The change is about 40% shorter.

**What I cut**
- **Opening:** I cut "In today's fast-paced digital landscape, invoicing is more than just a task — it's a testament to…". I kept its point in one plain sentence.
- **Rebuild line:** "we didn't just rebuild our engine; we reimagined it from the ground up" became "we rebuilt our engine from the ground up."
- **Adjectives:** I cut "not just faster — it's smarter, more reliable, and more scalable." The queuing, retries, visibility and timing figures already make the case.
- **Closing:** I cut "Moving forward, we're excited to continue this journey with you! 🚀" and "we're always happy to help!". I kept "Let us know if you have any questions."

**Left as written**
- All numbers: 40,000 a day, roughly triples, up to six hours late, 38 minutes vs 5 hours 50 minutes.
- The hedges: "about", "roughly", "up to", "In testing", and "may help… a little sooner, although we have not measured that yet."

**Flag:** I kept "Experts agree that late invoices hurt cash flow" because it's your claim. It's vague, though. A named source or figure would make it stronger.

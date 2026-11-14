# wordsmith: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run wrote draft-tight.md about 40% shorter, kept 40,000, 'roughly triples', 'up to six hours', 38 minutes vs 5h50 and the 'not measured yet' hedge, but left 'Experts agree' in the text despite the rubric requiring it cut.

Target: a 200-word product blog post draft with clichés, hedges and real numbers. Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.11).
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

- Cut the opening cliché 'In today's fast-paced digital landscape'
- Cut 'testament', 'reimagined' and 'not just … it's' constructions
- Cut the emoji sign-off (🚀) and the 'Moving forward, we're excited' closing
- Kept all numbers unchanged: 40,000/day, roughly triples, up to six hours, 38 minutes vs 5 hours 50 minutes
- Kept the hedge 'may help some customers get paid a little sooner, although we have not measured that yet' at the same strength
- Added no new claims
- Result is noticeably shorter and reads plainly in the author's voice
- Wrote draft-tight.md and listed what was cut

## Missed

- 'Experts agree that late invoices hurt cash flow' was kept in the output. The rubric expects it cut as filler/unsourced authority. The run only flagged it as vague rather than removing it.
- The cut list in the final message does not mention the 'Experts agree' sentence as a cut, and the run did not list the several smaller trims (e.g. the opening sentence rewritten as 'shows customers how much a business values them') in detail.
- The rewritten opening sentence 'Invoicing shows customers how much a business values them' is a paraphrase of the cliché's point and arguably introduces a new claim not in the plain facts.

## Defects to fix in the skill

- The skill does not tell the agent to treat vague authority appeals ('Experts agree') as cliché/filler to cut, so it preserved the phrase under 'keep my facts' and only flagged it.
- The skill gives no guidance on distinguishing a user's facts from filler attributions, leaving ambiguity about when unsourced claims should be cut versus kept.
- The skill does not require the cut list to enumerate every removed phrase, so the report is a summary rather than a complete list.

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

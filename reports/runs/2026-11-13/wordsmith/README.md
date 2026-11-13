# wordsmith: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The skill wrote draft-tight.md about 40% shorter, kept 40,000/day, roughly triples, up to six hours, 38 minutes vs 5h50 and the unmeasured-benefit hedge, but it left 'Experts agree' in place, which the rubric required cutting.

Target: a 200-word product blog post draft with clichés, hedges and real numbers. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.07).
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

- Cuts the opening cliché and 'testament'
- Cuts 'reimagined' (now 'rebuilt our engine from the ground up')
- Cuts 'not just … it's smarter, more reliable, more scalable'
- Cuts the emoji sign-off (🚀) and the excited closing
- Keeps all numbers unchanged (40,000 a day, roughly triples, up to six hours, 38 minutes vs 5 hours 50 minutes)
- Keeps the hedge 'may help… a little sooner, although we have not measured that yet' at the same strength
- Adds no new claims, as far as the summary shows
- Result is reported as about 40% shorter, with a list of cuts provided

## Missed

- Did not cut 'Experts agree'; kept it deliberately as the author's claim and only flagged it as vague, though the rubric lists it among the clichés to remove
- The 40% shorter figure is the agent's own claim; the transcript shows no word count, and the file contents were not checked

## Defects to fix in the skill

- The skill gives no guidance on stock authority-appeal phrases such as 'Experts agree'. The agent treated one as protected author content instead of filler to cut or flag, so the skill should list unsourced-authority openers as cut targets.
- The skill does not require checking the saved output, for example by comparing word counts, so the reported percentage is unverified.

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

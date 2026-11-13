# strategy-memo: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The memo recommends multi-entity first (8 vs 10 engineer-weeks) with a pre-sell test, uses most supplied figures and flags gaps honestly, but its headline ~+£2.7k MRR upside rests on an invented assumption and the 90-day plan does not pick a single metric that proves the call right.

Target: a real-shaped build decision for a 3-person fintech startup (QuickBooks vs multi-entity). Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 42 s, $0.17).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Read situation.md and write me the decision memo for the board: which do we build next quarter?
```

## Rubric

- Makes one clear recommendation with the reasoning a board can check
- Uses the numbers given (58 vs ~20 waitlist pace, 10 vs 8 engineer-weeks, 2 churned to QuickBooks, 4 multi-entity asks, ~£900 plan, 14 months runway, 9% MoM) and does the arithmetic right
- Names the strongest case for the option not chosen and what would change the call
- Gives a 90-day plan and the metric that proves it right or wrong
- Invents no market data; anything it would need is listed as an open question

## Hard checks


## Met

- Makes one clear recommendation (multi-entity first, with a pre-board pre-sell test) and gives reasoning a board can check
- Uses the supplied numbers: 58 vs ~20 waitlist, 10 vs 8 engineer-weeks, 2 churned to QuickBooks, 4 multi-entity asks, ~£900 plan, 14 months runway, 9% MoM; basic arithmetic (6,900/31 ≈ £223, 2/31 ≈ 6%, 10+8=18) is correct
- Names the strongest case for QuickBooks in a dedicated Dissent section and lists explicit flip conditions (fewer than 3 of 4 commit, waitlist conversion ≥ ~21%, churned MRR large, further churn)
- Provides a 90-day plan with owners, milestones and metrics, plus 1-year and 3-year horizons
- Invents no external market data; market size and competitor coverage are listed as gaps and handed off to research-brief

## Missed

- The headline upside (~+£2.7k MRR, ~39% of MRR) rests on an assumed £223 current price for the 4 customers (4 × (900−223) ≈ £2,708). It is labelled [assumed], but it drives the recommendation and is not in the situation file
- The ~21% / ~12-customer flip threshold assumes QuickBooks users pay the same £223 ARPA, which is also an assumption; the comparison is built on it
- Several 'metrics' in the 90-day plan are unfilled placeholders ('supply this'), and no single metric is named as the one that proves the call right or wrong; the closest is commitments from the 4 (target 3+) versus the ~12 waitlist payers threshold
- The ~13-week quarter, the month-5 runway threshold of 9 months, and the 'target 3+' are invented parameters, though marked [assumed]
- Runway (14 months) and 9% MoM growth are restated but not used in any reasoning or calculation
- The 3-year section is mostly placeholders and adds little; the memo also carries a research-brief handoff block not requested for a board memo

## Defects to fix in the skill

- The skill's template pushes placeholders ('supply this') into the 90-day metric slots instead of requiring one concrete proof metric with a threshold from the supplied data
- The skill mandates 1-year and 3-year sections even when the situation gives no basis for them, producing filler placeholders in a board memo
- The skill does not require using every supplied figure (runway, MoM growth) in the argument, so those figures are only restated
- The skill appends a handoff block to another skill into the memo file, putting non-board content in the deliverable

## What it did

1. `Skill: strategy-memo`
1. `Read: /tmp/run-strategy-memo-r4chgu88/project/situation.md`
1. `Write: /tmp/run-strategy-memo-r4chgu88/project/strategy-memo.md`

## Files it wrote

Copied under `files/`:

- `strategy-memo.md`

## Final output

I've written the board memo to `strategy-memo.md`. It recommends building multi-entity first, but with low-to-medium confidence, because the data is thin.

- **Why multi-entity:** It's cheaper (8 engineer-weeks against 10). The demand comes from four paying customers, and the £900 plan is already priced. If all four upgrade and currently pay the £223 average, that's about +£2.7k MRR, roughly 39% of today's £6.9k. That assumes all four convert and that they pay the average today, and I don't have their actual plan prices.
- **What would flip it to QuickBooks:** QuickBooks only matches that upside if about 21% of the 58 waitlist sign-ups (about 12 customers) pay. That also assumes QuickBooks users pay the same average as Xero users. Sign-ups haven't been asked to pay, so the memo proposes a pre-sell test over the next three weeks. It would ask the four customers for a commitment at £900 and offer the waitlist a priced founding-customer deal. Fewer than 3 of the 4 committing, or 12 or more paying from the waitlist, would reverse the pick.
- **The dissent section:** Both customers you lost went to QuickBooks, and waitlist demand is about three times the Xero launch pace. The memo says plainly that this argues for QuickBooks first.
- **What's missing:** Several figures are marked as slots for you to fill, and they are listed under Gaps. The most important are what the four multi-entity customers pay now and how much MRR the two churned customers represented.
- **Roadmap:** It covers ninety days, one year and three years. I left the owners as "founders" or "engineer" in places, because I don't know who does what.

I also put a research-brief handoff at the end for sizing the QuickBooks market and checking competitors. I didn't assert any market facts myself.

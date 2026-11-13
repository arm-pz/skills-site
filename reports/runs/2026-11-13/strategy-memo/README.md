# strategy-memo: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run read situation.md and wrote strategy-memo.md recommending multi-entity (8 vs 10 engineer-weeks) at low-to-medium confidence. The checkable arithmetic holds (4×(£900−£223)≈£2.7k, about 39% of £6.9k MRR; 21% of 58≈12 sign-ups; 58 vs ~20 is about 3x), but the memo's contents and use of runway and growth were not visible.

Target: a real-shaped build decision for a 3-person fintech startup (QuickBooks vs multi-entity). Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 42 s, $0.13).
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

- One clear recommendation (multi-entity first) with reasoning a board can check: cheaper build, four paying asks, plan already priced
- Arithmetic in the summary is internally consistent: +£2.7k MRR is about 39% of £6.9k, and the QuickBooks break-even is about 21% of 58 sign-ups, roughly 12 customers
- Strongest case for QuickBooks is given in a dissent section (2 churned to QuickBooks, waitlist pace about 3x the Xero launch), along with explicit flip conditions: fewer than 3 of 4 committing, or 12 or more paying from the waitlist
- 90-day plan with a pre-sell test over about three weeks and pass/fail thresholds that prove the call right or wrong
- No market facts asserted; missing inputs are listed under Gaps (what the four customers pay now, MRR of the two churned customers) and a research-brief handoff covers QuickBooks market sizing and competitors

## Missed

- The final output never mentions the 14 months runway or 9% MoM growth, so use of those given numbers could not be confirmed
- The £223 average and £6.9k MRR could not be traced to situation.md from the transcript; if they were derived or assumed rather than given, they risk being invented
- Owners in the roadmap are left generic ('founders', 'engineer'), and the 1-year and 3-year roadmap goes beyond the requested decision memo

## Defects to fix in the skill

- The skill does not require the memo to use every provided figure explicitly (runway and growth rate) or to state which figures came from the source file and which were derived
- The skill adds a multi-horizon roadmap (90 days, 1 year, 3 years) and a research handoff by default, which pads a focused one-decision board memo

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

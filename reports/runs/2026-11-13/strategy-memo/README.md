# strategy-memo: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The memo recommends multi-entity first (8 vs 10 engineer-weeks) with a pre-sell test to flip it, uses most supplied figures and has a 90-day plan, but the central upside number (+£2.7k MRR) rests on an invented £223 average price for the 4 requesters and the 14-month runway and 9% MoM are barely used in the reasoning.

Target: a real-shaped build decision for a 3-person fintech startup (QuickBooks vs multi-entity). Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 3 tool calls, 42 s, $0.21).
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

- One clear recommendation (multi-entity first, QuickBooks next quarter) with ranked options and stated confidence
- Strongest case for QuickBooks is given in a dedicated Dissent section, plus explicit flip conditions (fewer than 3 of 4 commit, waitlist conversion of about 12 or more, churned MRR large)
- 90-day plan with owners, milestones and metrics, and a named proving metric (commitments from the 4, waitlist payers vs ~12 threshold)
- No external market data asserted; market size and competitor coverage are listed as gaps and deferred to research-brief
- Most supplied figures used: 58 vs ~20 waitlist, 10 vs 8 weeks, 2 churned, 4 asks, £900 plan, 14 months, 9% MoM; 6,900/31 ≈ £223 and 2/31 ≈ 6% are correct

## Missed

- Headline upside of +£2.7k MRR (+39%) depends on an assumed £223 current price for the 4 requesters; the real current price is unknown, so the figure is a scenario presented as the main justification. It is flagged as assumed, but the recommendation leans on it
- Arithmetic is shaky in places: (900-223)*4 ≈ £2.7k is fine, but the '12 customers ≈ 21% of waitlist' flip threshold compares gross QuickBooks MRR with incremental multi-entity MRR, and 2 churned of 31 is 'about 6%' while the dissent says '100% of the churn' with no total churn base given
- Runway (14 months) is only used as a vague checkpoint 'above 9 at month 5' with an invented threshold; the 9% MoM growth is not used to project anything or tie the decision to runway
- Invented details: a ~13-week quarter, the 'month 5 runway above 9' threshold, and a 'week 10 beta' schedule, though most are labelled assumed
- Pre-board test of 3 weeks overlaps with a 90-day plan that starts from the board decision, which muddles the timeline; board meeting date '3 weeks from 2026-11-13' may be taken from the file but is not verified here
- Includes 1-year and 3-year sections with many unsupported slots, which pads the memo beyond the ask

## Defects to fix in the skill

- The skill's template forces a 1-year and 3-year roadmap even when the decision is a single-quarter build, producing placeholder-heavy filler
- No instruction to anchor the recommendation on the supplied runway and growth figures (for example a simple projection), so they are mentioned but not used in the reasoning
- The skill lets a derived 'assumed' price drive the headline number instead of requiring the memo to lead with what is actually known and treat the assumption only as a sensitivity
- The unconditional research-brief handoff block is appended inside the deliverable file, polluting a board-facing memo

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

# Checkout test readout: B probably did win, on mobile only

**Don't kill B yet.** Your PM's "flat" comes from a data problem, not from the test.

## Executive summary
- **Pooled result looks flat.** Orders per session were 3.89% for A and 3.95% for B (+0.06 pts, p = 0.48). That is the number behind "flat".
- **The B arm logged zero orders on 2026-10-09**, on both mobile and desktop, while A was normal that day. That looks like a tracking or deploy outage. It is not a real conversion drop. Those 4 rows (8,000 B sessions, $0 revenue) dilute B's result.
- **With 10-09 dropped from both arms, B wins.** B converts at 4.25% against 3.89% for A: +0.37 pts, a 9.4% relative lift (95% CI +0.18 to +0.55 pts, p = 0.0001).
- **The lift is entirely mobile.** Mobile conversion went from 3.01% to 3.70% (+0.69 pts, +22.8% relative, 95% CI +0.47 to +0.91, p < 0.0001). Desktop is flat to slightly negative: 5.29% to 5.14% (−0.15 pts, CI −0.49 to +0.19, p = 0.40).
- **Decision:** Confirm what happened on 10-09. If it was an outage, B beat control on mobile. I'd ship B to mobile and keep a desktop holdout.

## The data
- Source is `checkout_test.csv`: 56 rows, 2026-10-01 to 2026-10-14 (14 days), one row per day × variant × device. There are no missing values.
- Traffic is split evenly: 91,000 sessions per arm, with mobile at 4,000/day and desktop at 2,500/day in each arm.
- I excluded 2026-10-09 for both arms and both devices. It is the only day with zeros, so it is the clearest anomaly in the file. Excluding it keeps the comparison balanced (84,500 sessions per arm).

## Findings, ranked by impact

**1. B's 10-09 zeros are almost certainly a measurement or deploy fault. (Observed that the zeros exist; Inferred that it's an outage.)**
- Two device rows with 4,000 and 2,500 sessions and exactly 0 orders and $0 revenue is not plausible organic behavior. Daily B orders run roughly 120–160 per device on every other day.
- Business implication: this one day turns a significant win into an apparent tie.
- Confidence: high that the data is bad, low on the cause.
- Check: engineering looks at checkout errors, deploys and event-logging on 10-09. If B actually broke for a day, that is a real reliability finding about B, and it argues for fixing B rather than killing it.

**2. Conversion on mobile rose about 23% relative. (Observed)**
- Orders were 1,923 for B against 1,566 for A on 52,000 sessions each. That is +0.69 pts, p < 0.0001, 95% CI +0.47 to +0.91 pts.
- Revenue per session on mobile was $1.51 for B against $1.24 for A, a lift of about 22%. I did not run a significance test on revenue per session.
- Business implication: mobile is where the checkout redesign pays off.
- Confidence: high. The effect is large and shows up on nearly every day (B mobile is above A mobile on all 13 clean days).

**3. Desktop shows no benefit, and a small harm can't be ruled out. (Observed)**
- Desktop conversion was 5.14% for B against 5.29% for A. The CI of −0.49 to +0.19 pts includes zero, so this is inconclusive.
- The data can't separate "no effect" from "mildly worse". Desktop is also the higher-value segment, at about $64 per order against about $41 on mobile.
- Business implication: a full rollout carries some risk on desktop.
- Confidence: medium-low. The test was powered for the pooled result, not for desktop alone.

**4. Order value is unchanged. (Observed)**
- Average order value is about $51.7 for B against $53.1 for A pooled, and flat within each device. The mobile lift comes from more orders, not bigger baskets. The pooled gap is a mix effect from more mobile orders.

## Actions
| Action | Rests on | Owner | Metric |
|---|---|---|---|
| Investigate 10-09 B logging or outage | Finding 1 | Engineering / analytics | Whether the zeros are a tracking gap or a real failure |
| Don't kill B. Ship B to mobile, keep desktop on A or a holdout | Findings 2–3 | PM | Mobile orders per session |
| Re-run or extend desktop to resolve the open question | Finding 3 | Experimentation | Desktop orders per session; guardrail on desktop revenue per session |
| Agree on one primary metric and the exclusion rule before the next test | Findings 1–2 | PM + analytics | n/a |

If the 10-09 cause turns out to be a real B failure, the call changes. You'd fix that fault, then re-test or extend before rolling out.

## Chart specs
1. **Daily orders per session by variant, one panel per device.** X is date. Y is orders ÷ sessions, starting at 0. Use two lines (A and B), with B's 10-09 point marked and annotated "zero orders, suspected outage". Small multiples are needed because the pooled view hides the mobile/desktop split. This chart shows the mobile gap and the outage together.
2. **Lift by segment.** Show Pooled (all days), Pooled (excl. 10-09), Mobile and Desktop as rows. Plot the relative or absolute lift as a dot with the 95% CI as a horizontal bar, and draw a reference line at 0. This is the chart that settles the argument with your PM.

## Assumptions and caveats
- I treated each day-device row as aggregate counts and used a two-proportion z-test. That assumes sessions convert independently. The file has no user IDs, so repeat visitors and clustering could make the real CIs wider.
- Random assignment, a sample-ratio check and the pre-registered primary metric are not in the file, so I can't verify them. Sessions are exactly equal across arms every day, which looks designed or capped rather than organic.
- Splitting by device is a post-hoc cut. It is plausible, because the redesign is more likely to matter on mobile, but it is a subgroup finding that deserves confirmation. Treat the desktop null as undecided.
- The mobile lift holds on every clean day, and the pooled lift holds with 10-09 out. I haven't tested other exclusion choices, such as dropping every day touched by a deploy.
- I did not check for novelty effects (the lift shrinking over the two weeks) or for day-of-week effects.

## Gaps
- The cause of the 10-09 B zeros.
- Whether the primary metric was orders per session or revenue.
- Whether mobile and desktop were planned as separate cuts.
- Significance for revenue per session. I give the point estimates only.
- Downstream metrics such as refunds, checkout errors and return rate.

I can write the pandas script behind these numbers if you want it.
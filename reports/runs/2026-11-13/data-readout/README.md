# data-readout: real-world run, 2026-11-13

**Verdict: PASS** (9/10). The run found B's zero orders on 2026-10-09 on both devices, excluded that day, and reported B beating A overall (4.25% vs 3.89%, +9.4%, p=0.0001), with mobile +22.8% (p<0.0001) and desktop flat (−0.15 pts, p=0.40), all matching ground truth.

Target: a 14-day checkout A/B test export (182,000 sessions, two devices) with one planted tracking outage. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 37 s, $0.12).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
We ran a checkout redesign test for two weeks. Export is in checkout_test.csv (variant A = control, B = new checkout). My PM says the result is flat and we should kill B. Did B win? What should we do?
```

## Rubric

- Finds that variant B recorded zero orders on 2026-10-09 on both devices and treats it as a tracking or data fault, not real behaviour
- Recomputes the comparison without the faulty day and reports that B beats A overall with a significance figure close to the ground truth
- Splits by device: B clearly wins on mobile; desktop shows no significant difference once the outage is removed
- Recommends an action that follows from the numbers (e.g. do not kill B; ship on mobile, keep testing or ship on desktop, fix tracking) and states what it could not compute
- Every number it states matches the ground truth or is derived from the file; nothing invented

## Hard checks

- ✓ names the day-9 gap in variant B
- ✓ reports a mobile-specific result

## Met

- Identifies B's zero orders on 2026-10-09 on both devices (4 rows, 8,000 sessions, $0 revenue) and treats it as a likely tracking or deploy fault, labelling the cause as inferred and unconfirmed
- Recomputes without the faulty day: A 3.89% vs B 4.25%, +9.4% relative, p=0.0001, matching the ground truth of z 3.80 and p 0.0001
- Splits by device: mobile 3.01% to 3.70% (+22.8%, p<0.0001) and desktop 5.29% to 5.14% (p=0.40), matching the ground truth
- Recommends not killing B, shipping on mobile with a desktop holdout, investigating the 10-09 outage and extending the desktop test; the gaps section lists what it did not compute (revenue-per-session significance, outage cause, novelty and day-of-week effects)
- Stated numbers match the ground truth or derive from the file (1,923 vs 1,566 mobile orders, 84,500 and 52,000 sessions per arm, 91,000 per arm overall); the pooled all-days figures of 3.89% vs 3.95% and p=0.48 also match

## Missed

- Does not report the all-days desktop result (B −9.4%, p=0.0026) that appears as significant harm before the outage is removed; it only reports the cleaned desktop figure
- Several derived figures (revenue per session of $1.51 vs $1.24, AOV, "B above A on all 13 clean days", about $64 vs $41 per order) are not in the ground truth and cannot be verified from the transcript excerpt, though they are plausibly computed from the file

## Defects to fix in the skill

- The skill does not require stating the all-days per-device numbers alongside the cleaned ones, so the apparent desktop harm created by the outage goes unmentioned
- The 'ship on mobile' recommendation is stated as firm in the summary while the outage cause is still unconfirmed; the skill could require the recommendation to be conditional on the fault being confirmed

## Ground truth

```
all      all days    A 0.0388 (3535/91000)  B 0.0395 (3594/91000)  lift +1.7%  z 0.71  p 0.4759
all      excl day 9  A 0.0389 (3285/84500)  B 0.0425 (3594/84500)  lift +9.4%  z 3.80  p 0.0001
mobile   all days    A 0.0302 (1690/56000)  B 0.0343 (1923/56000)  lift +13.8%  z 3.94  p 0.0001
mobile   excl day 9  A 0.0301 (1566/52000)  B 0.0370 (1923/52000)  lift +22.8%  z 6.15  p 0.0000
desktop  all days    A 0.0527 (1845/35000)  B 0.0477 (1671/35000)  lift -9.4%  z -3.01  p 0.0026
desktop  excl day 9  A 0.0529 (1719/32500)  B 0.0514 (1671/32500)  lift -2.8%  z -0.85  p 0.3971
day 9, variant B orders: ['0', '0'] (tracking outage planted)
```

## What it did

1. `Skill: data-readout`
1. `Bash: ls -la && head -5 checkout_test.csv && wc -l checkout_test.csv`
1. `Bash: cat checkout_test.csv | head -60; ls .claude/skills/data-readout/references`
1. `Bash: python3 -I - <<'E'
import csv,math
R=list(csv.DictReader(open('checkout_test.csv')))
for r in R:
    for k in('sessions','orders'):r[k]=int(r[k])
    r['revenue`

## Final output

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

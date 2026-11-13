# Ledgerline board memo: QuickBooks or multi-entity next quarter

## 0. The decision requested

Choose the single build for next quarter: **QuickBooks support (~10 engineer-weeks)** or **multi-entity for Xero (~8 engineer-weeks)**. Decided by the board at the meeting in 3 weeks (from 2026-11-13). `[supplied]`

## 1. Situation analysis

- Product: Reconcile, payout-to-invoice matching for Xero. `[supplied]`
- 31 customers, £6.9k MRR, ~9% MoM growth, 14 months runway, 2 founders + 1 engineer. `[supplied]`
- Average revenue per customer ≈ £223/month (6,900 / 31). `[derived from supplied figures]`
- QuickBooks demand: 58 waitlist sign-ups in 6 weeks, against ~20 for Xero in the same period at launch. `[supplied]` Sign-ups are not payers; the share who would pay is `[waitlist-to-paid conversion — supply this]`.
- Multi-entity: 4 current customers asked, for Xero accounts above 5,000 invoices/month. It would support a ~£900/month plan. `[supplied]` What those 4 pay today is `[current plan price of the 4 — supply this]`.
- Churn: 2 customers lost in 6 months, both citing a move to QuickBooks. `[supplied]` That is about 6% of the base in 6 months. `[derived]` Their MRR is `[MRR of the 2 churned — supply this]`.
- Capacity: one engineer. A quarter is about 13 weeks `[assumed]`, so only one option fits (10 + 8 = 18 weeks).

**Arithmetic on what each option has to deliver** (all conversion figures are scenarios, not forecasts):

| | Multi-entity | QuickBooks |
| --- | --- | --- |
| Engineer-weeks | 8 | 10 |
| Upside if the 4 asking customers all move to £900 and currently pay the average £223 `[assumed]` | ≈ +£2.7k MRR (≈ +39% of today's MRR) | n/a |
| Customers needed to match that at £223 ARPA `[assumed QuickBooks users pay the same as Xero users]` | n/a | ≈ 12 customers, i.e. ≈ 21% of the current 58 waitlist |
| Evidence strength | 4 paying customers, a named price point | 58 sign-ups that have not been asked to pay |
| Other effect | Raises ARPA; no new platform | May stop QuickBooks-driven churn and opens a second market |

## 2. Recommendation

**Build multi-entity first, with a pre-sell test on the QuickBooks waitlist before the board meets, which can overturn this.**

| Rank | Option | Plausible effect | Tradeoff | Data needed |
| --- | --- | --- | --- | --- |
| 1 | Multi-entity now, QuickBooks the following quarter | Up to ~+£2.7k MRR from customers who have already asked (if all 4 convert); shipping is cheaper and less uncertain | Another quarter in which QuickBooks-minded prospects and customers can leave; the waitlist cools | [willingness of the 4 to commit at £900 — supply this] |
| 2 | QuickBooks now, multi-entity later | Opens a second market and may cut churn; waitlist is ~3x the Xero launch pace | Biggest bet on the least-validated demand; new-platform risk; delays a near-certain upgrade | [waitlist-to-paid conversion — supply this]; [QuickBooks API fit and integration risk — supply this] |
| 3 | Split the quarter (both, partial) | Hedges | 18 weeks of work in ~13 with one engineer; risks shipping neither well | [engineer availability — supply this] |

Confidence: **medium-low**. Multi-entity wins only if most of the 4 requesters will commit at the new price. QuickBooks wins if at least ~21% of the waitlist (≈12 customers) would pay roughly current ARPA, or if the churned customers were large `[figures needed above]`.

**What would change my mind:** (a) fewer than 3 of the 4 will commit to the £900 plan; (b) a pre-sell to the waitlist converts at or above ~21%; (c) the 2 churned customers' MRR is a large share of £6.9k, which would make churn defence the priority; (d) a further QuickBooks-attributed churn before the board meeting.

**Pre-board test (next 3 weeks, cheap):** ask the 4 customers for a written commitment or deposit at £900; email the 58 with a priced founding-customer offer and count paid or deposit responses.

Owner: a founder runs both tests `[assumed which founder — supply this]`. Metrics: commitments from the 4 (target 3+); paid/deposit conversions from the waitlist (flip threshold ≈ 12).

## 3. Execution roadmap

**Ninety days** (assuming multi-entity wins)

| Line | Owner | Milestone | Metric |
| --- | --- | --- | --- |
| Weeks 1–2: run the two pre-sell tests; confirm scope with the 4 customers; pull MRR for the 2 churned accounts; spec multi-entity | Founders / engineer | Board gets real numbers | Commitments from the 4; waitlist payers; data gaps closed |
| Weeks 3–10: build multi-entity | Engineer | Beta with the 4 | Beta live by ~week 10; matching accuracy on 5,000+ invoice/month accounts `[measurement — supply this]` |
| Weeks 10–13: launch £900 plan, migrate the 4, scope QuickBooks (API fit, data model) | Founder | Plan live | MRR uplift vs ~£2.7k scenario; QuickBooks scoping doc done |
| Keep the waitlist warm with a dated update | Founder | Monthly email | Waitlist churn/unsubscribes `[measurement — supply this]` |

**One year:** ship QuickBooks (~10 weeks) in the following quarter, with waitlist pre-sold. Owner: engineer, with a founder on launch. Metric: QuickBooks paying customers and QuickBooks-attributed churn at zero. Hold the ~9% MoM growth rate `[supplied]`; the target is `[growth target — supply this]`. Runway checkpoint: months of runway above 9 at month 5 `[assumed threshold]`.

**Three year:** Ledgerline as a multi-platform reconciliation product (Xero, QuickBooks, `[others — supply this]`) with a mid-market tier. Owners: founders. Metrics: `[3-year ARR target — supply this]`, share of MRR from the £900 tier, hiring plan beyond one engineer.

## 4. Assumptions and open questions

Assumptions: a quarter is ~13 engineer-weeks; the 4 requesters pay about the average £223 today; QuickBooks users pay the same ARPA as Xero users; build estimates hold; one engineer is the only builder.

Open questions: what the 4 pay today; what the 2 churned customers paid; whether waitlist sign-ups come from the same kind of firm as current customers; whether Xero-only is limiting the 9% growth; whether more of the 31 are at QuickBooks risk.

## 5. Dissent

The strongest case against: the only evidence of *loss* is on the QuickBooks side. Two of the six months' churn, 100% of it, went to QuickBooks, and demand there is about three times the Xero launch pace. Four customers asking for a feature is anecdote; being a Xero-only product in a market that is moving off Xero is structural. Building multi-entity deepens dependence on a platform your own customers are leaving, and for one quarter you trade a wider market for a £900 plan that four accounts may never take up. If the Xero base is shrinking at the edges, upmarket pricing optimises the part of the business with the least future.

## 6. Gaps

- [current plan price of the 4 multi-entity customers — supply this]
- [MRR of the 2 churned customers — supply this]
- [waitlist-to-paid conversion — supply this]
- [willingness of the 4 to commit at £900 — supply this]
- [QuickBooks integration risk and API fit — supply this]
- [matching-accuracy metric for large accounts — supply this]
- [growth and ARR targets — supply this]
- Size of the QuickBooks user market and competitor coverage: external, not asserted here.

HANDOFF — strategy-memo -> research-brief
Goal: size the QuickBooks reconciliation opportunity and check competitor coverage of payout-to-invoice matching
Brief: UK/Xero-adjacent small and mid-size finance teams; decision: QuickBooks vs multi-entity
Evidence: 58 waitlist sign-ups in 6 weeks; 2 churned customers moved to QuickBooks
Assumptions: QuickBooks users pay similar ARPA to Xero users
Gaps: market size, competitor coverage, API constraints
Next: Want me to run research-brief on this?

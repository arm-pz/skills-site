**Decision: HOLD**

List: provider A, 2,400 rows. Sampled 10 (the supplied sample, so I can't confirm it was random). Date: 2026-11-13.

| # | Company | Title | Size fit | Mailbox valid | Note |
|---|---------|-------|----------|---------------|------|
| 1 | Ledgerline | VP Customer Success | 180, yes | yes | Pass |
| 2 | Quillbook | Head of CS | 95, yes | yes | Pass |
| 3 | Fernway | Customer Success Manager | 240, yes | yes | **Fail: wrong seniority.** ICP needs VP, Head, Director or CCO. |
| 4 | Paystack Labs | none (first name "Info") | 320, yes | **no** | **Fail: role inbox** (info@). |
| 5 | Tallyhub | Director of CS | 410, yes | yes | **Fail: current customer**, excluded in the ICP. |
| 6 | Docket | CCO | **2,600** | yes | **Fail: size.** The ICP cap is 500. |
| 7 | Brightline Talent | Head of CS | 60 | yes | **Fail: recruitment agency**, excluded. |
| 8 | Ravelin Data | VP Customer Experience | 130, yes | **no** | **Fail: gmail address.** The company domain is raveldata.example, and the title is also off-spec. |
| 9 | Stackwise | Head of CS | 75, yes | yes | Pass |
| 10 | Penny Lane Software | Director of CS | 220, yes | yes | Pass |

6 of 10 are wrong. The HOLD threshold is 2 or more.

**Fail pattern:** wrong filter. The failures are spread across title seniority, a size ceiling, exclusions (agency, existing customer) and mailbox type. That points to a query that isn't applying the ICP constraints, not one bad data source. Mailbox quality is a secondary problem (a role inbox and a free-mail address).

**Cause:** provider A's query doesn't enforce the 50–500 size band, the seniority floor, the agency and customer exclusions, or the named-work-address requirement.

**Required change:**
- Cap headcount at 500.
- Restrict titles to VP, Head, Director or CCO of Customer Success.
- Exclude agencies and recruiters by industry.
- Suppress Brightfold and Tallyhub.
- Drop role inboxes and free-mail domains.

**Re-run condition:** pull a fresh random 10-row sample after the fix. A HOLD isn't lifted on this sample. I'd also have provider A re-quote the 2,400 count, because the filters will shrink it.

**Provider B:** the README only gives a summary (8 on ICP, 1 role inbox, 1 over 500 employees), not the rows. That is 2 wrong in 10, which is also HOLD by the same rule. It is still much better than A's 4 on ICP. Before treating B as the fallback, I'd request its actual rows and a 50–100 contact comparison against A on the same criteria. I'm not scoring B from a summary.

**Source benchmarks used:** the 10-row sample and the "2 wrong means HOLD" rule come from Will Breton's X article of 18 October 2026. Treat them as a starting threshold, not a law.
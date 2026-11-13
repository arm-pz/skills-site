# cold-email-list-gate: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run returned HOLD after checking all 10 sample rows, correctly finding 4 on ICP and 6 off, with a fail pattern and re-run condition; it misattributed the Ravelin failure, named an unsupported suppression target (Brightfold), and declined to compare provider B on the same criteria.

Target: a 10-row provider sample of a 2,400-row cold-email list against a written ICP. Run headless in a clean project with only this skill installed (7 turns, 5 tool calls, 25 s, $0.09).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
We're about to load a 2,400-lead list from provider A. ICP is in icp.md, the 10-row sample is leads_providerA.csv, and there's a note on provider B in README.md. GO or HOLD?
```

## Rubric

- Checks all 10 rows against company type/size/country, title, mailbox and exclusions, row by row
- Finds exactly 4 rows on ICP (Ledgerline, Quillbook, Stackwise, Penny Lane) and 6 off: Fernway (IC title), Paystack info@ (role inbox), Tallyhub (current customer), Docket (2,600 employees), Brightline Talent (recruitment agency), Ravelin (gmail, and CX not CS title)
- Returns HOLD with the fail pattern and a concrete re-run condition
- Compares provider B (8/10) on the same criteria and says what that implies
- Invents no rows or numbers

## Hard checks

- ✓ returns HOLD

## Met

- Checked all 10 rows in a table against size, title, mailbox and exclusions
- Identified exactly 4 on ICP (Ledgerline, Quillbook, Stackwise, Penny Lane) and 6 off, with the right reason for Fernway, Paystack, Tallyhub, Docket and Brightline
- Returned HOLD (hard check met)
- Gave a fail pattern (wrong filter, mailbox quality secondary) and a concrete re-run condition (fresh random 10-row sample after fix, re-quote the count)
- Provider B: noted 8/10, said it is 2 wrong and also HOLD by the same rule, better than A, and asked for actual rows before treating it as a fallback

## Missed

- Ravelin was labelled a gmail failure with a title note ('VP Customer Experience' off-spec); the rubric expects CX not CS title as a distinct reason. This was only mentioned in passing and was not counted as a title failure, and the 'Size fit' and 'Mailbox valid' columns do not capture it.
- Required change says 'Suppress Brightfold and Tallyhub'; Brightfold is not a row in the sample (the excluded agency was Brightline Talent), which may be an invented or misnamed entry.
- Provider B was not compared on the same criteria; the run explicitly declined to score it and only restated the README summary, so the implication is thin.
- Cited a 'Will Breton X article of 18 October 2026' as the source of the benchmark; the transcript shows no read that supports this beyond the skill's reference file, so provenance is unverified.
- Said the fail pattern is 'wrong filter' while 4 of the 6 failures are individual-row issues; the claim about what the provider's query does ('doesn't enforce the 50-500 band') is inferred beyond the evidence, including a size floor failure that no row demonstrated.

## Defects to fix in the skill

- The skill does not require comparing the fallback provider on the same criteria or stating a clear implication when only a summary is available, so the run stopped at 'request the rows'.
- The skill's output template has no title-fit column or per-row note guidance that forces every failing reason to be listed, so secondary failures like Ravelin's CX title are buried.
- The skill does not instruct the agent to take exclusion names only from the sample/ICP files, which allowed an unsupported name (Brightfold) into the required changes.

## What it did

1. `Skill: cold-email-list-gate`
1. `Read: /tmp/run-cold-email-list-gate-w5d7j69p/project/icp.md`
1. `Read: /tmp/run-cold-email-list-gate-w5d7j69p/project/leads_providerA.csv`
1. `Read: /tmp/run-cold-email-list-gate-w5d7j69p/project/README.md`
1. `Read: /tmp/run-cold-email-list-gate-w5d7j69p/project/.claude/skills/cold-email-list-gate/references/gate-rules.md`

## Final output

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

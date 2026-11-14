# cold-email-list-gate: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). Run returned HOLD after checking all 10 rows of provider A's sample (4 on ICP, 6 off) and mapping each failure, but it mentioned a nonexistent 'Brightfold' suppression, only partly scored provider B, and attributed a benchmark to an external source.

Target: a 10-row provider sample of a 2,400-row cold-email list against a written ICP. Run headless on the CLI default model in a clean project with only this skill installed (7 turns, 5 tool calls, 25 s, $0.13).
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

- Checked all 10 rows row by row against size, title, mailbox and exclusions
- Found exactly the 4 on-ICP rows (Ledgerline, Quillbook, Stackwise, Penny Lane) and the 6 off rows with correct reasons (Fernway seniority, Paystack info@, Tallyhub customer, Docket 2,600, Brightline agency, Ravelin gmail and CX title)
- Returned HOLD with a fail pattern (wrong filter, mailbox secondary) and a concrete re-run condition (fresh random 10-row sample after filter fix, re-quote count)
- Compared provider B (8/10 on ICP) and stated the implication: better than A but still HOLD by the same rule, so request its rows before using it as fallback

## Missed

- Invented or unsupported entity: 'Suppress Brightfold and Tallyhub' names Brightfold, which is not in the sample (likely a mix-up with Brightline Talent or an ICP exclusion list not shown in the transcript)
- Provider B comparison asserts '2 wrong in 10' and 'also HOLD' from a README summary while saying it won't score B from a summary, which is internally inconsistent
- Added a cited external source (Will Breton X article, 18 October 2026) as a benchmark; it was not read in any tool call visible in the transcript, so its provenance is unverified
- Ravelin's CX-vs-CS title issue is noted but the table lists size as 'yes' and the Title column as 'VP Customer Experience' without clearly flagging it as a separate title fail in the Note column header

## Defects to fix in the skill

- Skill output template does not tell the agent to restrict named suppressions to entities actually present in the ICP or sample, allowing a stray name (Brightfold)
- Skill does not specify how to handle provider B when only a summary is available (score it as given vs. refuse), producing an inconsistent stance
- Skill's source-benchmark footer invites citing an external article without a step confirming where that source came from

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

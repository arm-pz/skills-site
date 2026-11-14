# research-brief: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run correctly concluded the user (about £47,000 combined gross income) starts MTD for Income Tax on 6 April 2027 under the £30,000 threshold, cited gov.uk pages and listed the changes, but left the tax-year basis of the test unverified and mixed in details from an unopened search summary.

Target: UK Making Tax Digital for Income Tax: thresholds and dates, from public sources. Run headless in a clean project with only this skill installed (11 turns, 9 tool calls, 58 s, $0.21).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I'm a UK sole trader with about £38,000 of self-employment income plus £9,000 from renting out a flat. When do I have to start using Making Tax Digital for Income Tax, and what exactly changes for me? Cite sources.
```

## Rubric

- States the phased thresholds correctly: qualifying income over £50,000 from 6 April 2026, over £30,000 from 6 April 2027, over £20,000 from 6 April 2028
- Explains that qualifying income is gross self-employment plus property income (here about £47,000), so on current rules this person is in from 6 April 2027 (over £30,000), not 2026 (not over £50,000), and that the test uses the income on an earlier tax return
- Lists what changes: quarterly updates via compatible software, digital records, final declaration
- Ties each claim to a cited primary source (gov.uk) and flags anything uncertain or subject to change
- Invents no thresholds, dates or penalties

## Hard checks

- ✓ cites gov.uk

## Met

- States the phased thresholds correctly: £50k from 6 April 2026, £30k from 6 April 2027, £20k planned from 6 April 2028, with the £20k flagged as planned
- Explains qualifying income is gross self-employment plus property income, concludes 6 April 2027 and not 2026 for this user
- Lists what changes: digital records, quarterly updates via compatible software, final declaration/annual return
- Cites gov.uk primary sources per claim in a table, with confidence levels, conflicts and gaps flagged, and marks search-summary-only claims as such
- Hard check met: cites gov.uk
- No invented thresholds or dates; uncertain items tagged [unverified]/[my inference]

## Missed

- The rubric wants it explained that the test uses income on an earlier tax return; the answer only 'infers' the 2025–26 return and says no page states it explicitly, and its gaps list says the £30k year-basis could not be settled (the 'find out if and when you need to use MTD' fetch failed)
- The summary computes the combined figure as £47,000 but then hedges by treating £38k as possibly turnover or profit; it states an assumption rather than plainly using about £47,000 as asked
- Quarterly deadlines, the £200 at 4 points penalty and the 31 January return rest on a search summary of a page that was never opened, so they are not tied to a read primary source
- The first line says 'I read three GOV.UK pages' yet the claim table credits a fourth fetched page, and the sign-up page was fetched twice, so the account of what was read is slightly muddled

## Defects to fix in the skill

- The skill allows claims to be reported from search summaries without requiring the source page to be opened; it should require fetching the page for any date or penalty figure, or drop the claim
- The skill has no fallback when the key authoritative page (the 'work out if you need to use MTD' guidance) fails to fetch, such as retrying or trying alternative gov.uk URLs, so the earlier-return rule stayed unverified
- The output template is heavy (status line, summary, claim table, conflicts, gaps, sources), which duplicates content for a simple question

## What it did

1. `Skill: research-brief`
1. `ToolSearch: `
1. `WebSearch: `
1. `WebFetch: https://www.gov.uk/guidance/work-out-if-you-need-to-use-making-tax-digital-for-income-tax`
1. `WebFetch: https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax`
1. `WebFetch: https://www.gov.uk/guidance/sign-up-for-making-tax-digital-for-income-tax`
1. `WebFetch: https://www.gov.uk/government/publications/extension-of-making-tax-digital-for-income-tax-self-assessment-to-sole-traders-and-landlords/making-tax-digital-for-i`
1. `WebFetch: https://www.gov.uk/guidance/sign-up-for-making-tax-digital-for-income-tax`
1. `WebSearch: `

## Final output

**STATUS: PARTIAL.** I read three GOV.UK pages with WebFetch. The quarterly dates and penalty rules come only from a search summary, not a page I opened.

**Decision this informs:** when you must start MTD for Income Tax, and what changes. **Assumption:** the £38k is turnover (income before expenses). You haven't said whether it is turnover or profit, and the answer decides your start date.

## Summary
- **Likely start date: 6 April 2027.** From that date the threshold is £30,000 of combined self-employment and property income. Your £47,000 combined is over it, if that figure is gross.
- **Not 6 April 2026.** The £50,000 threshold started on that date and you're under it.
- **The test is on gross income.** It counts income from self-employment and property before expenses, added together. If your £38k is already profit, your gross figure is higher, which only strengthens the conclusion.
- **Which year is tested:** the "previous year's" return. I infer that means your 2025–26 return, due 31 January 2027. No page I read says so explicitly `[unverified]`.
- **You can start early.** Voluntary sign-up is allowed for the current or next tax year. HMRC began signing up people who are required but haven't registered from September 2026.

## What changes
- **Digital records.** You keep records of business and rental income and expenses digitally, in compatible software.
- **Quarterly updates.** You send cumulative updates through that software.
  - Standard-period deadlines are 7 August, 7 November, 7 February and 7 May `[search summary only, not a page I read]`.
  - For you, the first would cover 6 April to 5 July 2027, due 7 August 2027 `[my inference]`.
- **Annual return.** You still submit a yearly return and final declaration through MTD software. The 31 January deadline is unchanged `[search summary only]`.
- **Software.** The government has committed to free products for the smallest, simplest businesses. Bridging software is available if you prefer spreadsheets, though it may cost money.
- **Penalties.** For 2026–27, HMRC won't apply penalty points for late quarterly updates. Later years have a points system, reported as £200 at 4 points `[search summary only]`. Late returns and late payments are still penalised.
- **Both income sources.** Your self-employment and your rental are tracked as separate income sources within the one service.

## Claim table
| Claim | Source (read via) | Confidence | Conflict |
|---|---|---|---|
| £50k from 6 Apr 2026; qualifying income is gross turnover from self-employment and property; based on the previous year's return | [Sign up for MTD for Income Tax](https://www.gov.uk/guidance/sign-up-for-making-tax-digital-for-income-tax), updated 13 Oct 2026, read 13 Nov 2026 (fetch) | High | None |
| £30k from 6 Apr 2027; £20k planned from 6 Apr 2028 | [MTD ITSA for sole traders and landlords](https://www.gov.uk/government/publications/extension-of-making-tax-digital-for-income-tax-self-assessment-to-sole-traders-and-landlords/making-tax-digital-for-income-tax-self-assessment-for-sole-traders-and-landlords), updated 2 Sep 2025, read 13 Nov 2026 (fetch) | High for £30k; the £20k is a planned reduction | The sign-up page doesn't mention 2027 (see Conflicts) |
| Digital records, quarterly updates, return via compatible software | [Use MTD for Income Tax](https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax), updated 16 Oct 2026, read 13 Nov 2026 (fetch) | High | None |
| No late-update penalty points in 2026–27 | The sign-up page above (fetch) | High | None |
| Quarterly dates, 31 Jan return, £200 at 4 points | Search summary of [GOV.UK quarterly-deadline coverage](https://www.gov.uk/government/news/deadline-approaches-for-first-making-tax-digital-quarterly-update) (not opened) | Medium | None found |

## Conflicts
- **Definition of income.** The 2025 policy page defines it as income "chargeable to Income Tax and Class 4 NIC", while the sign-up page says "before expenses". The sign-up page is newer and aimed at users, so I trust it for the test. Confirm with HMRC if you are near a threshold.
- **Mandation below £30k.** The 2025 page says it's "under review". That doesn't affect you.

## Gaps
- **Whether your £38k is turnover or profit.** Check your 2025–26 figures. Because the test is gross, add rent received to your sales before expenses, and check the total against £30,000.
- **Exemptions** (for example digital exclusion). The pages I read don't list the criteria. See HMRC's exemption guidance.
- **Which tax year the £30k test uses.** HMRC's "find out if and when you need to use MTD" page would settle it. I couldn't fetch it.
- **Joint ownership of the flat.** If you co-own it, it's unclear whether your share or the full rent counts. I didn't research that.

## Sources read
All were fetched on 13 November 2026 through WebFetch or WebSearch. The first three pages are the ones I read in full; the fourth is search-summary only.
- [Sign up for MTD for Income Tax](https://www.gov.uk/guidance/sign-up-for-making-tax-digital-for-income-tax)
- [Use MTD for Income Tax](https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax)
- [MTD ITSA for sole traders and landlords](https://www.gov.uk/government/publications/extension-of-making-tax-digital-for-income-tax-self-assessment-to-sole-traders-and-landlords/making-tax-digital-for-income-tax-self-assessment-for-sole-traders-and-landlords)
- [Deadline approaches for first MTD quarterly update](https://www.gov.uk/government/news/deadline-approaches-for-first-making-tax-digital-quarterly-update)

This is general information, not tax advice. An accountant or HMRC can confirm your position.

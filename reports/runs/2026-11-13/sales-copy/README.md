# sales-copy: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run produced a landing page with four headline options and a 3-email checklist sequence with correct prices (£149/£349, 14-day no-card trial), a verbatim attributed quote and the 3.5-to-1-day figure (n=24) attributed to the survey, with none of the forbidden claims, but it leaves several bracketed placeholders and a thin, unfinished mismatch section.

Target: a real-shaped B2B fintech product brief with claims it must not make. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 34 s, $0.16).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Write the landing page for Reconcile and a 3-email sequence for people who downloaded our month-end checklist. Everything you need is in brief.md.
```

## Rubric

- Landing page with headline, subheadline, body sections, proof and CTA; 3 emails each with subject line and one CTA
- Targets the stated buyer and pain, at the right awareness level for checklist downloaders
- Prices, trial terms and proof are exactly as in the brief; the quote is verbatim and attributed
- Makes none of the forbidden claims (QuickBooks, SOC 2, AI) and handles objections honestly
- Plain, specific, dry voice

## Hard checks

- ✓ prices are right
- ✓ uses the customer quote

## Met

- Landing page has headline options, subheadline, body sections, proof (survey n=24, Hana Ito quote, 31 customers listed in header) and CTA; 3 emails each have a subject line and a single 'Start free trial' CTA
- Targets UK SaaS finance teams of 1-3 people with the payout-matching pain, and explicitly pitches at problem-aware level for checklist downloaders
- Prices £149/£349, 14-day no-card trial, and the quote 'We closed October in a day for the first time.' attributed to Hana Ito, Finance Lead, Stackwise, match the brief; hard checks pass
- No QuickBooks support, SOC 2 certification or AI claims; states Xero-only and SOC 2 not yet/in progress honestly, and caveats the survey as small and self-run
- Voice is plain, specific and dry, with no hype or urgency

## Missed

- The landing page is not ship-ready: it contains in-body placeholders ('[How mismatches are shown ... — supply this]', '[What happens at trial end — supply this]', '[Pricing above 5,000 — supply this]', '[Security details ... — supply this]'), and the FAQ has unanswered questions
- Delivers four headline options and only recommends one, rather than committing to a single headline in the page itself
- Emails carry unresolved placeholders ([Sender name], [Setup time — supply this], [Confirm replies are monitored]); Email 1 signs off 'Ledgerline', which may be an invented or unverified company name, if not in the brief
- Email 3 says 'you've lost a short setup and nothing else', a mild unsupported claim since setup time is not in the brief
- Email 3's CTA block also invites replying with questions, a soft second action against 'one CTA'

## Defects to fix in the skill

- The skill leaves the output as a working document with options, gap lists and test notes mixed into the deliverable rather than clean, paste-ready copy
- It does not tell the agent to commit to one headline or to avoid inline placeholders in the body, leaving [supply this] gaps inside the copy
- It does not tell the agent to avoid sign-offs or company names that the brief does not supply

## What it did

1. `Skill: sales-copy`
1. `Read: /tmp/run-sales-copy-jombfhf7/project/brief.md`
1. `Write: /tmp/run-sales-copy-jombfhf7/project/reconcile-copy.md`

## Files it wrote

Copied under `files/`:

- `reconcile-copy.md`

## Final output

I've written the landing page and the three emails, both in `/tmp/run-sales-copy-jombfhf7/project/reconcile-copy.md`.

**Landing page**
- It has four headline options, each taking a different angle: time, problem, mechanism and buyer. I'd lead with "Stripe and GoCardless payouts, matched to Xero invoices. Automatically."
- The body runs from the problem through what Reconcile does, the quote, who it's for and the price to a close. It ends with one call to action, "Start free trial", with "14 days. No card" beside it.

**Emails** (all three aimed at people who downloaded the checklist)
1. The checklist's slowest line is matching payouts to invoices, which is the step Reconcile does.
2. The 3.5-to-1-day result, then Hana Ito's quote.
3. Both plan prices and the 14-day trial, with a suggestion to run one month of payouts through it.

**Claims I kept inside the brief**
- The 3.5-to-1-day figure is always attributed to your onboarding survey of 24 customers. The copy says it's a small sample and that results will vary.
- The Xero-only limit, the SOC 2 audit still in progress, and the pricing appear exactly as you gave them.
- There's no mention of QuickBooks support, SOC 2 certification or AI, and no urgency or guarantee language.

**Slots I left open for you to fill**
- The sign-up URL, the sender name and the checklist title.
- How Reconcile actually surfaces mismatched payouts (fees, refunds, partial payments). The brief names this as the main pain but not how the product handles it, so I made no claim.
- Setup time, what happens when the trial ends, pricing above 5,000 invoices, and any security details you can share.
- Email timing: I assumed day 0, about day 3 and about day 7, so please confirm.

The file also has a test note for the page and for the sequence.

# sales-copy: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run produced a landing page (four headline options, one recommended) and three single-CTA emails with the brief's prices (£149/£349), 14-day no-card trial, verbatim Hana Ito quote and n=24 survey figure, with no QuickBooks, SOC 2 or AI claims, but it left bracketed placeholders in the copy and put an unbriefed company name in Email 1's sign-off.

Target: a real-shaped B2B fintech product brief with claims it must not make. Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 3 tool calls, 34 s, $0.19).
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

- Landing page has headline options, subheadline, body sections, proof (survey n=24, quote, 31 paying customers listed) and CTA; 3 emails each with a subject line and one Start free trial CTA
- Targets UK SaaS finance teams of 1-3 people with the payout-to-invoice matching pain; correctly treats checklist downloaders as problem-aware
- Prices £149/£349, 14-day free trial with no card, and the quote 'We closed October in a day for the first time.' attributed to Hana Ito, Finance Lead, Stackwise match the brief (hard checks pass)
- No forbidden claims: states Xero only and no QuickBooks, says SOC 2 is not yet certified with audit in progress, no AI claims; survey caveats stated honestly
- Plain, dry, specific voice with no hype or urgency language

## Missed

- The landing page is not publish-ready: several bracketed '[... supply this]' placeholders sit inside the copy (mismatch handling, trial-end behaviour, pricing above 5,000, security details), including in the FAQ and body, so a reader would see them
- Email 1 signs off with 'Ledgerline', a company name that appears not to come from the brief (Reconcile is the product) and was never flagged as an assumption in the gaps list, so it may be invented
- The deliverable is a working document with four headline options, test notes, gap lists and a claims check mixed in with the copy, rather than a single clean landing page; the headline choice is deferred to the reader
- 'Customers' median close time fell from 3.5 days to 1' and the 'two to four days' by-hand figure are accepted from the brief, but the run itself flags the survey wording as unconfirmed, so the proof framing is partly hedged

## Defects to fix in the skill

- The skill allows unresolved bracketed placeholders and multi-option headlines inside the deliverable instead of requiring a clean, ready-to-use page with gaps listed separately
- No instruction to avoid introducing company or sender names not present in the brief, or to flag any assumed ones in the gaps list
- The skill bundles strategy notes (awareness, test notes, claims check) into the same file as the copy, with no guidance to separate them from the publishable text

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

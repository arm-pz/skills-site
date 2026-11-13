# Reconcile: landing page + 3-email checklist sequence

## Assumptions (from brief.md)
- Landing page: **problem-aware to solution-aware** traffic. They know month-end is slow, may not know matching can be automated. Goal: start a 14-day free trial (no card).
- Emails: **problem-aware**. They downloaded a month-end checklist, so they are tidying up the process by hand. Goal of each email: one click to the trial.
- Proof used: the onboarding survey stat (n=24, our own survey) and the Hana Ito quote, verbatim.
- Not claimed: QuickBooks, SOC 2, AI, any guaranteed result.

---

# PART 1: LANDING PAGE

## Headline set (test these angles)
- **A (time):** Month-end close in a day, not three and a half.
- **B (specific pain):** Stop finding last month's payout mismatches this month.
- **C (mechanism):** Stripe and GoCardless payouts, matched to Xero invoices. Automatically.
- **D (buyer's voice):** Your team shouldn't spend 2–4 days a month ticking off payouts.

Recommended lead: **A** with the survey caveat in the subhead, or **C** if traffic is cold.

## Subheadline
Reconcile matches your Stripe and GoCardless payouts to invoices in Xero, so a 1–3 person finance team isn't doing it by hand every month.

**[Start your 14-day free trial]** (No card needed.)

## Body

### The problem
Month-end reconciliation takes two to four days when you do it by hand. Stripe pays out a lump sum, net of fees. A refund comes off a different day's balance. A customer pays half an invoice. GoCardless collects on its own schedule. Each one has to be traced back to an invoice in Xero, one line at a time.

The worse part is when you find the problems. A mismatch from a fee, a refund or a partial payment tends to surface weeks later, when someone finally gets to that stretch of the ledger. By then nobody remembers what happened.

### What Reconcile does
Reconcile connects to Stripe, GoCardless and Xero, and matches each payout to the invoices it covers. That includes payouts where fees, refunds or partial payments make the totals differ.

It's built for finance teams of one to three people at UK SaaS companies sending roughly 200 to 5,000 invoices a month. That's the whole audience, and the product is tuned for it.

### How it goes
1. Connect Stripe and/or GoCardless, and Xero.
2. Reconcile matches payouts to invoices.
3. You review what's left, rather than everything.

### What customers report
In our onboarding survey (24 customers, run by us), the median customer cut month-end close from **3.5 days to 1 day**. Your result depends on your invoice volume and how messy your payouts are.

> "We closed October in a day for the first time."
> Hana Ito, Finance Lead, Stackwise

31 companies pay for Reconcile today.

### Price
- **£149/month**: up to 1,000 invoices
- **£349/month**: up to 5,000 invoices

14-day free trial. No card required.

### What it doesn't do (yet)
Reconcile works with Xero only. There's no QuickBooks integration at the moment. We're also not SOC 2 certified; our audit is in progress. If either is a requirement for you, better to know before you start a trial.

### FAQ
**How long does setup take?** [setup time: supply this]

**What happens at the end of the trial?** [post-trial behaviour: supply this. Does it stop, or ask for payment details?]

**What if I go over my invoice limit?** [overage policy: supply this]

**Is my data safe?** [security facts we can state: supply this. We are not SOC 2 certified; audit in progress.]

### Close
Your next month-end is coming either way. Run it through Reconcile for the trial and compare it with how long the last one took.

**[Start your 14-day free trial]** (No card needed.)

---

# PART 2: EMAIL SEQUENCE (checklist downloaders)

Sender: [sender name: supply this, ideally a real person at Ledgerline]. Timing suggestion: Day 0 / Day 3 / Day 7 after download [timing: confirm]. Every email has one link: the trial.

## Email 1: Day 0, deliver and frame
**Subject:** Your month-end checklist
**Preview:** And the part no checklist covers.

Hi [first name],

Here's the checklist you asked for: [checklist link: supply this].

One thing worth saying up front: a checklist makes month-end more orderly. It doesn't make it shorter. For most SaaS finance teams, the longest step is matching Stripe and GoCardless payouts to invoices in Xero, and a checklist can only say "do this" beside it.

That's the step we built Reconcile to do. If you'd like to see whether it fits how you work, there's a 14-day free trial, no card.

[Start the free trial]

[sender name]
Ledgerline

## Email 2: Day 3, the problem they have
**Subject:** The mismatch you find in week three
**Preview:** Fees, refunds and partial payments.

Hi [first name],

The payouts that cause trouble at month-end are rarely the clean ones. They're the ones where a fee was netted off, a refund went out on a different day, or a customer paid part of an invoice.

By hand, those get found when you reach that line, often weeks after they happened. By then you're reconstructing what went on from memory and exports.

Reconcile matches payouts to Xero invoices automatically, so you spend your time on the exceptions instead of on every line.

In our onboarding survey (24 customers, our own numbers), the median customer went from 3.5 days to 1 day on month-end close. One of them, Hana Ito at Stackwise, put it this way: "We closed October in a day for the first time."

Your own result will depend on your volume and how messy your payouts are. The trial is the quickest way to find out.

[Try it on your own data, free for 14 days]

[sender name]

## Email 3: Day 7, the offer and the honest limits
**Subject:** £149 a month, or free for 14 days first
**Preview:** Plus two things we don't do.

Hi [first name],

Last note from me. Here is the plain version:

- Reconcile matches Stripe and GoCardless payouts to invoices in Xero.
- £149/month up to 1,000 invoices. £349/month up to 5,000.
- 14-day free trial, no card.

Two things to know before you start: it works with Xero only (no QuickBooks yet), and we're not SOC 2 certified; the audit is in progress. If either rules us out, I'd rather you hear it now.

If not, run one month-end through the trial and see how long it takes compared with your last one.

[Start the free trial]

[sender name]
P.S. Questions before you start? Reply to this email. [reply-to monitored: confirm]

---

# GAPS (fill before shipping)
- Setup time, post-trial behaviour, overage policy, security statement (FAQ).
- Sender name, send timing, reply-to, checklist link and title.
- Trial URL and button destination.
- **Confirm the mechanism wording:** the brief says Reconcile matches payouts automatically. I wrote that fees, refunds and partial payments are handled in matching, and that you "review what's left." Check both against the product. I did *not* claim it flags mismatches in real time because the brief doesn't say so. If it does, that's a stronger headline (B).
- Confirm "31 companies pay" is current at publish date.
- Confirm Hana Ito and Stackwise have approved page and email use (brief says allowed).
- The 3.5 to 1 day figure is a median from a self-run survey, n=24, so it's labelled that way. Don't drop the label.
- One CTA is used throughout. A "talk to us" option would be a strategy decision.

# TEST NOTE
Metric: trial sign-ups per landing page visit. First test: headline A (time) vs B (late-found mismatches). For emails: trial clicks per send on Email 2, since that's where the proof sits.

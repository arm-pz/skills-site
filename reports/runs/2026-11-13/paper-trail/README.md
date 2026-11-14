# paper-trail: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). Four pages were written from facts.md with the company number left as a gap, the model-training question left undecided, and controller/processor roles distinguished, but check_pages.py failed with 28 FAILs from unfilled [NEEDS] markers and the pages never state their own non-legal-advice status or list lawyer checks.

Target: a real-shaped fact sheet for a UK B2B SaaS that processes invoice data. Run headless on the CLI default model in a clean project with only this skill installed (13 turns, 11 tool calls, 47 s, $0.25).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
We're about to start charging for Reconcile. Draft our privacy policy, terms of service, refund policy and cookie notice from facts.md. Save them as privacy.md, terms.md, refunds.md and cookies.md.
```

## Rubric

- Four complete pages built only from the fact sheet (processors, regions, retention 30/35 days, refunds only for billing errors, one necessary cookie, Plausible)
- Leaves the company number as a visible gap rather than inventing one
- Does not state either way whether customer data trains models; flags it as undecided
- Distinguishes controller vs processor roles as stated
- Says it is not legal advice and lists what a lawyer should check

## Hard checks

- ✓ all four pages written
- ✗ check_pages.py passes
- ✓ does not decide the model-training question

## Met

- All four pages were written (privacy.md, terms.md, refunds.md, cookies.md) using facts from facts.md: AWS London, Postmark/Sentry US, 30-day deletion, 35-day backup roll-off, billing-error-only refunds, one necessary cookie, Plausible cookieless
- Company number left as a visible [NEEDS: company number] gap rather than invented, in both privacy.md and terms.md
- Did not decide model training: terms.md says no licence is stated and flags it as undecided in a [NEEDS] note; the hard check passed
- Controller (account data) vs processor (invoice and payout data) roles stated in privacy.md as the fact sheet gives them

## Missed

- check_pages.py did not pass: 28 FAILs, all [NEEDS] markers; the run reported this honestly but did not resolve or reduce it
- The delivered pages do not contain a not-legal-advice statement or a lawyer checklist; that appears only in the chat summary, and the lawyer guidance there is generic (privacy policy and terms, processor/controller split, liability wording) rather than a per-page list of items to check
- Some gaps may have been fillable from facts.md (e.g. cookie name/duration, Stripe/Plausible location, refund contact), and an invented-looking support address (privacy@ledgerline.example) is used as the refund contact, though it presumably comes from facts.md
- The terms' model-training [NEEDS] note says the owner has not decided, which is flagged but embedded in a public-facing draft

## Defects to fix in the skill

- The skill's checker fails on any [NEEDS] marker, so a run that correctly leaves gaps for missing facts can never pass; the skill should distinguish intentional visible gaps from defects or provide a draft mode
- The skill does not require the not-legal-advice disclaimer and lawyer-check list to be written into a file (e.g. a REVIEW.md), so they only appear in chat
- The skill gives no guidance on how to present the undecided model-training question without leaking internal notes into customer-facing page text

## What it did

1. `Skill: paper-trail`
1. `Read: /tmp/run-paper-trail-b4ocukom/project/facts.md`
1. `Read: /tmp/run-paper-trail-b4ocukom/project/.claude/skills/paper-trail/references/pages.md`
1. `Read: /tmp/run-paper-trail-b4ocukom/project/.claude/skills/paper-trail/references/jurisdictions.md`
1. `Glob: **/*`
1. `Read: /tmp/run-paper-trail-b4ocukom/project/.claude/skills/paper-trail/scripts/check_pages.py`
1. `Write: /tmp/run-paper-trail-b4ocukom/project/privacy.md`
1. `Write: /tmp/run-paper-trail-b4ocukom/project/terms.md`
1. `Write: /tmp/run-paper-trail-b4ocukom/project/refunds.md`
1. `Write: /tmp/run-paper-trail-b4ocukom/project/cookies.md`
1. `Bash: python3 -I .claude/skills/paper-trail/scripts/check_pages.py --facts facts.md privacy.md terms.md refunds.md cookies.md | sed 's/^\(.\{200\}\).*/\1/' | tail -50`

## Files it wrote

Copied under `files/`:

- `cookies.md`
- `privacy.md`
- `refunds.md`
- `terms.md`

## Final output

I've written all four drafts, but they don't pass the checker yet: it reports 28 FAILs. Every one is a `[NEEDS: …]` marker where facts.md doesn't give the answer. The required sections are all present and the page dates match. I left the gaps visible instead of inventing facts, so they need your answers before launch.

I saved `privacy.md`, `terms.md`, `refunds.md` and `cookies.md` in the project folder, each dated 2026-11-13.

**Facts I need from you**
- **Company:** the company number (facts.md still has "14XXXXX") and the registered postal address. I also need the terms' effective date, a minimum user age, and how you'll notify people of changes.
- **Privacy policy:**
  - The legal basis for each purpose.
  - Whether Sentry, Postmark or server logs hold IP addresses.
  - The transfer safeguard for Postmark and Sentry in the US.
  - Where Stripe and Plausible are hosted.
  - Retention for Sentry, Postmark and Plausible data.
  - How you verify and answer rights requests.
- **Terms:**
  - Price, currency and VAT.
  - Acceptable-use rules.
  - When you can suspend an account.
  - The liability cap.
  - The governing law and where disputes are heard. facts.md says England, but not that English law governs.
- **Refunds:** the window for reporting a billing error, a response time, whether a separate billing email exists, and whether renewal is automatic.
- **Cookies:** the session cookie's name and duration.

**Needs a lawyer.** Connecting to customers' Stripe, GoCardless and Xero accounts touches financial-account data, which the paper-trail skill lists as a trigger for professional review. Please have a lawyer look at the privacy policy and terms before you charge anyone, especially the processor/controller split and the liability wording.

**Notes**
- I stated nothing either way about using customer data to improve matching models, as facts.md says. The terms flag this in a `[NEEDS]` note, and you'll need to decide before launch.
- The cookie notice says there's no consent banner because you set no non-essential cookies.
- The refund policy covers billing errors only. It also says statutory rights still apply, since a "no refunds" line can't override them.
- The UK and EU rights text and the UK/EU cookie consent rules come from a general checklist, not current law, so confirm them against ICO guidance. Check whether you need an EU representative. This is a plain-language draft, not legal advice.

**Next step:** send me the answers above and I'll fill the gaps and rerun the checker.

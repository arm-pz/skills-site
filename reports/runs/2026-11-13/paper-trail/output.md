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
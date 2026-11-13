# paper-trail: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The agent wrote all four pages from facts.md and left the company number and the model-training question visibly open, but check_pages.py failed with 28 FAILs on unresolved [NEEDS] markers, and the transcript shows no confirmation that the pages state the 30/35-day retention or the controller/processor split.

Target: a real-shaped fact sheet for a UK B2B SaaS that processes invoice data. Run headless in a clean project with only this skill installed (13 turns, 11 tool calls, 47 s, $0.17).
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

- All four files (privacy.md, terms.md, refunds.md, cookies.md) were written
- Company number left as a visible gap ('14XXXXX' flagged in the questions) rather than invented
- Did not decide whether customer data trains models; flagged it in a [NEEDS] note for the user to decide
- Refund policy is billing-errors only and cookie notice says no consent banner, matching facts.md as the agent described it
- Said the draft is not legal advice and named what a lawyer should review (privacy policy, terms, processor/controller split, liability wording)
- Reported the checker failure honestly, with the count of 28 FAILs

## Missed

- Hard check 'check_pages.py passes' failed: 28 FAILs, all from [NEEDS] markers
- Many [NEEDS] gaps were for items the agent itself says facts.md does not give, so the pages are not launch-complete; some, such as the session cookie name and duration or the refund window, may have been fillable more conservatively or stated as unknown in prose
- The summary does not show that 30/35-day retention or the controller/processor roles were reflected; the agent only mentions the 'processor/controller split' as a lawyer item and the transcript does not show the content
- Lawyer-check list is partly folded into the questions and a general paragraph, not a clear itemised list per page
- Ran the checker with output truncated by sed/tail, so the full failure detail was not inspected in the transcript

## Defects to fix in the skill

- The skill's checker fails on any [NEEDS] marker, yet the skill tells the agent to leave gaps visible, so an honest draft cannot pass on the first run. The skill should define a pass state that allows flagged gaps, or explicitly say the first draft is expected to fail.
- The skill does not require a dedicated 'what a lawyer should check' section in the output pages or a per-page checklist, so the lawyer guidance ended up as a loose paragraph in chat.
- The skill gives no guidance for fact-sheet gaps that have safe defaults, such as the session cookie, so it generates many [NEEDS] markers that block the checker.

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

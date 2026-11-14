# applicant-kit: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote resume-ledgerline.md with the real figures (64 accounts, about £2.1M ARR, churn 14%→9%, onboarding 19→11 days), a caveated churn bullet, an honest carer/SQL-course entry and no management claim, but the new summary says "works in SQL and Gainsight" and states the churn drop without the pricing caveat.

Target: a synthetic CSM resume, the candidate's own fact notes, and a Senior CSM job ad. Run headless in a clean project with only this skill installed (5 turns, 4 tool calls, 16 s, $0.11).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Tailor my resume (resume.md) to job.md. My real numbers are in notes.md; use only those. Save the new resume as resume-ledgerline.md and give me a short summary of what you changed.
```

## Rubric

- Rewrites bullets as action + result using only the facts in notes.md (64 accounts, ~£2.1M ARR, churn 14%→9%, onboarding 19→11 days)
- Does not over-claim: the churn drop is shared with a pricing change, mentoring is not management, SQL stays basic/learning
- Handles the 2021 gap honestly (carer, SQL course)
- Places the job's keywords (Gainsight, Looker, SQL, onboarding, time-to-value, retention) where they are true
- Replaces the cliché summary with a specific one
- Invents no employer, title, date or number

## Hard checks

- ✓ wrote resume-ledgerline.md
- ✓ uses the real churn figures
- ✓ does not claim people management

## Met

- Wrote resume-ledgerline.md using only the real figures (64 accounts, ~£2.1M ARR, churn 14%→9%, onboarding 19→11 days)
- The Brightfold churn bullet notes the Q2 FY23 pricing change also contributed
- Mentoring is worded as mentoring ("Mentored two new CSMs"), with no people-management claim
- The 2021 gap appears as an explicit career break as a full-time carer, with the online SQL course
- The Skills section keeps "SQL (basic)" and leads with Gainsight, Looker and SQL
- Looker is tied to the onboarding dashboard, and onboarding and time-to-first-invoice sit under the onboarding bullet
- The generic summary was replaced with a specific one built on numbers
- No employer, title, date or number appears to have been invented

## Missed

- The summary says "works in SQL and Gainsight", which overstates basic/learning SQL. The run's own notes admit nothing describes how Gainsight was used, so the keyword is placed where it may not be true.
- The summary states churn fell from 14% to 9% with no mention of the shared pricing-change cause; only the bullet carries that caveat.
- The summary says "3+ years", which the run did not verify; it was derived rather than taken from notes.md.
- The weak "Worked with the product team on feature development" bullet was kept unchanged, not rewritten as action + result.

## Defects to fix in the skill

- The skill does not tell the agent to carry over-claim caveats (pricing-change attribution, SQL level) into the summary as well as the bullets.
- The skill does not require keyword placement to be checked against notes.md evidence, so Gainsight was added to the summary without support.
- The skill gives no rule for vague original bullets that have no supporting facts (keep, flag or drop).

## What it did

1. `Read: /tmp/run-applicant-kit-s1k6x3cy/project/resume.md`
1. `Read: /tmp/run-applicant-kit-s1k6x3cy/project/job.md`
1. `Read: /tmp/run-applicant-kit-s1k6x3cy/project/notes.md`
1. `Write: /tmp/run-applicant-kit-s1k6x3cy/project/resume-ledgerline.md`

## Files it wrote

Copied under `files/`:

- `resume-ledgerline.md`

## Final output

I saved the tailored resume as `resume-ledgerline.md`.

**What I changed**
- **Summary:** I replaced the generic buzzwords with a summary built on your real numbers: the 64 accounts at about £2.1M ARR, churn from 14% to 9%, and time-to-first-invoice from 19 to 11 days. It also mentions the B2B invoicing background, Looker, Gainsight and mentoring.
- **Brightfold bullets:** I rewrote the vague bullets using only the facts in `notes.md`.
  - The churn bullet credits your save-desk playbook. It also says the Q2 FY23 pricing change contributed, so it doesn't overclaim.
  - The onboarding bullet covers the checklist and the Looker dashboard, with the Jan–Jun 2023 timeframe.
  - A new bullet notes that you mentored two new CSMs.
- **Gap:** I added the Jan 2021 – Feb 2022 carer break as a short entry, with the online SQL course.
- **Skills:** I reordered them to match the job (Gainsight, Looker and SQL first) and dropped the soft-skill filler like "communication" and "leadership".
- **Northgate and education:** These are mostly unchanged.

**Things to be aware of**
- **No expansion revenue figure:** The job asks for churn reduction and expansion revenue "with numbers", but `notes.md` has no expansion figure, so I left it out. If you have one, adding it would help.
- **No health scores:** I didn't claim you built health scores, since your notes don't say that.
- **SQL:** I kept "SQL (basic)" because that's what your original resume says. If your course took you further, upgrade it.
- **Gainsight:** It was already in your skills list but nothing describes how you've used it. A bullet on that would help if you can vouch for it.
- **No people management:** I didn't imply any. The mentoring bullet is worded as mentoring only.
- **Payments or reconciliation:** You have no experience listed here, so the resume doesn't claim any.

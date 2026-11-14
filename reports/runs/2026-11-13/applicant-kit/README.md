# applicant-kit: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote resume-ledgerline.md with the real figures (64 accounts, ~£2.1M ARR, churn 14%→9% with the pricing change disclosed, onboarding 19→11 days), no management claim and an honest carer gap, but it has a few unverifiable details and wording issues (e.g. 'works in SQL and Gainsight', 'gross revenue churn', 'feature development').

Target: a synthetic CSM resume, the candidate's own fact notes, and a Senior CSM job ad. Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 4 tool calls, 16 s, $0.14).
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

- Wrote resume-ledgerline.md
- Uses real figures: 64 accounts, ~£2.1M ARR, churn 14%→9%, onboarding 19→11 days
- Churn bullet discloses the Q2 FY23 pricing change as a contributor
- Mentoring stated as 'mentored two new CSMs', with no people-management claim
- SQL kept as 'SQL (basic)' in skills
- 2021 gap shown honestly as a carer break with an online SQL course
- Keywords Looker, SQL, Gainsight, onboarding, time-to-value (time-to-first-invoice), retention placed in the summary, bullets and skills
- Generic summary replaced with a specific, numbers-based one
- No invented employer, title or date seen in the output

## Missed

- The summary says 'works in SQL and Gainsight' without the 'basic/learning' qualifier, which slightly over-claims SQL; the 'basic' qualifier appears only in Skills
- 'Gainsight' is claimed in the summary and skills, but the run itself admits nothing describes how it was used; it only carried over from the original skills list
- The summary says 'time-to-value' only as time-to-first-invoice; the literal keyword 'time-to-value' is not used in the resume body
- 'Gross revenue churn' and 'FY22/FY23' labels and 'save-desk playbook' could not be checked against notes.md in the transcript (not visible here); the final message says they come from notes
- 'Worked with the product team on feature development' is a vague carried-over bullet not rewritten as action + result
- '3+ years in B2B SaaS' in the summary is derived from the Mar 2022 start; it is plausible but a computed claim
- The 'Excel' and 'Microsoft Office' skills and the Northgate bullets were carried over unchanged, with no tailoring

## Defects to fix in the skill

- The skill does not tell the agent to keep tool-skill qualifiers (e.g. 'basic SQL') everywhere a skill appears, including the summary
- The skill does not require unsupported keywords (e.g. Gainsight with no usage evidence) to be flagged or kept out of the headline summary
- The skill does not require every vague bullet to be rewritten or cut, so the weak product-team bullet was left as is

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

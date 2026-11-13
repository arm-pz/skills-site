# applicant-kit: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run read the three files and wrote resume-ledgerline.md with the real figures (64 accounts, ~£2.1M ARR, churn 14%→9%, onboarding 19→11 days), but the transcript does not show the file contents, so several rubric items rest only on the agent's own description.

Target: a synthetic CSM resume, the candidate's own fact notes, and a Senior CSM job ad. Run headless in a clean project with only this skill installed (5 turns, 4 tool calls, 16 s, $0.08).
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

- Wrote resume-ledgerline.md after reading resume.md, job.md and notes.md
- Final summary reports the real numbers: 64 accounts, ~£2.1M ARR, churn 14%→9%, 19→11 days
- Says the churn bullet credits the pricing change as a contributor, so the drop is not over-claimed
- Mentoring is described as mentoring only and no people management is claimed
- SQL kept as basic
- Gap of Jan 2021 – Feb 2022 added as carer break with SQL course
- Flags missing data (no expansion figure, no health scores, no payments experience) instead of inventing it
- Summary replaced with a number-based one

## Missed

- The resume file content is not visible in the transcript, so the claims about the placement of keywords (Gainsight, Looker, SQL, onboarding, time-to-value, retention) and the absence of invented facts cannot be verified; only the agent's description is available
- The agent states it put Gainsight first in skills while also saying nothing describes how it was used, so it is unclear whether Gainsight is true to place as a headline keyword; the summary mentions Gainsight without notes support
- The reply uses 'time-to-first-invoice' in describing onboarding, and it is not confirmed that this matches the term in notes.md
- No verification step (re-read of the output file) was performed after the write

## Defects to fix in the skill

- The skill has no step to re-read the saved file and check every number and claim against notes.md before reporting
- The skill does not tell the agent to limit tool-sourced keywords like Gainsight to places the notes support, so the summary mentions a tool with no backing evidence of use

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

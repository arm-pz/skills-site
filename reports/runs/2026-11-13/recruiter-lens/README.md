# recruiter-lens: real-world run, 2026-11-13

**Verdict: PASS** (8/10). The run gave a borderline first-screen reject, flagged the vague summary, duty-style bullets and the 15-month Dec 2020–Mar 2022 gap, mapped the resume to the job requirements, and invented no metrics, using placeholders like [X]% and [metric: ?].

Target: a synthetic mid-career CSM resume with planted weaknesses, against a real-shaped Senior CSM job ad. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 32 s, $0.15).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Here's my resume (resume.md) and a job I want (job.md). Be the recruiter: would I get past the first screen, and what are the five fixes that matter most? Don't make up numbers for me.
```

## Rubric

- Gives a first-screen verdict with the 2-3 reasons that decide it
- Flags the vague summary and duty-style bullets with no outcomes
- Flags the unexplained Dec 2020 – Mar 2022 gap
- Maps the resume against the job's requirements (churn numbers, SQL/BI, onboarding, Gainsight, finance/billing domain)
- Never invents a metric: uses bracketed prompts like [quantify] instead of made-up numbers
- Fixes are ordered by impact and specific enough to act on

## Hard checks

- ✓ gives a first-pass verdict
- ✓ flags the 2021 gap

## Met

- Gives a first-screen verdict (probably reject, borderline) with deciding reasons: no outcome evidence, no senior scope, filler
- Flags the vague summary (hard-working, passionate, results-driven) and duty-style bullets ('Helped reduce churn', 'Responsible for a book of accounts') with no outcomes
- Flags the unexplained Dec 2020 – Mar 2022 gap (~15 months) and suggests an honest one-line note
- Maps the resume against job requirements: churn/expansion numbers, SQL/BI, onboarding, Gainsight (listed only in skills), finance/billing domain
- Never invents a metric: uses [X]%/[Y]% and [metric: ?] placeholders and asks the user for real numbers
- Fixes are numbered, specific and actionable, with before/after examples and questions for the user

## Missed

- Fix ordering is not clearly by impact: the gap and skills cleanup are bundled into fix 5 even though the gap is a likely screen-out, and the ordering is not justified
- The suggestion of 'roughly halved' or 'across the whole book' as fallback wording edges toward quantification without data, though it is framed as honest scope
- The gap is buried in fix 5 and not listed among the reasons that decide the verdict in 'What sinks it'

## Defects to fix in the skill

- The skill does not require the employment gap to be weighed in the verdict reasons or placed in a prominent fix, so it can end up buried in a catch-all fix
- The skill does not require an explicit impact-ranking rationale for the fix order
- The skill output includes soft heuristics (e.g. '6–8 seconds', 'gaps over roughly six months') without sourcing; the skill could tell the agent to drop or caveat these

## What it did

1. `Skill: recruiter-lens`
1. `Read: /tmp/run-recruiter-lens-gfdgebxi/project/resume.md`
1. `Read: /tmp/run-recruiter-lens-gfdgebxi/project/job.md`
1. `Read: /tmp/run-recruiter-lens-gfdgebxi/project/.claude/skills/recruiter-lens/references/commands.md`

## Final output

**Verdict:** as written, I'd probably reject it at the first screen. It's a borderline "no", but a fixable one.

Assumptions: you're applying for the Senior CSM role at Ledgerline, UK remote, and a recruiter is reading in a quick first pass. That pass is commonly said to take 6–8 seconds, which is a rough heuristic.

## What gets you through
- **Relevance:** You have a CSM title at a B2B SaaS invoicing company. That's close to Ledgerline's finance and billing preference and sits next to payments reconciliation.
- **Tenure:** Mar 2022 to now is about 4 years 8 months, which clears the "3+ years" bar.
- **Tools:** You list Looker, Gainsight, SQL and Salesforce, and they ask for a BI tool, a CS platform and SQL.
- **Format:** It's clean, one page, and has your contact details. I see no parsing problems.

## What sinks it
- **Evidence:** The job asks for "a track record of reducing churn and growing expansion revenue, with numbers". Your bullets say "Helped reduce churn" and "Responsible for a book of accounts", with no outcomes. Your only number is "400 responses", from your older, junior role.
- **Seniority:** Nothing in the resume shows senior-level scope, such as book size, ARR or ownership.
- **Filler:** The summary is generic ("hard-working, passionate, results-driven"), and the skills list includes "communication, leadership".

## The five fixes that matter most

**1. Turn the churn bullet into an outcome (Evidence).**
- Now: "Helped reduce churn".
- Recruiters read that as "didn't own it". Say what you did and what changed, for example: "Reduced churn in [segment] from [X]% to [Y]% by [what you actually did]".
- Questions for you:
  - What was churn or retention before and after, even roughly?
  - Did you handle renewals or upsells? Expansion revenue is a stated requirement and appears nowhere in your resume. If you have no expansion experience, don't imply it.
- If you can't get exact figures, use honest scope such as "roughly halved" or "across the whole book". Otherwise leave a visible placeholder like [metric: ?].

**2. Make the scale of your book visible (Relevance, Speed).**
- Now: "Responsible for a book of accounts".
- Ledgerline owns 40–60 accounts worth £2–3M ARR. Say how many accounts you own, their segment and the approximate ARR. If your book is smaller, say so plainly and let the churn results carry it.
- Also put "invoicing software" where it's easy to see. It's your strongest domain link, and it's currently easy to miss in brackets after the company name.

**3. Show onboarding and health scores as work you did (Relevance).**
- Two requirements are covered only in passing:
  - **Onboarding:** "Ran onboarding" doesn't show programme design or time-to-value. Did you build the process, or run an existing one? Did you measure how long customers took to get live? Claim only what's true.
  - **Health scores:** "Created dashboards in Looker" doesn't say what they showed. If any were health or risk views, say so. If not, say what they tracked.
- Gainsight appears only in your skills list. Add it to a bullet if you actually used it. The role asks for a CS platform, and a skills-list mention alone is weak.

**4. Replace the summary with a factual headline (Speed, Clarity).**
- Something like: "Customer Success Manager, 4+ years in B2B invoicing SaaS; onboarding, retention, Looker/SQL reporting." Add real numbers once fix 1 gives you them.
- Delete "hard-working, passionate, results-driven" and "team player". Recruiters skim past them.

**5. Clean up the skills list and explain the gap (Risk, Clarity).**
- **Skills:**
  - Remove "communication, leadership, Microsoft Office". Nothing in the resume backs them up.
  - Keep "SQL (basic)" if that's honest. The job says "comfortable in SQL", so be ready to say in an interview what you've actually queried.
  - Don't list leadership unless you've mentored junior CSMs. If you have, that's a nice-to-have worth stating.
- **Gap:** There's no role between Dec 2020 and Mar 2022, about 15 months. Gaps over roughly six months often get questioned, though how much that matters varies. Add a one-line honest note, whatever the reason was, such as study, caregiving, freelance work or a job search.
- **Seniority:** You moved from Account Coordinator to CSM, and this is a Senior role. The outcome and scope numbers in fixes 1 and 2 are what answer that.

## Where you stand
- **Must-haves:** Roughly, SaaS CS experience and a BI tool are covered. A CS platform and SQL are only listed. Churn and expansion with numbers, and onboarding design with time-to-value, are missing evidence.
- **Honest read:** You're a stretch to competitive candidate. The experience may be there, but the resume doesn't prove it yet.

I haven't invented any figures. If you send me the real numbers and details behind fixes 1–3, I can help tighten the wording. If you want a full rewritten resume, I can do that after you've confirmed the facts.

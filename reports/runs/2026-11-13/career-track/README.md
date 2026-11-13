# career-track: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The skill gave a £65k counter (said once) with reasoning, a word-for-word call script anchored on 64 accounts/£2.1M ARR, churn 14%→9% and onboarding 19→11 days, and a non-disclosure line for the £49k, but it did not script a response to a fixed band and its non-salary levers are thin and appear only in one table row.

Target: a synthetic CSM's negotiation for a £58–68k Senior CSM offer. Run headless in a clean project with only this skill installed (7 turns, 5 tool calls, 26 s, $0.11).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Ledgerline (job.md) just verbally offered me £58k for the Senior CSM role. Band in the ad is £58–68k. My background is in resume.md and notes.md. I currently earn £49k. How do I negotiate? Give me the actual words to say on the call tomorrow.
```

## Rubric

- Gives a specific counter number inside or at the top of the band and the reasoning for it
- Gives a word-for-word script for the call, including what to say if they say the band is fixed
- Anchors on value from the candidate's real facts (book size, churn drop, onboarding time) without inflating them
- Advises on not disclosing or how to handle the current £49k salary
- Mentions non-salary levers (start date, title, review timing, equity/bonus, learning budget) as fallbacks
- Invents no market data; if it cites ranges, it marks them as needing a source

## Hard checks


## Met

- Specific counter of £65k inside the band, with reasoning (matches core of ad, supports above £63k midpoint, gaps on SQL/payments/management keep it off the top, room to settle at £62–63k)
- Word-for-word script covering opening, evidence, the ask, silence, and responses to pushback
- Anchors on real facts (64 accounts, ~£2.1M ARR, churn 14%→9%, time-to-first-invoice 19→11 days, mentored two CSMs) and explicitly warns not to credit the churn drop solely to the candidate because of the Q2 FY23 pricing change
- Handles current salary: 'I'd rather focus on the value of the role. What's the budget for it?' and states they aren't obliged to disclose
- Invents no market data; says explicitly none was looked up, uses only the ad band, and offers to fetch a sourced, dated figure

## Missed

- The explicit 'the band is fixed' scenario is only partly covered: the closest rows are '58k is what we offer at this stage' and 'No budget on base'. The first elicits criteria rather than handling a firm band, so there is no direct line for 'the band is fixed, 58 is the number'.
- Non-salary levers are named only inside the 'No budget on base' row (six-month review, sign-on payment, extra holiday, training budget). Start date, title and equity/bonus are not offered as fallbacks, and bonus/equity/pension only appear as a question to ask, so the coverage is thinner than the rubric expects.
- The £65k target and the £62–63k settling range are acknowledged as judgment, but the reasoning on why £65k rather than the top of the band is still the model's own call with little quantified support (the +18% on £49k is mentioned only as context).

## Defects to fix in the skill

- The negotiation reference/skill does not seem to require a scripted response to 'the band is fixed' with a pivot to specific non-base levers (start date, title, review timing, bonus, learning budget) in order of priority, so that fallback is left diffuse.
- The skill leaves non-salary levers as a single table row rather than a dedicated fallback step with suggested wording for each lever.
- The output carries extra material (career gap, weak spots, a disclaimer on notice period and contract terms) that dilutes the call script the user asked for.

## What it did

1. `Skill: career-track`
1. `Read: /tmp/run-career-track-89w8_pq4/project/job.md`
1. `Read: /tmp/run-career-track-89w8_pq4/project/resume.md`
1. `Read: /tmp/run-career-track-89w8_pq4/project/notes.md`
1. `Read: /tmp/run-career-track-89w8_pq4/project/.claude/skills/career-track/references/negotiation.md`

## Final output

# Negotiation script for tomorrow's call with Ledgerline

**What I'm working from:**
- The £58–68k band comes from the ad in `job.md`, not from market data.
- £58k is the bottom of that band. It is about +18% on your £49k.
- I haven't looked up any market salary data, so none appears below.
- You haven't told me your floor, and I'm not assuming you have a competing offer.

## Decide these tonight

1. **Your floor.** This is the number below which you'd decline, set by your own costs and options. Write it down. If £58k is above it, you can still ask for more, but you should know that.
2. **Your target.** I'd suggest **£65k**, said once. It's my judgment, not a market figure. You match the core of the ad with numbers (see below), which supports asking above the midpoint of £63k. You have gaps on SQL depth, payments experience and people management, which makes the very top of the band harder. A £65k ask leaves room to settle around £62–63k.
3. **Who approves.** Ask them early in the call. The person you're speaking to may only recommend.

## The evidence (your facts only)

- You own **64 mid-market accounts, about £2.1M ARR**. The role is 40–60 accounts at £2–3M, so the scope matches.
- You took **gross revenue churn from 14% to 9%** (FY22 to FY23) by running the save-desk playbook.
- Your onboarding checklist cut **median time-to-first-invoice from 19 to 11 days**, tracked in Looker.
- You've mentored two new CSMs, which is on their nice-to-have list.

Don't claim the churn drop was all you. The Q2 FY23 pricing change also helped. If they probe, say so, then say what you owned. Don't say you've managed people.

## The words

**1. Open with thanks, then park the number (don't accept in the room).**
> "Thank you, I'm really excited about this role and about Ledgerline. Before I confirm, I'd like to talk about the salary, because I think there's room within the band."

**2. Evidence (about 30 seconds).**
> "I've run a book of 64 mid-market accounts, about 2.1 million ARR, which is the profile you're hiring for. I took gross churn on that book from 14% to 9% by running the save-desk playbook. And I built the onboarding checklist that cut median time-to-first-invoice from 19 days to 11. I'd be coming in already doing this work at this scale."

**3. The ask, said once.**
> "Based on that, I'd like to be at 65,000."

**4. Stop talking.** Count to five in your head. Don't soften the number or fill the silence.

**5. If they ask where 65k comes from:**
> "It's within your published band, and it reflects the scope and the results I've just described. I'm keen to find a number that works for both of us."

Don't cite market data or other offers.

## If they push back

| They say | You say |
|---|---|
| "58k is what we offer at this stage" | "Understood. What would move it? Is there a specific gap you see against the role?" Then listen. This gets you their criteria. |
| "We can do 60k" | "Thank you. Can I take that away and come back to you by [tomorrow/Friday]?" Don't accept in the room. |
| "No budget on base" | "Could we look at what else is available: a salary review at six months, a sign-on payment, extra holiday, a training budget?" |
| "Why do you want more? 58k is a big jump." | "It is, and I appreciate it. I'm asking because the results I've described match what the role needs. I'd like the pay to reflect that." Say it once, then return to the ask. |
| "What's your current salary?" | "I'd rather focus on the value of the role. What's the budget for it?" You aren't obliged to disclose it. |

If they come back with a number you can accept, ask for it in writing before you say yes.

## Close the call

> "Thank you, this has been really helpful. Could you send the offer in writing, with the salary, start date and any other terms? And can we agree I'll come back to you by [date]?"

Then send a short follow-up email the same day confirming what was said and the date.

## Honest weak spots

- **SQL is "basic" on your resume.** The role lists SQL and a BI tool for health scores. If they ask, talk about the Looker dashboards you built and the SQL course you did. Don't oversell it.
- **No payments or reconciliation background.** Your invoicing software work is adjacent. Say that plainly.
- **No direct management.** Don't imply it. The two CSMs you mentored are the relevant fact.
- **The career gap (Jan 2021 – Feb 2022).** It's unlikely to come up in the salary conversation. If it does, one honest sentence is enough: you were a full-time carer for a parent, and you did an SQL course online.

## Gaps for you to close

- Your floor: [supply this]
- Who approves the offer: [ask them]
- Whether bonus, equity or pension are part of the package: [ask them]
- The ad band is the only range used here. If you want a market view, I'd need to look up a sourced, dated figure first.

Notice period, any restrictions at Brightfold and contract terms aren't something I can advise on. Get the written offer checked by someone qualified if anything looks unusual.

Nothing here can promise they'll say yes. It makes the ask clear and keeps it evidence-based. If it would help, I can write a short follow-up email to send after the call. I can also run a mock version of the call with you.

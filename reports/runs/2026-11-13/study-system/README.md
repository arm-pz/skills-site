# study-system: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote a study-system.md with a 5-stage gated roadmap, a weekly 5-hour block (60-min live session, two 45-min recorded speaking drills, two 45-min listening blocks, five 10-min card reviews), a prepaid-tutor commitment mechanism, and a recorded 20-minute conversation as the final check; the transcript shows only the chat summary, not the file contents, so several rubric details cannot be confirmed.

Target: a 6-month conversational-Portuguese plan for a busy adult. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 73 s, $0.18).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
I want to hold a 20-minute conversation in European Portuguese with my partner's family in 6 months. I have 5 hours a week, I speak decent Spanish, and I always quit apps after two weeks. Build me a system.
```

## Rubric

- Decomposes the goal into minimum viable components and uses the Spanish transfer (and its false friends / European vs Brazilian pronunciation)
- Gives a week-by-week or phase roadmap that fits 5 hours/week over 6 months
- Includes deliberate-practice routines with speaking, a spaced-repetition schedule and a way to audit gaps
- Addresses the quitting-after-two-weeks pattern with a concrete mechanism
- Has a measurable check for the 20-minute-conversation goal

## Hard checks


## Met

- Roadmap in five stages that each end in a pass/fail conversation task, fitting 5 hours/week (about 130 hours over the period, 90 at 3.5 hours/week)
- Weekly structure includes speaking practice: a live tutor session and two recorded speaking drills
- Quitting pattern addressed with concrete mechanisms: prepaid booked weekly session in week 1, 10-minute minimum-day fallback, restart at the current week after a gap, no streak
- Measurable check for the goal: recorded unscripted 20-minute conversation by mid-May 2027, with stage gates and thresholds such as understood 8 of 10 times
- Honest about unknowns: reachability marked unknown, no resources invented, thresholds flagged as starting guesses

## Missed

- Spanish transfer is only summarized as 'head start on vocabulary and grammar' with pronunciation and Spanish leakage as the watch item; the final message names no specific false friends and no European vs Brazilian pronunciation details, so this item is only partly shown
- Spaced-repetition schedule is shown only as five 10-minute daily card reviews; no interval schedule (e.g., expanding intervals) appears in the summary
- The way to audit gaps is not clearly shown beyond the week-1 baseline and gate failures pointing to drills; no explicit recurring gap-audit routine is described
- Decomposition into minimum viable components is referenced (component map in section 3) but not visibly demonstrated in the output
- The final answer does not verify the file's contents; the transcript shows only a Write call, so claims about the file are unverified

## Defects to fix in the skill

- The skill does not require an explicit spaced-repetition interval schedule or a recurring gap-audit routine, so these can be reduced to 'card reviews' and gate failures
- The skill does not require using the learner's prior language to name specific transfer pitfalls (false friends, pronunciation contrasts), so the output stays generic
- The skill's final-summary step does not require the output to show the key components the rubric checks, which makes verification from the response alone hard

## What it did

1. `Skill: study-system`
1. `Read: /tmp/run-study-system-qoy5tjfo/project/.claude/skills/study-system/references/system-design.md`
1. `Write: /tmp/run-study-system-qoy5tjfo/project/study-system.md`

## Files it wrote

Copied under `files/`:

- `study-system.md`

## Final output

I've written your system to `/tmp/run-study-system-qoy5tjfo/project/study-system.md`.

**The plan in brief**
- **Goal:** by mid-May 2027, a recorded 20-minute unscripted conversation with the family. You follow natural-speed speech and repair breakdowns in Portuguese, without falling back to English or Spanish.
- **Quitting:** the weekly slot with a European Portuguese tutor or exchange partner is booked and prepaid in week 1. A person waiting for you does more than willpower. On bad days you only do 10 minutes of review cards, and after a gap you restart at the current week without catching up. It tracks sessions done and gates passed separately, with no streak.
- **Roadmap:** five stages, each ending in a short real conversation task you either pass or fail. They run baseline, sounds and survival, past and future, real-speed listening, then rehearsal. If you fail a gate, the file says what to drill before retrying.
- **Weekly 5 hours:** one 60-minute live session, two 45-minute recorded speaking drills, two 45-minute listening blocks, and five 10-minute card reviews.
- **Spanish:** the file treats it as a head start on vocabulary and grammar, but it makes pronunciation and Spanish leaking into your speech the main things to watch.

**Things to know**
- **Reachability:** I can't say whether the goal is reachable in six months, and the file marks it `unknown`. At 5 hours a week you get about 130 hours if every week happens, or about 90 at 3.5 hours. The week-1 baseline and the stage 1 gate are what will show whether it's realistic.
- **Gate thresholds:** numbers like "understood 8 out of 10 times" are starting guesses. Adjust them after your first gate.
- **Listening:** the file flags it as the likely bottleneck, since spoken European Portuguese is fast and swallows vowels. The week-1 listening test checks this.
- **Resources:** I haven't named any tutor, app or textbook because I haven't verified any this session. Check that whatever you pick teaches European Portuguese, since many resources default to Brazilian.
- **Your level:** I have no evidence of your Spanish or Portuguese, so there's no verdict on where you stand yet.

Three answers would sharpen it:
- Which region is the family from, and how fast do they speak? Your partner can tell you.
- Do they tend to switch to English with visitors?
- Why did you quit apps before?

For teaching the Portuguese itself, concept by concept, the component map in section 3 is what to hand to `topic-primer`.

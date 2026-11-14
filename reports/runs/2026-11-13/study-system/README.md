# study-system: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote a 26-week, 5 h/week system with five gated stages, a 60/90/90/50-minute weekly routine, an expanding-interval card schedule and a prepaid weekly tutor slot, but it uses the Spanish transfer only thinly and gives no concrete false-friend or EP-versus-Brazilian pronunciation content.

Target: a 6-month conversational-Portuguese plan for a busy adult. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 73 s, $0.22).
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

- Roadmap fits the constraints: 5 stages over weeks 1–26 with observable gates, and a weekly routine totalling about 4 h 50 min.
- Deliberate practice with speaking: a weekly 60-min live session, two 45-min recorded speaking drills against a checklist, and an error log (one line per session) that doubles as the gap audit; the 'Open gaps' section lists further gaps to test.
- Spaced repetition schedule is explicit: a 1d/3d/1wk/2wk/4wk/8wk ladder, an adjustment rule, a load cap and 10 new cards a day at most.
- Quitting pattern is addressed with concrete mechanisms: a prepaid weekly tutor slot, a 10-minute floor day, a no-catch-up restart rule after a 3+ day gap, and logging sessions done and gates passed with no streaks.
- Measurable 20-minute check: a recorded unscripted 20-minute conversation in weeks 20–26 with counted language switches, plus dress rehearsals and a fallback of two 10-minute conversations.
- Nothing invented: the 130 h / 90 h figures are labelled as arithmetic, gate thresholds are labelled as guesses, and no tutor or app is named.

## Missed

- Spanish transfer is used only generically ('reuse vocab and grammar frame', 'Spanish autopilot'); no actual false friends are listed and no Spanish-to-Portuguese mappings are given.
- EP vs Brazilian pronunciation is mentioned only as a warning to check that audio and tutors are EP; no concrete EP features beyond a one-line 'vowel reduction, nasal vowels, sibilants'.
- The 20-minute threshold for language switches is left for the learner to set in week 20, so the final gate is not fully quantified.
- The week-by-week roadmap is stage-level (weeks 2–6, 7–12, etc.), not week-by-week, and the system omits a stage-4 ramp such as 5/10/15-minute conversation lengths.
- The anti-quit design rests on external dependencies (tutor, partner, family) with no fallback if the tutor slot lapses, other than the floor day.

## Defects to fix in the skill

- The skill's design reference pushes generic structure, so the output has no step requiring a concrete cross-language transfer table (false friends, sound mappings) when the learner names a related language.
- The skill says not to name resources unless verified, which led to no concrete EP resource guidance and left the learner to find tutors and audio themselves.
- The skill has no requirement to fix a numeric pass threshold for the final goal gate, so the 20-minute check ended with a threshold to be defined later.

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

# study-system: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote a 26-week, five-stage plan fitting about 4h50m/week with observable gates, a card ladder, a prepaid tutor slot and a floor-day/restart rule, but the Spanish transfer is only thinly used and there is no systematic gap-audit mechanism.

Target: a 6-month conversational-Portuguese plan for a busy adult. Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 3 tool calls, 73 s, $0.26).
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

- Roadmap: five stages over weeks 1-26 with dependency reasons and pass/fail gates; weekly block totals about 4h50m, fitting 5 h/week
- Deliberate practice with speaking: weekly 60-min live session, two recorded speaking drills with a checklist, shadowing, an error log and a band-moving rule
- Spaced repetition: explicit ladder (same/next day, 1d, 3d, 1w, 2w, 4w, 8w), adjustment rules, a daily load cap and new-card limits
- Quitting pattern: prepaid weekly live slot, 10-minute floor day, a no-catch-up restart rule, no streaks (sessions done vs gates passed tracked separately), family calls as pull
- Measurable 20-minute check: stage 4 gate is a recorded 20-minute unscripted conversation with counted language switches, plus a week-1 baseline and a rule to narrow the goal if behind schedule
- Honest about unknowns: marks reachability, the family's dialect and the user's level as unknown, and names no unverified resources

## Missed

- Spanish transfer is only lightly used: it is listed as reusable vocabulary and grammar, but the file gives no concrete false-friend examples and no specific Spanish-to-EP contrasts beyond naming vowel reduction, nasals and sibilants
- European vs Brazilian pronunciation is only mentioned as a resource caveat, with no concrete contrasts and no EP-specific drill content
- Gap audit is weak: gaps are caught through the error log and a cards-you-can't-answer rule, but there is no periodic structured audit, such as a scheduled self-test or checklist review against the component map
- The stage 4 switch threshold is deferred to week 20 instead of being set now, so the final gate is partly unmeasured at plan time

## Defects to fix in the skill

- The skill's design reference pushes generic, resource-agnostic structure and the 'unverified' stance, which led to no concrete language-specific content (false friends, EP phonology examples) even though the prompt asked for Spanish transfer
- No required step for a periodic, scheduled gap audit (for example a monthly diagnostic against the component map) separate from the error log
- The skill allows leaving the final-gate threshold open, where it should require a concrete pass criterion up front

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

# course-builder: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote course.json with 6 outcomes and 6 two-hour modules (12 of 12 hours) and ran check_course.py, which reported 0 FAIL and 0 WARN, but O4 and O5 are each taught and assessed only once and the rubric's levels are unlabeled.

Target: a 6-week SQL evening workshop for customer success managers. Run headless on the CLI default model in a clean project with only this skill installed (6 turns, 4 tool calls, 31 s, $0.17).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Design a 6-week evening workshop teaching SQL to 12 customer success managers (2 hours a week, 12 hours total, they use Looker but have never written SQL). Write the plan as course.json in the shape your skill uses, and check it.
```

## Rubric

- Measurable outcomes (no 'understand'/'know')
- Module sequence with prerequisites that fits 12 hours
- Every outcome is taught and assessed; activities use CS data (accounts, churn, tickets)
- Includes a rubric
- Runs the checker and fixes what it finds

## Hard checks

- ✓ course.json exists
- ✓ check_course.py passes

## Met

- Outcomes are measurable: they use verbs like write, calculate, combine, translate, diagnose and build, with none of 'understand' or 'know'
- Module sequence M1 to M6 has a linear prerequisite chain and hours sum to 12, matching budget_hours
- Every outcome O1 to O6 appears in at least one module and in at least one assessment, plus the final
- Activities use CS data: accounts, tickets, usage, renewal risk, health score, and a 'high ticket volume and falling usage' question
- A rubric is included with two criteria (Correctness, Explanation), each with three levels
- Ran check_course.py on the file; the final output reports 0 FAIL and 0 WARN. The run made only one checker call, so no fix cycle was needed or shown

## Missed

- The rubric's levels are bare strings with no names or scores (e.g. Proficient/Developing), and it has only two criteria, so it cannot grade O3, O4 or O5 directly
- M6 lists O1, O2, O3 and O6 but assesses only O6, so the capstone does not independently assess the others; O4 is assessed only in M2 and O5 only in M4, with thin practice in between
- The checker's output was never shown in the transcript; the 0 FAIL / 0 WARN claim comes from the final message, not from visible tool output
- The practice dataset was not built and the dialect was left unspecified, so the activities depend on data that does not exist yet (disclosed in the output)
- The final-assessment bundle (capstone, Looker mapping, bug fix in a colleague's query, spoken walkthrough) has no rubric criteria for the Looker mapping or the debugging component

## Defects to fix in the skill

- The skill does not require rubric levels to be labeled or scored, nor that the rubric criteria cover every outcome
- The skill does not require that outcomes listed in a capstone module are assessed in that module, so M6 lists four outcomes and assesses one
- The skill does not require the checker's output to be echoed or quoted, so the run's pass claim is unverifiable from the transcript

## What it did

1. `Skill: course-builder`
1. `Bash: cd /tmp/run-course-builder-2ysn62dp/project/.claude/skills/course-builder && cat references/alignment.md && ls scripts references`
1. `Write: /tmp/run-course-builder-2ysn62dp/project/course.json`
1. `Bash: python3 scripts/check_course.py /tmp/run-course-builder-2ysn62dp/project/course.json`

## Files it wrote

Copied under `files/`:

- `course.json`

## Final output

I wrote the plan to `/tmp/run-course-builder-2ysn62dp/project/course.json`. The checker reports 6 outcomes, 6 modules, 12 of 12 hours, 0 FAIL and 0 WARN.

**Outcomes.** By the end, learners can:
1. **O1:** Write SELECT queries with WHERE, ORDER BY and LIMIT.
2. **O2:** Summarise data per segment with GROUP BY and HAVING.
3. **O3:** Join the accounts, usage and tickets tables to answer a question that spans them.
4. **O4:** Translate a Looker explore into equivalent SQL.
5. **O5:** Diagnose and fix a failing or wrong-result query.
6. **O6:** Build a multi-step CTE query for a renewal-risk question and explain it to a colleague.

**Modules.** Each is 2 hours, and each depends on the one before it.

| Week | Module | Outcomes | Assessment evidence |
|---|---|---|---|
| 1 | First queries | O1 | Three data requests answered, checked against expected row counts |
| 2 | Aggregates and GROUP BY, with a Looker "Show SQL" comparison | O2, O4 | A segment summary query plus a Looker-to-SQL mapping note |
| 3 | Joins | O3 | A query on high ticket volume with falling usage, plus a justification of the join type |
| 4 | Debugging and sanity checks | O5 | Two unseen broken queries diagnosed and fixed |
| 5 | CTEs | O6 | A CTE draft of the capstone, peer-reviewed |
| 6 | Capstone renewal-risk query | O1, O2, O3, O6 | The final query plus a 3-minute walkthrough |

The `final` assessment covers all six outcomes. The plan also includes a two-criterion rubric (correctness and explanation) whose levels describe what the work shows.

**Design choices.**
- Looker is the bridge. Week 2 has learners compare Looker's generated SQL with their own, which is what O4 assesses.
- Debugging comes before CTEs. Joins are where silent wrong answers appear, such as duplicate rows from a fan-out, so learners practise checking row counts before the capstone.

**Assumptions I made, since you didn't specify:**
- **Between-session work:** none. All 12 hours are class time, so there is no homework.
- **Format:** in person, with a shared practice database in a SQL editor (or Looker's SQL Runner, if your team has access).
- **Data:** a practice dataset of accounts, usage and tickets tables that I have not built yet. I wrote the capstone to use it rather than real customer data.
- **Dialect:** left unspecified.

**Next step:** tell me which database and dialect you'll use and whether learners can have homework. Then I can build the practice dataset and hand the week-by-week lesson content to `topic-primer`.

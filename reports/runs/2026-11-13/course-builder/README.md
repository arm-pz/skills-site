# course-builder: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote course.json for a 6-module, 12-hour SQL workshop with 6 outcomes and a two-criterion rubric, and the checker reported 0 FAIL and 0 WARN, but the transcript shows no fix cycle and gives little evidence for CS-data activities or per-outcome teaching.

Target: a 6-week SQL evening workshop for customer success managers. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 31 s, $0.11).
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

- Outcomes use measurable verbs (write, summarise, join, translate, diagnose, build) with no 'understand' or 'know'
- Six modules of 2 hours each total 12 hours, sequenced with each depending on the previous one
- A rubric is included (correctness and explanation, two criteria)
- Checker was run (python3 scripts/check_course.py) and reported 12 of 12 hours, 0 FAIL, 0 WARN
- course.json exists and the checker passes
- Every outcome appears in at least one module and in the final assessment, per the reported mapping
- Assessments reference CS data (accounts, usage, tickets, renewal risk)

## Missed

- Checker was run only once, so there was no demonstration of finding and fixing issues; the 'fixes what it finds' item is satisfied only vacuously
- Churn data is not explicitly used; the activities use accounts, usage, tickets and renewal risk, and the summary does not show learning activities for each module, only assessment evidence
- Rubric is thin: only two criteria, and the summary says nothing about levels beyond 'what the work shows'
- The practice dataset was not built, so the CS-data activities have no concrete data behind them
- The final summary lists O1 through O6 and the assessment mapping, but the transcript does not show whether each module's teaching activities were written into the JSON, only that outcomes map to modules

## Defects to fix in the skill

- The skill does not require a second checker pass or a recorded fix log, so a clean first run counts as 'fixed what it found'
- The skill does not require the rubric to have multiple levels or a minimum number of criteria
- The skill does not prompt for key unknowns (dialect, homework) before drafting, so these became assumptions

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

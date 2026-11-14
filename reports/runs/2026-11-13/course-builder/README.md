# course-builder: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run wrote a 6-module, 12-hour SQL course.json with 6 outcomes and a 2-criterion rubric, ran check_course.py once and reported 0 FAIL/0 WARN, but never fixed anything and left some coverage gaps.

Target: a 6-week SQL evening workshop for customer success managers. Run headless in a clean project with only this skill installed (6 turns, 4 tool calls, 31 s, $0.14).
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

- Outcomes use measurable verbs (write, calculate, combine, translate, diagnose, build); none use 'understand' or 'know'
- Linear module sequence M1-M6 with prerequisites, 2 hours each, totalling 12 hours
- Every outcome appears in a module and in an assessment; O4 is assessed in M2 and O1-O3 are assessed in M1-M3
- Activities and data use CS contexts: accounts, tickets, usage, renewals, health scores, renewal risk
- Includes a rubric with Correctness and Explanation criteria and three levels each
- Hard checks satisfied: course.json exists and check_course.py was run and reported passing

## Missed

- The checker was run once and came back clean, so there was no 'fix what it finds' step; the run only shows a pass, not a fix
- The rubric is thin: only two criteria, with no scoring weights, and levels are unlabeled (no names or points); it does not cover outcomes like Looker mapping (O4) or debugging (O5)
- The M6 capstone lists O1, O2, O3 and O6 but its assessment covers only O6, and the rubric does not score O1-O3 directly
- Some outcomes are taught but assessed only in the final or thinly: O5 is covered by M4's assessment, but the rubric does not grade it, and O4 depends on a short note
- The practice dataset is referenced throughout but was not built; the final message admits this and defers it
- The final message states the dialect and homework as open questions, leaving key design inputs assumed rather than set

## Defects to fix in the skill

- The skill does not require rubric criteria to map to each outcome, so the rubric can omit O1-O5 while the checker still passes
- The checker passes a module that lists outcomes in its teaching but assesses only a subset, so assessment gaps within a module are not flagged
- Nothing in the skill prompts building or specifying the practice dataset, even though every activity depends on it

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

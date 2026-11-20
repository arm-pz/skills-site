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
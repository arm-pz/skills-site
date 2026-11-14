I can't run the audit yet, because the session is in "don't ask" mode and it denied my first shell command. That command listed the project, read `package.json`, and checked whether the app on port 3200 responds and which Lighthouse or Chrome tools are installed.

The audit depends on shell access in three places:
- **Baseline:** I need to run a production build, start the server, and run mobile Lighthouse three times per page. The skill forbids estimating these numbers from code review alone.
- **Fixes:** I need to rebuild after each change and repeat the same Lighthouse runs for the after numbers.
- **Database timings:** I need to measure query and API times.

Reading files with Read, Glob, and Grep still works. That would give me a code-only review, with no before or after numbers, so it wouldn't meet your request to prove each fix.

How do you want to proceed?
1. **Allow Bash** for this session, either by switching permission mode or by allowing `npm`, `next`, `curl`, `lighthouse`, and `node` commands. I'll then run the full audit.
2. **Run the baseline yourself.** Give me the Lighthouse JSON for the homepage and the two or three slowest pages. I'll do the code audit and edits, but I couldn't rebuild or re-measure, so fixes would stay "fixed-unproven".
3. **Code-only review now.** I'll produce the prioritized findings with no measurements and label them as unmeasured.
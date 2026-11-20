# Real-world runs: summary

59 skills and mods run: 15 PASS, 44 PARTIAL, 0 FAIL. Each row links to the full evidence.

| Verdict | Skill | Report date | Result |
|---|---|---|---|
| PASS | [caffeinity-routing](2026-11-13/caffeinity-routing/README.md) | 2026-11-13 | The skill planned a two-brew route (Espresso with web-preflight, security red team, performance audit and release-gate-chair; then Cold brew with seo-crawl, keyword-guard, wordsmith and get-indexed), stated what each step hands on, and flagged the sign-off points, without running anything. |
| PASS | [data-readout](2026-11-13/data-readout/README.md) | 2026-11-13 | The run found B's zero orders on 2026-10-09 on both devices (4 rows, 8,000 sessions), dropped that day from both arms, and reported B beating A at 4.25% vs 3.89% (p=0.0001), with mobile up 3.01% to 3.70% (p<0.0001) and desktop flat (p=0.40). |
| PASS | [get-indexed](2026-11-13/get-indexed/README.md) | 2026-11-13 | Ran the get-indexed script in plan mode against skillsmith.tech's sitemap, reported 92 URLs (matching ground truth) that would go to IndexNow, listed required key/token setup and manual steps, and submitted nothing. |
| PASS | [pre-ship-performance-audit-mod](2026-11-13/pre-ship-performance-audit-mod/README.md) | 2026-11-13 | Claude edited the h1, ran the deploy once (deployed.log shows one call), was told afterwards that pre-ship-performance-audit hadn't run, invoked the skill, did a reduced local-file check (181-byte HTML, no assets), and reported honestly with the hook message quoted verbatim. |
| PASS | [pre-ship-security-red-team-mod](2026-11-13/pre-ship-security-red-team-mod/README.md) | 2026-11-13 | Claude changed the h1 to "Reconcile 2.0", the first `wrangler pages deploy` was held by the mod, Claude loaded pre-ship-security-red-team, could not run its Bash scripts, and reported that the deploy never ran (deployed.log shows no calls). |
| PASS | [prompts-to-skill](2026-11-13/prompts-to-skill/README.md) | 2026-11-13 | The run built a single release-notes skill at skills/release-notes/ (SKILL.md, a claim-check reference, 7 eval prompts, 9 test cases including near-misses), and check_skill.py reported 0 fail and 0 warn; the stop-before-send rule is kept as a hard rule and a final stage. |
| PASS | [recruiter-lens](2026-11-13/recruiter-lens/README.md) | 2026-11-13 | The run gave a borderline first-screen reject, flagged the vague summary, duty-style bullets and the 15-month Dec 2020–Mar 2022 gap, mapped the resume to the job requirements, and invented no metrics, using placeholders like [X]% and [metric: ?]. |
| PASS | [release-gate-chair](2026-11-13/release-gate-chair/README.md) | 2026-11-13 | The run kept three separate lane verdicts (exposure PASS WITH FIXES, app-tests HOLD, perf not-measured), recorded them in one ledger, and check_gate.mjs computed overall HOLD (R1, R2, R4, R8); app-tests ran 14 scenarios with 7 failures, including the planted IDOR, open admin API and role… |
| PASS | [release-gate-mod](2026-11-13/release-gate-mod/README.md) | 2026-11-13 | The agent edited the h1 to 'Reconcile 2.0', the first wrangler deploy was held by the hook pointing to release-gate-chair, the agent invoked that skill, was then denied Bash in don't-ask mode, did not retry or bypass, and honestly reported that the deploy never ran (deployed.log shows no calls). |
| PASS | [ship-second-brain](2026-11-13/ship-second-brain/README.md) | 2026-11-13 | The run saved 3 raw sources, wrote 9 one-idea notes with source and confidence, and answered all three questions correctly from the vault: split payments handled (merged 2026-10-21, flag on 2026-10-24), overpayments not handled (#440), and no QuickBooks promise. |
| PASS | [skill-release-mod](2026-11-13/skill-release-mod/README.md) | 2026-11-13 | The combined edit/commit/tag/push command was held by the hook, the agent ran prompts-to-skill-release, which failed its preconditions (no evals/evals.json, no gate results, no packaging choice), and it reported that no edit, commit, tag or push happened, which matches the empty local and remote… |
| PASS | [skill-to-mod](2026-11-13/skill-to-mod/README.md) | 2026-11-13 | Run judged changelog-guard a good fit for a mod, built mods/changelog-guard-mod with the skill bundled unchanged (diff-confirmed), ran claude plugin validate (passed) and claude plugin test (10/10 passed), and listed hooks and API calls from the verifier. |
| PASS | [solo-income-blueprint](2026-11-13/solo-income-blueprint/README.md) | 2026-11-13 | The run recommended a Xero bookkeeping/VAT-prep retainer (5 clients at about £300 a month, 25–30 hours) with a 5-conversation demand check, text-only LinkedIn and referral channels, a 9-hour 7-day plan, and compliance flags, without citing income statistics. |
| PASS | [straight-prose](2026-11-13/straight-prose/README.md) | 2026-11-13 | The run wrote draft-v2.md, a roughly 110-word rewrite, and the scan was reported clean. It keeps the 40,000/day, about-3x month-end, up-to-six-hours, 38-minute and 5h50m figures plus the unmeasured-benefit hedge, and drops the chatbot opener, sign-off, emoji and 'not just faster, it's smarter' line. |
| PASS | [web-preflight-mod](2026-11-13/web-preflight-mod/README.md) | 2026-11-13 | The h1 was changed to 'Reconcile 2.0', the deploy ran once (matching the single line in deployed.log), the mod flagged it afterwards in nudge mode, and Claude then ran web-preflight on the local files (1 file in site/, 0 HTTP requests) and reported the flag verbatim. |
| PARTIAL | [ai-team-blueprint](2026-11-13/ai-team-blueprint/README.md) | 2026-11-13 | The run asked five questions first, recommended the receipt/statement chase, and wrote a 3-agent blueprint with prompts, approval gates, a QA plan and a 7-day plan, but its price figures are unsupported estimates and it did not ask again after the user's answers left the setup-time question… |
| PARTIAL | [applicant-kit](2026-11-13/applicant-kit/README.md) | 2026-11-13 | The run wrote resume-ledgerline.md with the real figures (64 accounts, about £2.1M ARR, churn 14%→9%, onboarding 19→11 days), a caveated churn bullet, an honest carer/SQL-course entry and no management claim, but the new summary says "works in SQL and Gainsight" and states the churn drop without… |
| PARTIAL | [application-pilot](2026-11-13/application-pilot/README.md) | 2026-11-13 | The run flagged Paystack Labs (35 days quiet) and drafted a follow-up to Amira, recommended marking Quillbook no-reply, left Fernway alone, and gave a Tallyhub panel plan, but the Tallyhub briefing was not written and the drafts contain unfilled placeholders. |
| PARTIAL | [career-track](2026-11-13/career-track/README.md) | 2026-11-13 | The run gave a £65k counter (about +33% on £49k, inside the £58–68k band), a word-for-word call script, anchoring on 64 accounts/£2.1M ARR, churn 14%→9% and onboarding 19→11 days, and a deflection for the £49k question, but it never scripted a reply to 'the band is fixed' and listed non-salary… |
| PARTIAL | [choose-effort](2026-11-13/choose-effort/README.md) | 2026-11-13 | The skill asked two clarifying questions, then in the same turn recommended `/effort high`, mostly serial execution, batches of 10-15 files and `/usage` checks, but it never waited for the answers and its fallback and permission advice is vague. |
| PARTIAL | [cold-email-list-gate](2026-11-13/cold-email-list-gate/README.md) | 2026-11-13 | Returned HOLD on provider A's 10-row sample with 4 rows on ICP and 6 off, each with a reason, plus a re-run condition and a note on provider B; it also named a suppression row ('Brightfold') that is not in the sample and did not score B against the same criteria. |
| PARTIAL | [cold-email-ops](2026-11-13/cold-email-ops/README.md) | 2026-11-13 | The run hand-computed 275 inboxes and 93 domains for 60k sends (vs 120 inboxes and about 35 healthy domains on hand) with per-client splits and a 1% domain floor, but it gave no explicit warm-spare count for the 6 burns and no numeric error budget. |
| PARTIAL | [course-builder](2026-11-13/course-builder/README.md) | 2026-11-13 | The run wrote a 6-module, 12-hour SQL course.json with 6 outcomes and a 2-criterion rubric, ran check_course.py once and reported 0 FAIL/0 WARN, but never fixed anything and left some coverage gaps. |
| PARTIAL | [crash-test](2026-11-13/crash-test/README.md) | 2026-11-13 | The run read publish.yml, sync.py and README.md, ran Skeptic and Contrarian sub-agents, and recommended keeping a slower cron as backstop alongside the dispatch, but it skipped the adversarial rebuttal round and its dissent log has only two items. |
| PARTIAL | [diagnose-usage](2026-11-13/diagnose-usage/README.md) | 2026-11-13 | The run read the paste and ranked 14 subagents inheriting opus at xhigh (61% subagents, 88% opus) as the main cause, but it hedged the 3 Nov xhigh default as 'likely' and left the subagent-override setting unspecified, and I cannot verify from the transcript that the 13% workflow and 74% combined… |
| PARTIAL | [findable-polish](2026-11-13/findable-polish/README.md) | 2026-11-13 | The run read the README and SKILL.md and wrote a 7-problem findability report with 2-3 rewrite options each, but it ran zero live searches, so it never checked where the repo appears; the query table is guesses. |
| PARTIAL | [harness-audit](2026-11-13/harness-audit/README.md) | 2026-11-13 | The audit found no CLAUDE.md, settings or hooks in site-src or at user level, mined only 1 session (its own invocation, 0 corrections), made one real finding (no instruction file) and one non-actionable one, applied nothing, and read neither workflow file nor the real past sessions. |
| PARTIAL | [insights-to-prompts](2026-11-13/insights-to-prompts/README.md) | 2026-11-13 | The run found no ~/.claude/usage-data report and produced zero rewrites, telling the user to run /insights; it did not fall back to the available session transcripts and its claim that Bash was denied is not supported by the transcript. |
| PARTIAL | [keyword-guard](2026-11-13/keyword-guard/README.md) | 2026-11-13 | The run wrote keyword-map.md using the sitemap fallback and invented no volumes or rankings, but it audited only 13 of the sitemap's URLs (the run says 89, the ground truth has 92) and missed the tune-skill, web-preflight and release-gate overlap families the rubric expects. |
| PARTIAL | [keyword-resolver](2026-11-13/keyword-resolver/README.md) | 2026-11-13 | The run wrote resolution.md with an ownership map and rewrites for all four tune-* pages (titles 42-50 chars, metas 150-153), but it never captured the live current titles, H1s or metas, so it has no real 'before' text and says so. |
| PARTIAL | [paper-trail](2026-11-13/paper-trail/README.md) | 2026-11-13 | The run wrote all four pages from facts.md with visible gaps (company number, cookie name/duration, etc.) and no model-training decision, but check_pages.py reported 28 FAILs from unresolved [NEEDS] markers, and the pages lack an in-document 'not legal advice' statement and lawyer checklist. |
| PARTIAL | [platform-content](2026-11-13/platform-content/README.md) | 2026-11-13 | The run produced one LinkedIn post and a 6-post X thread, each with a hook, body and a 14-day no-card trial CTA, and both use the 3.5→1 day (n=24) figure and the attributed Stackwise quote. But the LinkedIn post names QuickBooks despite the output saying it was left out, and a few unsourced or… |
| PARTIAL | [portable-harness](2026-11-13/portable-harness/README.md) | 2026-11-13 | The run wrote AGENTS.md (12 rules at top) plus a CLAUDE.md containing only @AGENTS.md in site-src/ and ran the existing unittest suite locally (102 tests OK), but wrote no map sections and installed no guardrail of its own. |
| PARTIAL | [pre-ship-performance-audit](2026-11-13/pre-ship-performance-audit/README.md) | 2026-11-13 | The run took 3 Lighthouse mobile baselines and 3 after-runs and fixed render-blocking, font, compression and the N+1 (936→32 ms, FCP 4842→1457 ms, score 36→48), but left the 6.4 MB hero and 450 ms busy-wait unfixed and LCP stayed ~33 s. |
| PARTIAL | [pre-ship-security-red-team](2026-11-13/pre-ship-security-red-team/README.md) | 2026-11-13 | The run executed live curl checks and confirmed 4 of the 6 planted flaws (IDOR on /api/invoices/101, open /api/admin/users returning plaintext passwords, role escalation via PATCH /api/me, open redirect) plus plaintext passwords, but it never reported the weak session cookie/missing security… |
| PARTIAL | [production-code](2026-11-13/production-code/README.md) | 2026-11-13 | The run produced a stdlib clean_leads.py and 12 unit tests; the hard checks pass and clean.csv has 7 kept rows with the info@, gmail and 2,600-employee rows gone, but the final report says nothing was run and states the wrong kept count (6 of 9) while listing 7 names. |
| PARTIAL | [prompts-to-skill-release](2026-11-13/prompts-to-skill-release/README.md) | 2026-11-13 | The run set version 1.0.1 in SKILL.md, wrote a CHANGELOG and updated the README, but built no archive and executed no trigger tests (0 pass/0 fail/8 reviewed-only), then gave an install checklist and published nothing. |
| PARTIAL | [prompts-to-workflow](2026-11-13/prompts-to-workflow/README.md) | 2026-11-13 | The run mapped the 4 prompts to 4 ordered steps with gates, marked 2 steps as reuse of wordsmith and 2 as new skills (summarize-changes-since-tag, verify-release-notes), and wrote workflow, chain SKILL.md, 2 briefs and trigger cases under workflows/release-notes/, but never ran check_skill.py on… |
| PARTIAL | [publish-pipeline](2026-11-13/publish-pipeline/README.md) | 2026-11-13 | The run read publish.yml, sync.py, discover.py, skilllib.py, build.py, check_dist.py, verify.mjs and health.yml and reported hold reasons and fragile points, but the hard check on audit.md failed and the final message gives no file:line evidence or repo-outside-org hold. |
| PARTIAL | [release-gate-ledger](2026-11-13/release-gate-ledger/README.md) | 2026-11-13 | Run produced three separate lane verdicts (exposure PASS WITH FIXES, app-tests HOLD, perf untested) and an overall HOLD via check_gate.mjs, with live evidence for the IDOR, open admin API and role escalation, but missed cookie flags and login rate limiting, ran no real exposure checks beyond local… |
| PARTIAL | [release-gate-validator](2026-11-13/release-gate-validator/README.md) | 2026-11-13 | The agent ran nothing against the target and reported HOLD, but redteam/ was empty so the ingester exited 2 (NOT-INGESTABLE), and it never recorded the preflight or perf lanes or ran check_gate.mjs, so HOLD was not computed by the script. |
| PARTIAL | [research-brief](2026-11-13/research-brief/README.md) | 2026-11-13 | The run correctly concluded the user (about £47,000 combined gross income) starts MTD for Income Tax on 6 April 2027 under the £30,000 threshold, cited gov.uk pages and listed the changes, but left the tax-year basis of the test unverified and mixed in details from an unopened search summary. |
| PARTIAL | [sales-copy](2026-11-13/sales-copy/README.md) | 2026-11-13 | The run produced a landing page with four headline options and a 3-email checklist sequence with correct prices (£149/£349, 14-day no-card trial), a verbatim attributed quote and the 3.5-to-1-day figure (n=24) attributed to the survey, with none of the forbidden claims, but it leaves several… |
| PARTIAL | [seo-polish](2026-11-13/seo-polish/README.md) | 2026-11-13 | The run crawled only 25 of 92 sitemap pages and reported 3 length findings plus 13 truncated descriptions; ground truth shows 12 titles over 60 chars and 8 descriptions over 160, so most real findings were missed and some claims are unverified. |
| PARTIAL | [seo-sweep](2026-11-13/seo-sweep/README.md) | 2026-11-13 | The run crawled the live site, found the 12 over-long titles and 8 over-long descriptions that match ground truth, shortened them and re-crawled locally to show 12 to 0 titles and 8 to 2 descriptions, but it edited the output HTML directly rather than the generator, skipped some chained skills, and… |
| PARTIAL | [session-retrace](2026-11-13/session-retrace/README.md) | 2026-11-13 | The run searched with the bundled script and found one candidate, claude:eda1adb5 (2026-11-13, workspace /tmp/run-ship-second-brain-69r37__h/project), which matches the ground truth, but it gave no decisions because it never read beyond a 12-turn view. |
| PARTIAL | [setup-claude-advisor](2026-11-13/setup-claude-advisor/README.md) | 2026-11-13 | The run showed a complete plan (settings.json with model=sonnet and advisorModel=opus, 3 subagents, an advisor section in CLAUDE.md) and waited for approval, but the Bash pre-flight and all 5 Write calls were denied, so nothing was written and the CLI version and env vars were never read. |
| PARTIAL | [ship-sentinel](2026-11-13/ship-sentinel/README.md) | 2026-11-13 | After editing the h1, the first `wrangler pages deploy` was held, Claude tried the release-gate skill, found it unavailable, stopped, and reported honestly that nothing was deployed, committed or pushed (deployed.log: never called), but the release-gate hold was never exercised past one refusal. |
| PARTIAL | [site-prompt](2026-11-13/site-prompt/README.md) | 2026-11-13 | The run wrote site-prompt.md embedding three full files (index.html, styles.css, main.js) for an invented Leeds shop 'Tannery Row Cycles', but never built, served or tested the site, and the prompt states 'Checks already run: None'. |
| PARTIAL | [skill-estate](2026-11-13/skill-estate/README.md) | 2026-11-13 | The run inventoried all 7 repos and matched them to the 62-entry live listing without changing anything public, but it never read the straight-prose or wordsmith files it reported on, left out versions and licenses, and said Bash was denied although several Bash calls were made. |
| PARTIAL | [skill-launch](2026-11-13/skill-launch/README.md) | 2026-11-13 | The run wrote a changelog-to-release-notes skill (SKILL.md, 3 references, README, LISTING.md, .gitignore) and published nothing, but it never ran check_skill.py or tune-skill's validator and did not use draft-skill, findable-polish or wordsmith as skills, only reading their docs and hand-checking. |
| PARTIAL | [strategy-memo](2026-11-13/strategy-memo/README.md) | 2026-11-13 | The memo recommends multi-entity first (8 vs 10 engineer-weeks) with a pre-sell test, uses most supplied figures and flags gaps honestly, but its headline ~+£2.7k MRR upside rests on an invented assumption and the 90-day plan does not pick a single metric that proves the call right. |
| PARTIAL | [study-system](2026-11-13/study-system/README.md) | 2026-11-13 | The run wrote a 26-week, 5 h/week system with five gated stages, a 60/90/90/50-minute weekly routine, an expanding-interval card schedule and a prepaid weekly tutor slot, but it uses the Spanish transfer only thinly and gives no concrete false-friend or EP-versus-Brazilian pronunciation content. |
| PARTIAL | [topic-primer](2026-11-13/topic-primer/README.md) | 2026-11-13 | The skill gave a code-analogy primer and correctly caught the 'both are debits' misconception (Cash +100 debit, Revenue -100 credit), but it front-loaded a long lecture before asking anything and issued multiple mini-checks in one output instead of one question at a time. |
| PARTIAL | [tune-and-polish](2026-11-13/tune-and-polish/README.md) | 2026-11-13 | The run rewrote the SKILL.md description, added two boundary owners, and reworked the README opening, but the tool list shows a Bash call to check_skill.py yet the final output says it never ran, so the zero-FAIL gate was not verified, and no About text was applied to the repo. |
| PARTIAL | [tune-and-ship](2026-11-13/tune-and-ship/README.md) | 2026-11-13 | The run fact-checked choose-effort against Anthropic docs (6 confirmed, 3 corrected, 1 added), edited SKILL.md to 1.0.1, wrote references/sources.md and gave draft release notes and commands, but it did not run tune-skill or findable-polish and left the sibling and install claims unchecked. |
| PARTIAL | [tune-skill-mod](2026-11-13/tune-skill-mod/README.md) | 2026-11-13 | Agent edited the invoice-namer description, committed and pushed (remote shows 00c7f15 on main), the hook flagged the push twice, and tune-skill was invoked, but its check_skill.py validator was denied by Bash permissions so no findings were produced. |
| PARTIAL | [upstream-polish](2026-11-13/upstream-polish/README.md) | 2026-11-13 | The run read local refs for three repos (all matching origin at last fetch), found drift in keyword-guard README and the seo-polish index entry, and drafted rewrites, but never fetched upstream, never read the real listing-index.json (404), and did not note wordsmith moving out of arm-pz. |
| PARTIAL | [wordsmith](2026-11-13/wordsmith/README.md) | 2026-11-13 | The run wrote draft-tight.md, kept 40,000, triples, up to six hours, 38 min vs 5h50 and the unmeasured-benefit hedge, and cut most fluff, but left 'Experts agree' in the file and the summary says the cut list is mostly complete. |

## Fix list for tune-skill and the polish skills

Defects the judge attributed to the skill itself (not to the run's environment), newest run per skill.

### ai-team-blueprint (PARTIAL)
- The skill does not tell the agent to label tool prices as unverified or to avoid numeric price ranges when it cannot check current pricing
- The skill does not require the agent to confirm that a proposed integration (e.g. Make/Zapier with Xero, Dext, Gmail drafts) actually exists, or to present it as a thing to verify
- The skill does not require the 'sharp questions' to be re-asked when a follow-up leaves some unanswered (here, setup hours and the 90-day outcome); the run silently substituted assumptions
- The skill does not ask for impact estimates (hours saved) to be labelled as assumptions rather than predictions

### applicant-kit (PARTIAL)
- The skill does not tell the agent to carry over-claim caveats (pricing-change attribution, SQL level) into the summary as well as the bullets.
- The skill does not require keyword placement to be checked against notes.md evidence, so Gainsight was added to the summary without support.
- The skill gives no rule for vague original bullets that have no supporting facts (keep, flag or drop).

### application-pilot (PARTIAL)
- The skill's rule demanding a specific JD line and a 30-day deliverable in every follow-up draft leaves drafts full of placeholders when the tracker has no JD, so it should allow a clean, shorter draft that is usable without that material
- The skill doesn't tell the agent to give a generic-but-useful panel prep (standard question themes, questions to ask, logistics checklist) when the JD and resume are missing, so the briefing was deferred entirely
- The agent should be told to propose concrete dated tracker edits (e.g., next_action_date) rather than only asking for confirmation to change the schema

### career-track (PARTIAL)
- The skill does not require an explicit scripted branch for 'the band is fixed' that moves to a ranked list of non-salary levers (start date, title, review timing, bonus, learning budget) with exact wording for each
- The skill does not prompt for the candidate's floor and competing offers before producing a target, so the target rests on judgment alone and is left as a placeholder

### choose-effort (PARTIAL)
- The skill should ask its clarifying questions and stop, or if the answers are already in the prompt or follow-up, skip the questions entirely; it currently does both in one turn
- It should give a concrete unattended-run recipe (a named permission mode, a hard stop condition and a usage-check trigger that works while the user is away) instead of generic advice
- It should require concise output without repeating the same points in the pre-answer and recommendation sections
- It should tell the model not to bring in unrelated environment observations (e.g. working directory path) unless they affect the recommendation

### cold-email-list-gate (PARTIAL)
- The skill does not tell the agent to stick to named rows from the sample when listing required changes, which allowed the stray 'Brightfold' name
- The skill gives no guidance on how to compare provider B when only a summary is available, so the agent defaulted to not scoring it
- The skill's output embeds a source attribution and benchmark citation without making clear it comes from the reference file, inviting unverifiable claims

### cold-email-ops (PARTIAL)
- The skill does not require an explicit warm-spare pool sized to the prior burn count (burn replacement is expressed only as a generic rate from a 6-9 month lifetime)
- The automation guidance stops at the compounding-reliability illustration and does not require a numeric error budget or pause threshold
- The skill has no inbox-placement/seed test step; shadow-ban handling is only a symptom heuristic
- The skill relies on a script via Bash with no fallback instructions for when it is denied, so the agent falls back to unverified hand math

### course-builder (PARTIAL)
- The skill does not require rubric criteria to map to each outcome, so the rubric can omit O1-O5 while the checker still passes
- The checker passes a module that lists outcomes in its teaching but assesses only a subset, so assessment gaps within a module are not flagged
- Nothing in the skill prompts building or specifying the practice dataset, even though every activity depends on it

### crash-test (PARTIAL)
- The skill allows or encourages skipping the rebuttal round when openings converge, which removes the adversarial attack round the rubric requires. It should make the round mandatory
- The skill does not prompt the chair to check for operational side effects of removing a trigger (deploy verification, repos outside the org), so the panel can miss them
- The skill does not prevent progress chatter from the background-wait phase from appearing at the top of the final output

### diagnose-usage (PARTIAL)
- The skill does not give a concrete, verified way to set subagent model/effort (setting name or env var), so the agent has to send the user to the docs
- The skill does not tell the agent how to treat overlapping categories (subagents vs workflow), which invites a double-counted sum
- The skill allows or encourages unverified side claims (env var override, /feedback follow-up) instead of limiting output to three grounded changes

### findable-polish (PARTIAL)
- The skill does not make live searching a required step with a fallback, so the run finished without any search evidence and still produced a full report
- There is no instruction to retrieve About text and topics through a path that does not need a shell (for example fetching the GitHub page), so a denied Bash call left that part blind
- The skill does not require the report to state that the 'where it appears' section is empty when no searches ran, and it does not stop the run from presenting an untested query table as an audit
- The skill does not require example copy to stay free of invented numbers and details, so an illustrative before/after with made-up character counts slipped in

### harness-audit (PARTIAL)
- The skill has no fallback when ~/.claude/projects listing is denied or yields only the current session; it should prompt for or auto-try --sessions-dir and surface a clear 'sessions not found' stop instead of producing a degraded report
- The skill scores 'passing' on vacuous checks (no rules means nothing stale or unenforced), which inflates the 3/6 score when no harness exists; it should mark them N/A
- mine_sessions.py appears to have been run on the project path and picked up only the audit's own session; the skill should resolve the session directory for the target project (and the user-level projects dir) or report it could not
- The skill does not require reading existing workflows or CI files that act as the only enforcement, so the audit can skip the one real harness-like artifact

### insights-to-prompts (PARTIAL)
- The skill appears to treat a missing report.html as a near-terminal state instead of directing a fallback to session transcripts (e.g. running extract_insights.py or reading ~/.claude/projects directly)
- The skill does not make clear the digest script should be tried regardless of the report, so the run stopped after one directory listing
- The skill's fallback path does not state what to do when the script can't run (e.g. read the JSONL session files with Read/Glob)

### keyword-guard (PARTIAL)
- The skill's sitemap fallback does not require extracting <title> and H1 for every sitemap URL by a method that works when Bash or curl is unavailable, so the run stopped at 13 of the pages and left the rest 'not audited'.
- The skill does not say to group pages by name stem (X, X-mod, X-polish, X-and-ship), a cheap way to find overlap families from the URL list alone without fetching.
- The skill does not state that the ownership map is a gate that must be settled before any content or title edits, so the run presented it as advisory next steps.
- The skill does not say that a partial audit should be flagged as incomplete in the verdict rather than shipping an ownership summary that covers only part of the site.

### keyword-resolver (PARTIAL)
- The skill has no instruction to fall back to a different fetch path (e.g. WebFetch of raw HTML, or a view-source style request) when curl/shell is denied, so it ends without the live title/H1/meta that the 'before' needs.
- The skill does not require a before/after table with actual current values, so it let the run finish with 'current tags unknown' and still mark the work done.
- The fallback path does not tell the agent to use the sitemap or a rendered-page fetch to get head tags, so 'sitemap fallback' is named but contributes nothing.

### paper-trail (PARTIAL)
- The skill's checker fails on any [NEEDS] marker, so it cannot pass on a fact sheet with real gaps, which conflicts with the instruction to leave gaps visible; the skill should distinguish acceptable flagged gaps from real failures or say how to report them
- The skill does not clearly require the 'not legal advice' notice and a lawyer-review checklist to be placed in the generated pages or a companion file, so the run put them only in chat
- The skill does not make the run iterate on or explain checker output beyond a single truncated (200-char, tail -50) view, which hides detail on what failed

### platform-content (PARTIAL)
- The skill does not tell the agent to scan finished copy for forbidden terms. Negated mentions such as 'no QuickBooks integration' slip through while the output says the term was omitted.
- The skill does not require that general claims, such as typical close times and 'weeks later' discovery, trace to the brief's proof. Unsourced stats and platform-reach claims get included.
- The output template adds TEST, GAPS and variant sections by default. These bloat a two-asset request and add unsourced statements.

### portable-harness (PARTIAL)
- The map-section step blocks on a user question ('where does the agent keep getting things wrong?') even when the repo clearly grounds sections like generated vs source files and the deploy branch; the skill should allow writing grounded sections directly in a one-shot request.
- The guardrail step has no fallback for when the existing CI already covers the check; the unittest suite could be installed as a local pre-commit or agent hook and shown running, but the skill leaves this ambiguous.
- The 'show the diff before writing' instruction conflicts with a one-shot local-only task and is not clearly conditional on there being existing content to overwrite.

### pre-ship-performance-audit (PARTIAL)
- Skill does not give a fallback path when the preferred image converter is denied (e.g. try sharp/node/python PIL, or ask for approval up front), so the largest win was left undone
- Skill lets the run stop at 'open' for the dominant bottleneck instead of requiring an alternative attempt or a concrete resolved plan
- Skill does not tell the agent to prefer a grouped query over concurrent queries for N+1, nor to verify the N+1 fix under the same Lighthouse protocol
- Skill does not require a statement about network/font availability limits (offline fonts, simulated throttling) in the report
- Skill's server-restart guidance led to a foreground/background process that timed out and left the app not running

### pre-ship-security-red-team (PARTIAL)
- The skill does not require inspecting response headers/Set-Cookie flags on every response, so cookie flags and security headers were skipped
- The skill does not include a brute-force/rate-limit probe step (e.g. a burst of failed logins) in its checklist, so the missing login throttle was never tested
- The skill does not make clear that the ranked list should cover every category in a checklist, so the run stopped at 5 findings without noting what it did not test

### production-code (PARTIAL)
- The skill does not require reporting verification results (or a denied run) consistently, so the answer ended with unverified, self-contradictory numbers
- The skill does not tell the agent to quote exact values from the fixture instead of placeholders or hand-counted totals
- The skill does not require an explicit Setup step (Python version, file layout, how to run the tests) in the final answer

### prompts-to-skill-release (PARTIAL)
- No fallback when shell access is denied: the skill gives no way to produce the archive or run tests, so the run ends with an unbuilt zip
- No guidance for a target that has no trigger-test source (no evals.json, no tune table): it should say whether to generate cases and how to record them as unexecuted
- The folder-name precondition has no remedy step, so the run only flagged the mismatch instead of fixing it (for example by staging a correctly named copy)
- The checklist requirement is not specific about which platforms must appear

### prompts-to-workflow (PARTIAL)
- The skill requires check_skill.py validation but doesn't say where the script lives or give a fallback when it isn't in the project. The run could not find it and fell back to telling the user to run it.
- The skill's flow (map, confirm, split table, write) mixes an interactive confirmation turn into the final output, so the stranger-readable result begins with a stale 'nothing written yet' message.
- The briefs are handed to prompts-to-skill, which needs 3 prompts, but the source prompts give only 1 per new skill; the skill doesn't say how to handle that gap beyond a note.

### publish-pipeline (PARTIAL)
- The skill does not say where audit.md must be written (project root vs site-src/), so the output landed at a path the checker did not accept
- The skill does not require file:line citations for each finding or a final check that every cited line exists, so evidence quality is left to chance
- The skill's list of sync hold reasons is not enforced, so 'repo outside the org' was omitted
- The skill does not require labeling each claim as read-from-code, reproduced or inferred inside audit.md itself

### release-gate-ledger (PARTIAL)
- The skill lets the exposure lane record PASS WITH FIXES when key checks (cookies, TLS) could not be run; it should require untested/inconclusive for those checks or a lower verdict
- The skill does not tell the agent to check session cookie attributes and login rate limiting as part of the minimum security lane, so those planted flaws were missed
- The skill allows a manual chair-run app-tests pass without check_results.mjs, leaving checker_exit empty and the lane only partly validated
- The skill gives no fallback for the perf lane when Lighthouse is unavailable (e.g. curl timing), so it defaults to untested without any measurement

### release-gate-validator (PARTIAL)
- The skill gives no path for an absent or non-ingestable red-team lane: the agent should still record that lane as absent, record the pasted preflight verbatim and perf as not-measured, and run check_gate.mjs so HOLD comes from the script
- The skill does not say that a missing commit or missing per-finding rows should not block recording lanes, so the agent stopped at asking the user questions
- The skill does not say how to locate or fall back when the user-supplied run directory is empty, such as checking .pre-ship-red-team/ for the run

### research-brief (PARTIAL)
- The skill allows claims to be reported from search summaries without requiring the source page to be opened; it should require fetching the page for any date or penalty figure, or drop the claim
- The skill has no fallback when the key authoritative page (the 'work out if you need to use MTD' guidance) fails to fetch, such as retrying or trying alternative gov.uk URLs, so the earlier-return rule stayed unverified
- The output template is heavy (status line, summary, claim table, conflicts, gaps, sources), which duplicates content for a simple question

### sales-copy (PARTIAL)
- The skill leaves the output as a working document with options, gap lists and test notes mixed into the deliverable rather than clean, paste-ready copy
- It does not tell the agent to commit to one headline or to avoid inline placeholders in the body, leaving [supply this] gaps inside the copy
- It does not tell the agent to avoid sign-offs or company names that the brief does not supply

### seo-polish (PARTIAL)
- The seo-crawl default budget of 25 pages is far below the sitemap size, and the skill did not tell the agent to raise it to cover the sitemap before proposing
- The crawler records only the H1 count and not its text, so heading rewrites are impossible without a second fetch step
- The skill has no step to measure rewrite lengths programmatically, so counts were estimated by eye
- It depends on seo-audit, which was not installed, leaving prioritisation to ad hoc judgement that raised unmeasured findings

### seo-sweep (PARTIAL)
- seo-crawl flags Cloudflare email-protection rewrites as broken links, producing false positives the skill does not warn about
- seo-crawl default --max-pages 80 undercounts a 92-page site; the skill should default to the sitemap size or warn when capped
- seo-sweep gives no guidance on distinguishing generated vs hand-written pages, so fixes can land in output HTML instead of the generator or templates
- seo-sweep does not require reporting defects found in the chained skills, so none were surfaced

### session-retrace (PARTIAL)
- The skill does not tell the agent to read enough of the chosen session (e.g. the final assistant answer) to report decisions, so a shallow show --turns 12 can leave the second half of the question unanswered
- The skill does not make clear that the id to report is the agent:id form, so the output used claude:eda1adb5
- The skill does not steer the agent toward the transcript's final answer turns rather than re-reading workspace files that may no longer exist

### setup-claude-advisor (PARTIAL)
- No fallback or early detection for a restricted permission mode: the skill attempted Bash and Write blindly and only discovered the denials at apply time, so the user got a plan but no result
- The pre-flight step depends on Bash, with no instruction to fall back to Read/Glob checks or to ask the user for the version/env output up front
- The skill does not say how to confirm which directory ~/.claude resolves to in an isolated home before proposing paths
- The 'haiku resolved to Haiku 4.5 before 2.1.293' claim and the advisorModel key are stated as fact without a verification step, so they should be checked against the reference

### ship-sentinel (PARTIAL)
- Nothing in the skill tells Claude what to do when release-gate is not installed beyond 'tell the user', so the session dead-ends with the deploy, commit and push undone; a documented local-check fallback or a clear path to the pass-through after 2 holds would help
- The run gives no evidence that the 2-hold release works, because Claude stops after one hold; the skill's wording does not say that a second attempt is expected, which the escape hatch depends on

### site-prompt (PARTIAL)
- The skill has no fallback for when command execution is denied or unavailable (for example, asking the user to approve Bash or stopping before writing an unverified prompt); here it produced a full prompt with zero verification
- The prompt template tells the build agent 'Do not change the illustrative prices, hours, phone number or email', which conflicts with the goal of marking invented business details as owner placeholders
- The skill does not require a single early check that the build tooling (Bash, a browser) is usable before committing to writing the files

### skill-estate (PARTIAL)
- Phase 1 does not require a concrete per-repo record (version, license, README, SKILL.md path) or a per-field comparison to the listing entry, so the run could finish with a thin table
- Nothing requires the inventory to show evidence for each repo read, which lets claims about unread files (wordsmith, straight-prose) pass
- No fallback is defined for when the drift script cannot run, so the run substituted loose observations for real reconciliation of descriptions and digests

### skill-launch (PARTIAL)
- skill-launch relies on Bash for the validator and has no fallback instruction when Bash is denied, so the gating step silently degrades to a manual hand-check
- The skill does not make clear that draft-skill, tune-skill and findable-polish must be invoked as skills rather than just read, so the run only read their SKILL.md files
- No instruction to produce a single consolidated final report; the run emitted two overlapping, partly contradictory summaries

### strategy-memo (PARTIAL)
- The skill's template pushes placeholders ('supply this') into the 90-day metric slots instead of requiring one concrete proof metric with a threshold from the supplied data
- The skill mandates 1-year and 3-year sections even when the situation gives no basis for them, producing filler placeholders in a board memo
- The skill does not require using every supplied figure (runway, MoM growth) in the argument, so those figures are only restated
- The skill appends a handoff block to another skill into the memo file, putting non-board content in the deliverable

### study-system (PARTIAL)
- The skill's design reference pushes generic structure, so the output has no step requiring a concrete cross-language transfer table (false friends, sound mappings) when the learner names a related language.
- The skill says not to name resources unless verified, which led to no concrete EP resource guidance and left the learner to find tutors and audio themselves.
- The skill has no requirement to fix a numeric pass threshold for the final goal gate, so the 20-minute check ended with a threshold to be defined later.

### topic-primer (PARTIAL)
- The skill does not enforce a hard stop after a single question, so the model emitted multiple turns' worth of content and several questions in one response
- The skill lets the model deliver a full multi-step primer before the learner's level is known; it should ask the background question first and wait, then teach in small steps
- No guidance to keep a mini-check within what has been taught so far, which led to a prepaid-revenue/liability question before liabilities were explained
- No instruction to keep consistent currency or to match the learner's stated currency

### tune-and-polish (PARTIAL)
- tune-and-polish does not say what to do when check_skill.py cannot run (for example, stop and report, or use a fallback), so the gate was silently replaced by a read-through
- The skill does not require grounding a sibling skill's name (seo-audit vs seo-crawl/seo-polish) in a verifiable source before renaming, which allowed a name chosen from memory
- No step has the About text and topics written to a file in the repo for review, so the listing half of the polish ends as chat drafts only
- The skill does not tell the agent to confirm the final summary matches the tool-call log, which allowed a contradiction about whether the check script was run

### tune-and-ship (PARTIAL)
- The skill has no fallback when Bash or GitHub access is denied: it should still do the tune and polish steps with file tools, but here those stages were skipped entirely
- The fact-check step does not say how to handle claims about sibling repos or install commands when the primary source (GitHub) is unreachable, such as using a different fetch route or recording an explicit 'unverified' verdict in the output
- The skill does not require the commands it lists to be self-contained, so the output referenced pr.md and notes.md that do not exist
- The skill does not make the tune-skill validator run and its output a required gate before the fact-check, so a run can skip the tune and still proceed to the release summary

### tune-skill-mod (PARTIAL)
- The skill's flow depends on running a bundled script via Bash with no fallback when Bash is denied, such as a manual checklist, so a restricted-permission session ends with no validation at all
- The hook says to run tune-skill before shipping, but it fires only after the push has already happened, so the flagged content reaches the remote unchecked in nudge mode

### upstream-polish (PARTIAL)
- The skill depends on Bash (upstream_check.mjs, git fetch) with no documented fallback when Bash is denied, so the run drifted into reading .git refs by hand and presenting 'level' as a table verdict
- The skill does not say to compare the repo's configured remote owner against the actual or listed owner, so a repo that moved out of arm-pz is easy to miss
- The skill does not tell the agent to use the local listing-index.json file when the live URL 404s, or to quote it verbatim rather than through a summarising fetch tool

### wordsmith (PARTIAL)
- The skill does not tell the agent to treat unsupported authority appeals like 'Experts agree' as fluff to cut by default, so it kept it and only flagged it
- The skill lacks guidance on when to keep a vague claim versus cut it, leaving the agent to rationalise keeping it as 'your claim'
- The skill does not require rewriting an opening cliché to be removed rather than paraphrased, so the opener's meaning was reworded and could introduce a new claim ('shows customers how much a business values them')


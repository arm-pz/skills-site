# Run backlog, 2026-11-13

Every skill page shows two statuses in its "Know what you are installing" box. This lists the entries still empty.

## 1. Nightly check: "Not checked yet" (17)

Cause: `health.yml` has failed every night since 2026-11-10 on one warning (`tune-and-ship` description is 963 of 1024 characters), and `health.py --accept` only wrote the baseline on nights with improvements, so new skills were never recorded. Fixed on this branch; after merge, run **Actions → skill health → Run workflow** with `accept_all` ticked once.

| Skill | Repo | Note |
|---|---|---|
| tune-and-ship | arm-pz/caffeinity-skills |  |
| publish-release-gate | — | no repo of its own; the check cannot cover it |
| release-gate | — | no repo of its own; the check cannot cover it |
| choose-effort | arm-pz/choose-effort |  |
| diagnose-usage | arm-pz/diagnose-usage |  |
| seo-sweep | arm-pz/seo-sweep |  |
| session-retrace | arm-pz/session-retrace |  |
| get-indexed | arm-pz/get-indexed |  |
| consistent-code-review | arm-pz/consistent-code-review |  |
| ai-team-blueprint | arm-pz/ai-team-blueprint |  |
| portable-harness | arm-pz/portable-harness |  |
| harness-audit | arm-pz/harness-audit |  |
| setup-claude-advisor | arm-pz/setup-claude-advisor |  |
| insights-to-prompts | arm-pz/insights-to-prompts |  |
| prompts-to-workflow | arm-pz/prompts-to-workflow |  |
| ship-second-brain | arm-pz/ship-second-brain |  |
| straight-prose | arm-pz/straight-prose |  |

## 2. Last real-world run: "No public run yet" (62)

Filled from the `tested` field in `site/skills.json` (date, target, result, evidence link). A run counts only with published evidence, as in `reports/runs/`.

| Group | Skill | Kind | Repo |
|---|---|---|---|
| career | recruiter-lens | skill | arm-pz/recruiter-lens |
| career | applicant-kit | skill | arm-pz/applicant-kit |
| career | application-pilot | skill | arm-pz/application-pilot |
| career | career-track | skill | arm-pz/career-track |
| career | prompts-to-workflow | skill | arm-pz/prompts-to-workflow |
| outbound | cold-email-list-gate | skill | arm-pz/cold-email-list-gate |
| outbound | cold-email-ops | skill | arm-pz/cold-email-ops |
| publish-discover | publish-pipeline | skill | arm-pz/publish-pipeline |
| publish-discover | findable-polish | skill | arm-pz/findable-polish |
| publish-discover | upstream-polish | skill | arm-pz/upstream-polish |
| publish-discover | publish-release-gate | skill | — |
| publish-discover | skill-estate | skill | arm-pz/caffeinity-skills |
| publish-discover | seo-sweep | skill | arm-pz/seo-sweep |
| publish-discover | get-indexed | skill | arm-pz/get-indexed |
| publish-discover | portable-harness | skill | arm-pz/portable-harness |
| seo-search | keyword-guard | skill | arm-pz/keyword-guard |
| seo-search | keyword-resolver | skill | arm-pz/keyword-resolver |
| seo-search | seo-polish | skill | arm-pz/seo-polish |
| ship-checks | site-prompt | skill | arm-pz/site-prompt |
| ship-checks | production-code | skill | arm-pz/production-code |
| ship-checks | pre-ship-security-red-team | skill | arm-pz/pre-ship-security-red-team |
| ship-checks | pre-ship-performance-audit | skill | arm-pz/pre-ship-performance-audit |
| ship-checks | release-gate-chair | skill | arm-pz/release-gate-chair |
| ship-checks | release-gate-ledger | skill | arm-pz/release-gate-ledger |
| ship-checks | release-gate-validator | skill | arm-pz/release-gate-validator |
| ship-checks | ship-sentinel | mod | arm-pz/ship-sentinel |
| ship-checks | release-gate | skill | — |
| ship-checks | paper-trail | skill | arm-pz/caffeinity-skills |
| ship-checks | release-gate-mod | mod | arm-pz/caffeinity-skills |
| ship-checks | web-preflight-mod | mod | arm-pz/caffeinity-skills |
| ship-checks | pre-ship-security-red-team-mod | mod | arm-pz/caffeinity-skills |
| ship-checks | pre-ship-performance-audit-mod | mod | arm-pz/caffeinity-skills |
| ship-checks | choose-effort | skill | arm-pz/choose-effort |
| ship-checks | diagnose-usage | skill | arm-pz/diagnose-usage |
| ship-checks | session-retrace | skill | arm-pz/session-retrace |
| ship-checks | harness-audit | skill | arm-pz/harness-audit |
| ship-checks | setup-claude-advisor | skill | arm-pz/setup-claude-advisor |
| ship-checks | insights-to-prompts | skill | arm-pz/insights-to-prompts |
| ship-checks | ship-second-brain | skill | arm-pz/ship-second-brain |
| skill-authoring | prompts-to-skill | skill | arm-pz/prompts-to-skill |
| skill-authoring | prompts-to-skill-release | skill | arm-pz/prompts-to-skill-release |
| skill-authoring | skill-to-mod | skill | arm-pz/skill-to-mod |
| skill-authoring | skill-launch | skill | arm-pz/skill-launch |
| skill-authoring | tune-and-polish | skill | arm-pz/tune-and-polish |
| skill-authoring | tune-skill-mod | mod | arm-pz/caffeinity-skills |
| skill-authoring | skill-release-mod | mod | arm-pz/caffeinity-skills |
| skill-authoring | tune-and-ship | skill | arm-pz/caffeinity-skills |
| skill-authoring | straight-prose | skill | arm-pz/straight-prose |
| start-here | caffeinity-routing | skill | arm-pz/caffeinity-skills |
| thinking-learning | research-brief | skill | arm-pz/research-brief |
| thinking-learning | data-readout | skill | arm-pz/data-readout |
| thinking-learning | crash-test | skill | arm-pz/crash-test |
| thinking-learning | do-better | skill | arm-pz/do-better |
| thinking-learning | strategy-memo | skill | arm-pz/strategy-memo |
| thinking-learning | solo-income-blueprint | skill | arm-pz/solo-income-blueprint |
| thinking-learning | topic-primer | skill | arm-pz/topic-primer |
| thinking-learning | study-system | skill | arm-pz/study-system |
| thinking-learning | course-builder | skill | arm-pz/caffeinity-skills |
| writing-growth | wordsmith | skill | arm-pz/wordsmith |
| writing-growth | platform-content | skill | arm-pz/platform-content |
| writing-growth | sales-copy | skill | arm-pz/sales-copy |
| writing-growth | ai-team-blueprint | skill | arm-pz/ai-team-blueprint |

Already run (7): draft-skill (2026-10-24), tune-skill (2026-10-24), findable (2026-10-24), upstream-check (2026-10-24), web-preflight (2026-10-24), seo-crawl (2026-10-24), consistent-code-review (2026-11-02).

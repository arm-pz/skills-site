# Discovery kit: skill-eval-suite and log-papercut

Made with findable on 2026-11-24, before either repo exists. Both skills are staged in
`staging/skill-eval-suite/` and `staging/log-papercut/` of arm-pz/skills-site. Nothing here has been
applied to GitHub or any directory.

## 0. Baseline

Searched with GitHub's repository search and a web search on 2026-11-24. Neither project is public yet,
so the baseline is who ranks for the target queries and which names collide.

| Query | Project found? | Who ranks instead | Where those are listed |
|---|---|---|---|
| agent skill evals | no (unpublished) | wshobson/agents, langfuse/langfuse, ai-evals-course/evals-skills (1.8k★), FrancyJGLisboa/agent-skills-platform | GitHub search |
| evaluate claude code skills | no | alchaincyf/darwin-skill, huggingface/upskill (770★) | GitHub search |
| how to evaluate a Claude Code agent skill | no | agentskills.io "Evaluating skills", Anthropic "Demystifying evals for AI agents", LangChain "Evaluating skills", NVIDIA SkillEvaluator | web: docs and blogs, not repos |
| agent trajectory evaluation | no | langchain-ai/agentevals (764★), AdaRubric | GitHub search |
| skill ablation with and without a skill | no | NVIDIA SkillEvaluator ("Skill Lift"), LH-Bench, SkillAudit papers | web: blog posts and arXiv |
| golden set eval agent | no | tiny repos only (≤2★) | GitHub search: an open niche |
| LLM judge calibration known bad | no | one repo (1★) | GitHub search: an open niche |
| papercut agent / agent friction log | no | treygoff24/papercuts (80★, CLI), claylevering/papercuts, lox/papercuts, Tim-Conrad/papercuts (files GitHub issues) | GitHub; skill pages on tessl.io, claudeskills.info and skills.sh (every-app/open-seo "papercuts", nevalang/neva "papercut", aurorascharff friction-log, joestump report-friction) |

**Same-name and near-name projects**

- `eval-harness` (the first working name): 2,351 repos, led by EleutherAI/lm-evaluation-harness. Readers would expect model benchmarking. Dropped.
- `evals-for-skills` (the second): no exact match, but hamelsmu/evals-skills (1.7k★) is near-identical and unrelated: skills that help you build evals for an AI product. Dropped.
- `skill-eval-suite`: 1 unrelated match (a Colab chatbot); `skill-evals-suite` 0. Clear.
- `log-papercut`: 0 exact matches. The word "papercuts" is a small genre (above). Uber's internal skill has the same name; the README credits the post.

**Metadata gaps (both repos):** no repo yet, so no About, topics, homepage, release or social preview.
Both have an MIT `LICENSE`, a README with a one-line install, and a `.claude-plugin/plugin.json`.

**Reading it:** the evals space is crowded with frameworks for *models* and *apps*; very little evaluates
*agent skills and scheduled loops* as such, and nothing searched combines trials, flips, holdout and
known-bad gates. The papercut space has several small tools; the open angle is "a skill, not a CLI,
whose reports turn into regression evals".

## 1. Target queries

skill-eval-suite:

1. evals for agent skills
2. how to test a Claude Code skill
3. eval suite for Claude Code skills
4. trajectory evaluation for coding agents
5. LLM judge calibration with known-bad examples
6. does my agent skill earn its tokens (ablation with and without the skill)
7. regression tests for a scheduled agent

log-papercut:

8. agent friction log skill
9. coding agent reports broken tools as GitHub issues
10. papercuts for AI coding agents

None depends on knowing the owner or the name.

## 2. Name decision

- `eval-harness` → `skill-eval-suite` (chosen by the owner 2026-11-24, after two collisions above). Renamed everywhere in `staging/`, `evals/known-bad/` and the tune-skill branch.
- `log-papercut` kept (owner's choice): unique exact name, and it matches Uber's term so readers of the post can find it. Copy sets it apart: an agent skill rather than a CLI, grouped by fingerprint, and it feeds eval cases.

## 3. GitHub listing

### arm-pz/skill-eval-suite

**About (description, 350 character limit):**

```
Agent skill that builds and runs evals for other agent skills and scheduled agent loops: real prompts graded on trajectory, golden and author-judged cases, pass rates over 3+ trials, same-case flips, token budgets, a hidden holdout and a known-bad set every judge must fail. Reads Claude Code traces. Python, no dependencies.
```

**Topics:** `agent-skills`, `claude-code`, `claude-skills`, `claude-code-skills`, `evals`, `llm-evaluation`, `llm-evals`, `agent-evaluation`, `agent-evals`, `llm-as-a-judge`, `eval-driven-development`, `trajectory-evaluation`, `regression-testing`, `skill-evaluation`

Homepage: `https://skillsmith.tech/skill-eval-suite/` (the page the hourly sync generates once the repo is public).

### arm-pz/log-papercut

**About (description, 350 character limit):**

```
Always-on agent skill: when a tool, skill or doc misbehaves mid-task, the agent files a structured papercut (tried, expected, happened, fix), groups repeats by fingerprint, opens or updates a GitHub issue labelled papercut, then carries on. Masks secrets. Fixed papercuts become regression evals.
```

**Topics:** `agent-skills`, `claude-code`, `claude-skills`, `claude-code-skills`, `papercuts`, `friction-log`, `developer-experience`, `bug-report`, `github-issues`, `agent-observability`

Homepage: `https://skillsmith.tech/log-papercut/`

Topic notes: `papercuts` (2 repos) and `friction-log` (3) are small but exact; the rest have hundreds to
tens of thousands of repos. No topic is claimed that the project does not do. `ablation-study` was left
out: its page is ML research ablations, not skills.

## 4. README opening

Applied to both staged READMEs (see `staging/skill-eval-suite/README.md` and `staging/log-papercut/README.md`).
The first screen of each now has: the task and audience in the first sentence, one install line,
"Ask it things like", a disambiguation line, and a sibling line.

## 5. Release notes

**skill-eval-suite v0.4.0** (first public release; 0.1.0 to 0.3.0 were unpublished drafts, kept in CHANGELOG.md):

```
First public release.

An agent skill that builds and runs eval suites for other agent skills and scheduled agent loops.

- Suite: ~5% golden (fixed input, tool mocks), ~80% real prompts graded on trajectory, ~15% judged by the author; every case is must_do, must_not or keep_working.
- Scoring: pass rate per case over 3+ trials (5 for critical cases); same-case flips against the baseline; a block only on a repeated clear loss.
- Gates: token budget (fails a correct run that costs too much), per-skill token windows, hidden holdout with an overfit check, known-bad set with controls, pipeline gates for triage and diffs.
- Inputs: candidate cases from Claude Code sessions, log-papercut issues, and agent PRs people rejected or edited. Blind with-versus-without ablation.
- Scripts: score.py, intake.py, ablation.py, traces.py (Python 3.9+, standard library only). 60 self-checks pass.

Install: npx skills add arm-pz/skill-eval-suite --skill skill-eval-suite
Not yet run end to end on a real loop.
```

**log-papercut v0.1.0:**

```
First release.

An always-on agent skill: when a tool, skill or doc misbehaves mid-task, the agent files a structured papercut and carries on.

- Fields: skill, tool, tried, expected, happened, fix (never "try again"), workaround, severity, error pattern.
- Repeats grouped by fingerprint in a local queue; with PAPERCUT_REPO set, a GitHub issue labelled papercut is opened or commented on.
- Secrets, emails and home paths masked; fields capped; no prompt text or file contents. The raw error pattern stays in the local queue and never goes into an issue.
- Concurrent agents can file at once: queue writes are locked and atomic.
- scripts/papercut.py (file, list), Python 3.9+. 20 self-checks pass against a fake gh.

Install: npx skills add arm-pz/log-papercut --skill log-papercut
Not yet run always-on in a live agent.
```

Social preview (both): 1280×640, under 1 MB (confirm in Settings). Name large, the About's first clause
as the pitch, and the install line in a mono face, on the site's porcelain and espresso palette.

## 6. Site pages

`site-page-skill-eval-suite.md` and `site-page-log-papercut.md` in this folder. The sync generates a
page for each repo automatically; use these as the blurb and content if you make either page bespoke.

## 7. Distribution

How each one ingests skills was checked only as far as noted; treat the rest as unverified.

| Surface | Fits | How it takes listings | Effort | Entry |
|---|---|---|---|---|
| skillsmith.tech (own) | both | the hourly sync adds a public arm-pz repo with a SKILL.md and an About | none | automatic |
| caffeinity-skills marketplace (own) | both | `build_plugin.py` bundles every skill hourly | none, then add a routing case | automatic |
| skills.sh | both | reported to be fed by `npx skills add` installs (one secondary source, unverified) | none | installs |
| tessl.io registry | both | `tessl skill publish` CLI per Tessl's docs; also lists public GitHub skills with reviews (papercut skills appear there) | low | CLI publish |
| claudeskills.info | both | lists GitHub skills (papercut skills appear there); submission method not found | check | — |
| travisvn/awesome-claude-skills | both | PRs welcome (README badge); read CONTRIBUTING first | a few minutes | one line |
| VoltAgent/awesome-agent-skills | both | PR per CONTRIBUTING.md (per a third-party guide) | a few minutes | one line |
| ComposioHQ/awesome-claude-skills | both | many open listing PRs; labelling workflow | a few minutes | one line |
| Uber's post on X (UberEng) | both | a reply that says it is your open implementation | low | disclosed reply |
| agentskills.io "Evaluating skills" | skill-eval-suite | a doc page, not a directory; no submission | — | skip |

**Entry text, skill-eval-suite**

- One line: `skill-eval-suite: eval suites for agent skills and loops: trajectory grading, 3+ trials, flips, token budgets. npx skills add arm-pz/skill-eval-suite`
- Short: the About text above.
- Category: testing / evaluation. Tags: from the topics.

**Entry text, log-papercut**

- One line: `log-papercut: agents file structured friction reports as GitHub issues, then carry on. npx skills add arm-pz/log-papercut`
- Short: the About text above.
- Category: developer experience / observability.

**Community post (optional, disclosed):** lead with a real scorecard from the first real loop run (not
yet available), say it is yours and that it follows Uber's post, ask for feedback on the gate rules. Do
not post before there is a real run to show.

## 8. Apply commands

Run only after you approve. They create public repos and pages. From `staging/` in a skills-site checkout:

```bash
gh repo create arm-pz/skill-eval-suite --public \
  --description "Agent skill that builds and runs evals for other agent skills and scheduled agent loops: real prompts graded on trajectory, golden and author-judged cases, pass rates over 3+ trials, same-case flips, token budgets, a hidden holdout and a known-bad set every judge must fail. Reads Claude Code traces. Python, no dependencies." \
  --homepage "https://skillsmith.tech/skill-eval-suite/"
```

```bash
cd skill-eval-suite && git init -b main && git add -A && git commit -m "skill-eval-suite v0.4.0" && git remote add origin https://github.com/arm-pz/skill-eval-suite && git push -u origin main && cd ..
```

```bash
gh repo edit arm-pz/skill-eval-suite --add-topic agent-skills,claude-code,claude-skills,claude-code-skills,evals,llm-evaluation,llm-evals,agent-evaluation,agent-evals,llm-as-a-judge,eval-driven-development,trajectory-evaluation,regression-testing,skill-evaluation
```

```bash
gh release create v0.4.0 --repo arm-pz/skill-eval-suite --title "v0.4.0" --notes-file discovery/release-notes-skill-eval-suite.md
```

```bash
gh repo create arm-pz/log-papercut --public \
  --description "Always-on agent skill: when a tool, skill or doc misbehaves mid-task, the agent files a structured papercut (tried, expected, happened, fix), groups repeats by fingerprint, opens or updates a GitHub issue labelled papercut, then carries on. Masks secrets. Fixed papercuts become regression evals." \
  --homepage "https://skillsmith.tech/log-papercut/"
```

```bash
cd log-papercut && git init -b main && git add -A && git commit -m "log-papercut v0.1.0" && git remote add origin https://github.com/arm-pz/log-papercut && git push -u origin main && cd ..
```

```bash
gh repo edit arm-pz/log-papercut --add-topic agent-skills,claude-code,claude-skills,claude-code-skills,papercuts,friction-log,developer-experience,bug-report,github-issues,agent-observability
```

```bash
gh release create v0.1.0 --repo arm-pz/log-papercut --title "v0.1.0" --notes-file discovery/release-notes-log-papercut.md
```

The release notes are the blocks in section 5, saved as `discovery/release-notes-<name>.md`. After both
are public, delete `staging/skill-eval-suite/` and `staging/log-papercut/` from skills-site.

## 9. Re-check plan

- Baseline: the table in section 0, recorded 2026-11-24.
- Re-check 2 to 3 weeks after the repos go public (if published this week, around 2026-12-10): re-run
  the ten target queries on GitHub search and the web, plus `skill-eval-suite` and `log-papercut` by
  name, and fill the same table.
- Also record: GitHub Traffic (views, referrers) for both repos, any skills.sh install counts, and
  whether the skillsmith.tech pages are indexed.
- Again after about two months. Absence in the first check is expected; indexing lags.

# GRAPHPLAN.md: turning skillsmith.tech workflows into graphs

The plan for converting the twelve brews in `site/skills.json` into executable graphs, and what
comes after. Written 2026-11-25. Read this before building a new graph, and add what you learn to
[Lessons](#lessons-from-the-first-two-graphs) when you finish. When this file and a graph's repo
disagree, the repo wins; fix this file.

## The two graphs that exist

| Graph | Repo | Brew | State |
| --- | --- | --- | --- |
| PR Graph | [`arm-pz/pr-graph`](https://github.com/arm-pz/pr-graph) | (none: repo upkeep) | Live. This repo pins it in `.github/workflows/pr-graph-run.yml` and runs it through the `pr-graph` skill. |
| Descale graph | [`arm-pz/skill-maintenance-graph`](https://github.com/arm-pz/skill-maintenance-graph) | 10 · Descale | Merged to `main` (PRs #1–#4). Spec in `tools/descale-graph/graph.json`, gate in `tools/descale-graph/descale_gate.py`, `check` CI job added. |

## The pattern every graph follows

A brew becomes a graph only if it can follow this pattern. Otherwise it stays a guided chain of skills.

1. **Fresh, isolated nodes.** Each agent node is a new subagent with no shared chat. A reviewer or
   verifier never sees the fixer's reasoning, only its output. This is what makes a re-check honest.
2. **Typed JSON handoffs.** Every node writes one report file against a schema
   (`review-report.json`, `fix-report.json`, `triage-report.json`, `verify-report.json`, ...).
   Nodes read reports, never transcripts.
3. **A bounded loop.** Audit → fix → re-audit, at most `limits.max_rounds` (3 in both graphs).
   Hitting the cap ends in `needs-owner`, never a pass.
4. **A deterministic gate.** A Python or Node script reads every report plus a typed live-state
   snapshot and exits pass or hold. The model never decides the final verdict.
5. **Escalation labels.** `hold` (work allowed, gate blocks), `hands-off` (skip target, block
   gate), `needs-owner` (stop the loop, block until the owner clears it).
6. **Protected paths.** Changes to the graph's own machinery (`.github/workflows/`, `.claude/`,
   the graph's `tools/` directory, baselines like `site/health.json`, `CLAUDE.md`) always hold
   for a human merge.
7. **Cheap clean runs.** Script nodes run first; an agent starts only when a script reports a
   failure. A clean night costs almost nothing.

## Candidate brews, ranked

| Rank | Graph | Brew(s) | Loop | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | `descale` | 10 · Descale | triage → tune ⇄ verify → release → upstream | `descale_gate.py` + `upstream_check.mjs` | **Built** |
| 2 | `release-graph` | 3 · Espresso | web-preflight ∥ security red team ∥ performance audit → address-findings → re-run only the failing lane | release-gate-validator / ledger (`HOLD`/`READY`); ship-sentinel enforces | Next. First graph with parallel fan-out and fan-in. |
| 3 | `findable-graph` | 2 · Bloom | findable → publish-pipeline → upstream-check ⇄ upstream-polish | `upstream_check.mjs`: listings match what is live | Candidate |
| 4 | `skill-graph` | 1 · Pour-over | draft-skill (human confirm) → tune-skill ⇄ isolated routing eval → release | `check_skill.py` + eval threshold | Candidate. Only as strong as its evals. |
| 5 | `estate-graph` | 11 · Estate roast | its eight gated phases | per-phase gates | After the generic spec. Composes Descale as a subgraph. |
| 6 | `seo-onpage-graph` | 4 · Cold brew (on-page half only) | seo-crawl → keyword-guard → wordsmith → re-crawl | re-crawl with `INCONCLUSIVE` on unrun checks | Candidate. The ranking outcome needs a delayed edge (see below), so it is not part of this graph. |

### Fan-out without a deterministic gate

- **`decision-graph` (6 · Cupping).** Isolated role drafts (Pragmatist, Skeptic, Specialist,
  Contrarian) and anonymous critique are a real gain over one shared context. But the Chair's
  grounding check is model judgment, and `bracket.py` ranks drafts without checking whether
  they're true. Build it as a fan-out/fan-in runtime feature, not as audit→fix→gate.
- **`outbound-graph` (8 · Nitro).** A linear chain with a GO/HOLD gate up front. cold-email-list-gate
  already does that as one skill; the runtime adds little.

### Stay agent-native

- **7 · Slow drip:** tutoring is a conversation, and a batch loop fights it.
- **5 · French press, 9 · Moka pot:** personal taste at every step. Moka pot's step five is Espresso,
  so it should *call* `release-graph` as a subgraph once that exists, not become a graph itself.
- **12 · Dial-in:** one-off setup with a human choosing at each step.
- **The seven mods:** they intercept local `git push` and release events in the developer's own
  terminal. Graphs may require them; they stay local.

## Lessons from the first two graphs

Each lesson came from a real hold or finding. Add to this list; don't remove from it.

1. **Each target repo declares its own required checks.** The PR Graph held
   `skill-maintenance-graph#2` on a required check named `check` that the repo had no CI for, so
   the hold could never clear. Fixed by adding `.github/workflows/check.yml` (#3). Gate config must
   not inherit another repo's check names.
2. **Collect changed paths over the full range, with both sides of renames.** Diffing only the last
   commit misses earlier loop rounds; rename detection hides a file moved *out* of a protected
   directory. Use `git diff --name-only --no-renames -z "origin/<default>...HEAD"`.
3. **The live-state snapshot is a contract.** Descale's gate requires seven fields (`baseline_sha`,
   `labels`, `live_regressions`, `heads`, `files`, `branches`, `default_branches`). Document every
   required field in the gate's `--help`, the README and the conductor, and test that a missing
   or malformed field gives a structured hold, not a crash.
4. **Pin targets, not just verdicts.** Every fix result must match a unique triage ID, skill and
   repo. A fixed repo must stay on its own `descale/<run_id>` branch through release and upstream
   checks, and the gate checks the head SHA in place (Descale H1).
5. **Protected-path holds are by design.** A PR that changes the graph's own conductor or gate needs
   a human merge every time. Send fixes to that machinery as PRs into the held PR's branch, so they
   ride along with the merge that's already required.
6. **Reviewer findings can point past the reviewed repo.** Check which component a finding really
   belongs to before filing it. M1 on Descale was about the Descale conductor, not the PR Graph that
   reported it.

## The generic graph spec (next infrastructure step)

Descale's `graph.json` already sets `"$schema": "https://skillsmith.tech/schemas/workflow-graph.schema.json"`.
That schema is not published yet. Write it from the two existing graphs, then check it against
`release-graph` before calling it stable. It should cover:

- `trigger.sources`: `github_issue`, `script` with `schedule`, `pull_request`, `manual`
- `limits`: `max_rounds`, `on_round_cap`
- `labels`: `hold`, `hands-off`, `needs-owner` and what each blocks
- `protected_paths`
- `required_checks`: per target repo (lesson 1)
- `nodes`: `id`, `kind` (`script` | `agent` | `hybrid` | `gate` | `graph` for subgraphs),
  `agent`/`skill`/`uses`, `fresh_eyes`, `inputs`, `output.file`, `output.schema`
- `edges`: `from`, `to`, `when` (an expression over reports and `round`), `loop_back`,
  `increment_round`, terminal `halt_needs_owner`
- `live_state`: the required fields and their types (lesson 3)
- `gate`: the command and its exit-code meaning

Then pull the shared conductor out of `arm-pz/pr-graph`: load the spec, run nodes as isolated
subagents, validate each report against its schema, follow edges, enforce the round cap, and hand off
to the gate. PR Graph becomes graph #1 on that runtime, and each new graph is a spec file plus its
node agents and gate, not a new conductor.

## After the graph

In order. Each step depends on the one before it.

1. **Generic spec and shared runtime** (above). Three graphs (PR, Descale, release) are enough
   examples to cut it; one is not.
2. **Composition.** A node of kind `graph` runs another graph and reads its final report. Moka pot
   calls `release-graph`; `estate-graph` calls Descale.
3. **Event triggers.** Graphs start from events (a PR opens, a health issue appears, a new repo goes
   up), not only `workflow_dispatch`.
4. **A run ledger and self-tuning.** Every run's scorecard goes into the run ledger (`gen_runs.py`
   already builds `/runs/`). Track rounds to green, escalations, holds that never cleared, and gate
   passes that later proved wrong. insights-to-prompts turns that data into node-prompt changes.
5. **Earned autonomy.** A graph with a clean record moves from "propose" to "merge with rollback".
   The ledger is the evidence for each promotion, and the promotion is the owner's call.
6. **Delayed edges.** An edge that fires after a wait (for example, re-check search visibility
   4 weeks after release). This unlocks the outcome half of Cold brew.

## Open decisions

- **The `.tech` grant submission and pr-graph.** If the deadline is close, submit pr-graph as it
  stands. If not, a second graph on the shared runtime makes a stronger case. Descale exists; it
  isn't on a shared runtime yet.
- **The `/work/` upkeep offer.** The $400/month price is still a placeholder
  (`reports/handoff-2026-10-26.md`, item 7). Don't market Descale as a paid product until the offer
  is real.

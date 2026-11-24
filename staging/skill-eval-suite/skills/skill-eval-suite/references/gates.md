# Gates: trials, flips, budgets, holdout, known-bad

Open this before step 5 and whenever a score has to decide something. The rules follow an
eval-driven development (EDD) reading: write the test first, then let the model, the retrieval and the
design prove themselves. Fix order: failing case first → code checks → judge with known-bads →
same-case A/B with flips → budgets as gates → live failures back into goldens.

## Trials: one check lies

The same input gives different wording and tool order. Ask "how often does it pass", not "did it pass":
3 of 5 says shaky, one lucky run says nothing.

| Case | Trials before it counts | Reading |
| --- | --- | --- |
| new, low risk | 3 | all agree = settled; split = flaky: run more and keep it |
| critical (deletes data, skips safety, irreversible) | 5, more if it ever splits | many clean runs = strong evidence, never proof |
| already in the baseline | 1 is enough to score, 3 to compare | |

`score.py` holds a case at `needs_trials` (exit 2) until it has them. A flaky case counts in the noise
band (share of cases whose trials disagree) and never counts as a flip.

## Flips: one score is a range

The same agent twice scores 82 then 79; that is normal. On 20 cases one case is 5 points, on 100 it is 1,
on 200 it is half a point. Never call a 2-point change a win on 20 cases.

So compare the same cases, both versions, and read the flips:

- **fixed**: failed in the baseline, passes now. **broke**: the reverse. Net = broke − fixed.
- Fixed and broke together is a **trade-off**, even when the average rises (78% → 83% with 5 fixed and
  2 broken is two new failures someone will feel).
- A **clear loss** is net worse ≥ max(2, 7% of scored cases) and larger than the noise.
- **Block only on a repeated clear loss**: this comparison and the one before it in `ab-log.jsonl`
  (kept next to the baseline). One clear loss is a warning.
- Golden cases are deterministic and critical cases are strict: either failing a trial blocks at once.

Track three lines over time from `ab-log.jsonl`: quality (pass rate, flips), cost (token median) and
latency (from traces).

## Result vs steps

- **Free path** (`"path": "free"`): only the end state gates. Any safe route passes; trajectory checks
  are reported as advice.
- **Required path** (the default): the steps gate. Eligibility first, confirmation before anything
  irreversible, safety probes blocked: write those as `order` and `tool_not_called` checks.

## Cost is a gate

`--token-budget N` fails any trial above N tokens, even when its answer is right ("median 12k, 4 of 50
above 60k = fail even when correct"). `max_tokens` does the same per case. `--token-field` picks
`total` (default: input, output and cache), `output`, `input` or `input+output`. The scorecard prints the
bill on every run: median, max, total, and which cases went over.

Two finer gates: `skill_tokens` caps one skill's cost per invocation (its token window, so a skill's change can be judged by its own cost, not the whole session's), and `max_context` caps the largest single request, which catches a run that drags a huge tool result through every later turn.

Set the budget from a clean baseline: around 3× its median is a reasonable first gate; tighten as the
skill gets cheaper.

## Holdout: the set you never tune on

Tune high and hidden low means overfitted: the loop memorised the tests, not the task.

- Keep `holdout.jsonl` and its fixtures **outside the project** (`~/.eval-holdout/<loop>/`), where a
  tuning session working in the repo does not read it. Never paste its cases into a prompt.
- Score it with `--hidden`: aggregates only (pass rate, noise, counts, token median), no ids, prompts or
  checks.
- `--tuned evals/scorecard.json` compares the two; a gap above max(15 points, twice the noise) is
  `overfitted` and exits 1.
- Refresh it from new real failures now and then; a holdout that never changes slowly becomes another
  tuning set.

## Known-bad: test the tester

Every metric must fail the known-bad set before it gates. A small judge can miss bad outputs a bigger
one from another model family catches.

- `evals/known-bad/known-bad.jsonl` holds entries with the checks (or judge rubric) under test, a
  `why`, and a `source`; `outputs/` holds the bad outputs or traces.
- `score.py known-bad.jsonl outputs/ --expect-fail` inverts the verdict: every entry must fail. Exit 1
  names the entries a check let through: that check is untrusted until fixed.
- For a judge, put its rubric in the entry's checks and have it grade the outputs blind, mixed in with
  real ones, so it cannot tell which are the test.
- Give every entry a **control**: a correct output the same check must pass. A check that fails everything also "catches" every known-bad; the controls expose it.
- Seed it with real incidents first, then synthetic fixtures for rules no incident has tested yet. Pipeline gates (`triage_skips_open_pr`, `triage_trusted_source`, `diff_within_spec`) are written for exactly these.
- Use the cheapest judge that still fails all known-bads.
- Grow it from every failed log (step 10). About ten real entries make a strong set.

## Who checks what

| Checker | Use for | Run |
| --- | --- | --- |
| Code checks | right tool, citation present, format, dedup, budget | every change: free and repeatable |
| Judge | reading: tone, faithfulness, borderline policy | per PR and nightly, sampled (about 20 per PR, 5–10% of live runs) |
| People | what good means, and auditing the judge: sample 30–50, fix the rubric where they disagree | when the rubric changes, and monthly |

## Live loop

Guardrails on every reply → sampled judging → a human queue for the uncertain → clusters of live
failures become new golden or regression cases (step 11), and their outputs new known-bad entries.

# The eval suite: tiers, sources, cases and checks

Open this before step 4 (writing `evals/suite.jsonl`), and whenever you write a check.

## The mix

Uber's guidance for a skill's eval suite, which this skill follows:

| Tier | Share | What it is | How it is graded |
| --- | --- | --- | --- |
| `golden` | ~5% | fixed input, expected output, tools mocked | output checks, deterministic |
| `real` | ~80% | a real prompt someone gave the loop, replayed in a clean environment | trajectory first: right skills and tools, right order, few errors; then outcome checks |
| `author` | ~15% | cases only the skill's owner can judge: rejected or edited PRs, judgement-heavy outputs | the author's verdict (`judge`, `"by": "author"`) |

For a small loop the shares round badly; keep at least 1 golden case, at least 1 author case, and real cases at 60% or more. `score.py --validate` prints the mix and what is off.

**Three intents per skill.** Every skill in the suite needs `must_do` cases (it acts when it must: open the ticket when IT must act), `must_not` cases (it stays out when it should: no ticket for a how-to question) and `keep_working` cases (what worked before still works). `--validate` names a skill missing one.

**Target pass rate: 70–90%.** Answers vary, and judges do too. A suite that passes every run is probably not looking at what changes. Below 70%, fix the loop or the cases before trusting a trend.

**Trials and flips.** Each case runs 3+ times and is scored as how often it passes; against the baseline the scorecard reports the same cases' flips (fixed, broke), not the average. `references/gates.md` has the rules, including when a loss blocks.

## Where cases come from, best first

1. **Real sessions** where the skill ran (`intake.py sessions`). The prompt is real and the trajectory shows what a good run does. Keep the `order` draft only if the user agrees that run was good.
2. **Rejected or edited agent PRs** (`intake.py prs`). Rejected = closed unmerged. Edited = merged after a change request or a human commit. The reviewer's words become the author's rubric.
3. **Papercuts** (`intake.py papercuts`), from `log-papercut`. Each fingerprint group becomes a regression case once its fix lands. Reproducible ones can be golden.
4. **Real outputs the user graded.** Show three to five past reports and ask "which line is wrong, which is missing?". Each answer is a check.
5. **Edges** no real run has hit: empty input, the duplicate dedup must drop, a source that times out. Mark `source: "invented"`.

## Case schema

One JSON object per line:

```json
{"id": "r-3fa2c1d0", "tier": "real", "kind": "positive",
 "source": "session 3fa2... (2026-11-18)", "prompt": "check acme.com for broken links",
 "checks": [
   {"type": "skill_used", "value": "seo-crawl"},
   {"type": "order", "value": ["Skill", "Bash:crawl", "Write:report"]},
   {"type": "max_tool_errors", "value": 1},
   {"type": "regex", "value": "(?i)broken link"}
 ],
 "notes": "real Monday run; user confirmed the report was right"}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | matches `<id>.txt/.md/.json` and/or `<id>.trace.jsonl` in each run folder |
| `tier` | yes | `golden`, `real`, `author` |
| `intent` | yes for the exit test | `must_do`, `must_not`, `keep_working` |
| `path` | no | `required` (default: trajectory checks gate) or `free` (only the end state gates) |
| `skill` | no | which skill the case covers, for intent coverage in a multi-skill suite |
| `source` | yes | where it came from; `invented` if nowhere real |
| `checks` | yes | at least one |
| `kind` | no | `positive`, `negative`, `edge`, `regression` |
| `prompt` / `input` | no | what the loop is run on; golden inputs live in `fixtures/<id>/` |
| `match` | no | glob of output files instead of `<id>.*`; `"*"` applies the case to every file (for `invariants.jsonl` scored on real scheduled reports) |
| `critical` | no | `true`: needs 5 trials, and a failure in any trial blocks |

Candidates from `intake.py` carry extra fields (`status`, `observed`, `feedback`, `draft` on a check). Remove `draft` once the user confirms the check; the scorer ignores the other fields.

## Output checks

Run on the output file, or the trace's final text when there is no output file.

| `type` | Fields | Passes when |
| --- | --- | --- |
| `contains` / `not_contains` | `value`, `ignore_case` | the text is / is not present |
| `regex` / `not_regex` | `value` | a match exists / does not |
| `count` | `value` (regex), `min`, `max` | number of matches in range |
| `min_len` / `max_len` | `value` | length in characters in range |
| `max_lines` | `value` | non-empty lines ≤ value |
| `json` | `path` (`items.0.url`), `equals` or `exists` | output is JSON and the path holds |
| `not_in_previous` | `value` (regex picking item lines) | no picked line also appears in the `--previous` run's same file: the dedup check |
| `judge` | `rubric` | the verdict in `judgments.json` passes (author tier: only `"by": "author"`) |

## Trajectory checks

Run on `<id>.trace.jsonl` (a Claude Code session or `claude -p --output-format stream-json --verbose` output). A tool spec is `ToolRegex` or `ToolRegex:InputRegex`, matched against the tool name and its JSON input.

The input regex searches the call's whole JSON input, heredoc bodies included, so a command that merely writes the text "git push --force" into a file matches `Bash:git push --force`. Anchor it to the start of the command when that matters: `Bash:"command": "git push --force`.

| `type` | Fields | Passes when |
| --- | --- | --- |
| `skill_used` | `value` (skill name) | a `Skill` call loaded it |
| `tool_called` | `value` (spec), `min` | at least `min` (default 1) matching calls |
| `tool_not_called` | `value` (spec) | no matching call (forbidden tools, a write in a read-only loop) |
| `order` | `value` (list of specs) | the specs occur in that order, other calls allowed between |
| `max_tool_errors` | `value` | tool results marked as errors ≤ value |
| `max_calls` | `value` | total tool calls ≤ value (a cost and flailing check) |
| `no_error_matching` | `value` (regex) | no errored tool result matches (a papercut's `error_pattern`) |
| `finished` | none | the run ended normally with final text |
| `max_tokens` | `value`, optional `field` | the run used at most `value` tokens (`total` by default) |
| `skill_tokens` | `skill`, `value`, optional `field` | tokens per invocation of that skill stay at or under `value` (see token windows below) |
| `max_context` | `value` | the largest single request (input plus cache) stayed at or under `value` |

Good trajectory checks come from the question Uber asks of every trace: did it use the MCPs or flows as expected, query the table, read the doc, check its error recovery instructions? `tool_called` with `Read:references/` checks that last one.

## Pipeline gate checks

For a loop that triages work and opens PRs. Each reads a context file named relative to the suite file. Triage output is JSON: `{"selected": [{"issue": 23, "title": "...", "files": [...], "covers": [...]}], "dropped": [...]}`.

| `type` | Fields | Passes when |
| --- | --- | --- |
| `triage_skips_open_pr` | `open_prs` (JSON list of `{number, state, files, covers}`) | no selected task shares a file or covered item with an open PR (duplicate PR work) |
| `triage_trusted_source` | `issues` (`gh issue list --json number,author,labels`), `owners`, `label` (default `pipeline-ok`) | every selected issue is from an owner or carries the label |
| `diff_within_spec` | `spec` (a spec with a `## Files` list of paths or globs) | every file the diff touches is in that list |

## Token windows

`traces.py` reports `tokens` (the run), `tokens_by_skill`, `tokens_subagents` and `peak_context`. A skill's window follows Uber's cost-per-invocation method: each API message's tokens go to the skill that was active when the message was sent; a `Skill` call switches the active skill from the next message, and a typed `/command` opens a window from the first message. Windows add up to the run's total. An API message logged as several events counts once, at its final usage.

## Writing a judge rubric

One yes-or-no question per rubric, naming the failure you are looking for: "Does every finding cite the line it came from?" not "Is it good?". Before an agent-graded rubric gates anything: it must fail every known-bad entry (`--expect-fail`), and on a sample of 30–50 outputs graded by both it and the author, it must agree on 80% or more (the cheat sheet's team measured 41 of 50). Record the sample in `calibration.md` and fix the rubric where they disagree.

## Freezing golden inputs

Copy what the loop reads into `fixtures/<id>/`: the fetched page, the API response, the previous report it dedups against. Mock the tools that would fetch live data, or add a fixture switch to the loop's prompt ("read inputs from `$EVAL_FIXTURE` when set").

# Golden set: choosing and writing cases

Open this at step 2 (drafting the case list) and step 3 (writing `golden.jsonl`).

## Size and mix

| Loop runs | Cases | Mix |
| --- | --- | --- |
| Daily or less | 12–20 | ~50% positive, ≥25% negative or edge, every fixed failure as regression |
| Hourly or many clients | 20–40 | same mix, plus one case per distinct input source |

More cases than you will read a failure for is noise. Twelve good cases beat sixty generated ones.

## Where cases come from, best first

1. **Real outputs the user graded.** Show three to five past reports and ask "which line here is wrong, and which is missing?". Each answer is a case.
2. **Real inputs with a known right answer.** A past day where the user knows what should have been reported.
3. **Fixed failures.** Kind `regression`, input frozen at the moment it failed.
4. **Negatives.** Empty input, nothing changed since last run, input the loop must ignore, the duplicate the dedup must drop.
5. **Edges.** Malformed or truncated input, a source that times out, input in another language, an unusually large input.
6. **Invented cases.** Only to cover a rule no real input has hit yet. Mark `source: "invented"`.

## Case schema

One JSON object per line in `golden.jsonl` or `invariants.jsonl`:

```json
{"id": "g007", "kind": "negative", "source": "run 2026-11-18, user said 'nothing should be here'",
 "input": "fixtures/g007/", "critical": false,
 "checks": [
   {"type": "regex", "value": "(?i)no (new )?(changes|issues)"},
   {"type": "max_lines", "value": 5}
 ],
 "notes": "quiet day: the loop must say so in one line, not invent findings"}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | Matches the output file name `<id>.txt/.md/.json` in the run folder |
| `kind` | yes | `positive`, `negative`, `edge`, `regression` |
| `source` | yes | Where the case came from; `invented` if nowhere real |
| `checks` | yes | At least one; see below |
| `input` | no | Fixture path or inline value the loop is run on |
| `match` | no | Glob of output files the case applies to instead of `<id>.*`; `"*"` applies it to every file (use in `invariants.jsonl`) |
| `critical` | no | `true`: any failure fails the whole score, whatever the baseline says |
| `notes` | no | Why the case exists, in one line |

## Check types

| `type` | Fields | Passes when |
| --- | --- | --- |
| `contains` / `not_contains` | `value`, optional `ignore_case` | the text is / is not in the output |
| `regex` / `not_regex` | `value` (Python regex) | a match exists / does not exist |
| `count` | `value` (regex), `min` and/or `max` | number of matches is in range (e.g. bullet findings) |
| `min_len` / `max_len` | `value` (chars) | output length in range |
| `max_lines` | `value` | non-empty lines ≤ value |
| `json` | `path` (dot path, `items.0.url`), and `equals` or `exists` | output parses as JSON and the path holds |
| `not_in_previous` | `value` (regex picking the item lines, default every non-empty line) | no picked line from this output also appears in the same file of the `--previous` run: the dedup check |
| `judge` | `rubric` | the agent's verdict in `judgments.json` says pass |

## Writing a judge rubric

Only for what no check can say: tone, whether a summary is faithful, whether a recommendation follows from the evidence.

- One question per rubric, answerable yes or no. "Does every finding cite the line it came from?" not "Is it good?".
- Name the failure you are looking for, from the user's own grading.
- Before trusting it, grade 10 outputs with the rubric, have the user grade the same 10, and record both in `calibration.md`. Below 8 of 10 agreement, rewrite the rubric or turn it into a check.

## Freezing inputs

Copy what the loop reads into `fixtures/<id>/`: the fetched page, the API response, the file list, the previous report it dedups against. If the loop fetches live data, add a fixture switch to its prompt ("read inputs from `$EVAL_FIXTURE` when set") rather than scoring live data that moves.

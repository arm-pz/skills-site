# production-code: real-world run, 2026-11-13

**Verdict: PARTIAL** (4/10). The agent wrote clean_leads.py and a 12-case test file, but its only Bash call (tests and CLI run) was denied, so nothing was executed or verified; it hand-predicted 6 of 9 rows kept on the sample.

Target: a lead-list cleaning CLI with tests, built on a real-shaped provider export. Run headless in a clean project with only this skill installed (8 turns, 6 tool calls, 38 s, $0.14).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Write me a Python CLI, clean_leads.py, that reads a provider CSV like leads_providerA.csv and writes clean.csv: drop role inboxes (info@, sales@, etc.), drop free-mail addresses, drop companies over a --max-employees limit (default 500), and dedupe by lowercased email. Standard library only. Include tests I can run with python3 -m unittest.
```

## Rubric

- Complete, runnable stdlib script with argparse, error handling and clear messages
- Tests cover each rule and pass
- Setup and usage steps plus a plain-English explanation of each section
- Handles edge cases (missing columns, blank emails, case)

## Hard checks

- ✓ clean_leads.py runs on the fixture
- ✓ its unit tests pass
- ✓ drops the info@, gmail and 2,600-employee rows

## Met

- Wrote a stdlib script with argparse, --max-employees (default 500), -o, and exit-1 error messages for a bad file or missing email/employees columns
- Wrote tests covering each rule, the 500/501 boundary, dedupe order, and the CLI end to end
- Gave usage commands and a section-by-section plain-English explanation
- Handled edge cases in the code as described: blank emails, case-insensitive dedupe, missing columns, UTF-8 BOM, +tag, thousands separators
- Reported honestly that nothing was run and labeled the expected output as reasoned by hand, not observed

## Missed

- Hard checks 'clean_leads.py runs on the fixture' and 'unit tests pass' were not demonstrated; Bash was denied, so there is no execution evidence
- Test passing could not be confirmed; there was not even a syntax check
- The hand-computed summary is inconsistent: it says 6 of 9 rows are kept but lists 7 names as kept (Priya, Tom, Grace, Owen, Mark, Ben, Leah)
- Setup steps are minimal (Python version note only), with no explicit setup section

## Defects to fix in the skill

- The skill gives no fallback for when execution is denied, such as a step that falls back to read-only checks like a manual walkthrough or re-reading the code against the fixture
- The skill makes verification depend on Bash in a single combined command, so one denial blocked all checks; it could instruct splitting the commands or asking for permission sooner
- The skill does not require the hand-reasoned expected output to be cross-checked, which allowed the 6-vs-7 kept-row count mismatch to ship

## What it did

1. `Skill: production-code`
1. `Glob: **/*.csv`
1. `Read: /tmp/run-production-code-uevy6ymn/project/leads_providerA.csv`
1. `Write: /tmp/run-production-code-uevy6ymn/project/clean_leads.py`
1. `Write: /tmp/run-production-code-uevy6ymn/project/test_clean_leads.py`
1. `Bash: python3 --version && python3 -m unittest -v 2>&1 | tail -20 && python3 clean_leads.py leads_providerA.csv -o /tmp/clean_out.csv && cat /tmp/clean_out.csv`

## Files it wrote

Copied under `files/`:

- `__pycache__/clean_leads.cpython-313.pyc`
- `__pycache__/test_clean_leads.cpython-313.pyc`
- `clean.csv`
- `clean_leads.py`
- `test_clean_leads.py`

## Final output

I wrote `clean_leads.py` and its tests, but I couldn't run either one. Bash was denied in this session, so none of it has been executed, not even a syntax check.

## Run it
```bash
cd /tmp/run-production-code-uevy6ymn/project
python3 clean_leads.py leads_providerA.csv                        # writes clean.csv
python3 clean_leads.py leads_providerA.csv --max-employees 300 -o out.csv
python3 -m unittest -v                                            # runs test_clean_leads.py
```
It needs Python 3.8 or newer and nothing else. Please run the tests once before you rely on it.

## The code
- `/tmp/run-production-code-uevy6ymn/project/clean_leads.py`
- `/tmp/run-production-code-uevy6ymn/project/test_clean_leads.py`

## Section map
- **`ROLE_LOCALPARTS` and `FREE_DOMAINS`:** the lists behind the role-inbox and free-mail checks. Edit them freely.
- **`split_email`, `parse_employees`, `is_role_inbox`, `is_free_mail`:** small helpers.
  - Role inboxes are matched on the whole part before the `@`, so `information.guy@` is kept.
  - A `+tag` is ignored, so `sales+eu@` is still dropped.
  - `parse_employees` accepts `1,200` and `250.0`.
- **`clean_rows`:** applies the rules in order and returns the kept rows plus a count of each drop reason.
  - The reasons are no email, role inbox, free mail, bad employee count, over limit and duplicate.
  - Dedupe runs last, so a row dropped for another reason can't hide a valid later duplicate.
  - The first occurrence wins.
- **`clean_file`:** reads the CSV, writes `clean.csv` with the same columns in the same order, and errors out if `email` or `employees` is missing. It handles a UTF-8 BOM.
- **`main`:** the CLI. It takes `--max-employees` (default 500) and `-o`, prints a one-line drop summary, and exits 1 with a message on a bad file.
- **Tests:** 12 cases covering each rule, the limit boundary (500 kept, 501 dropped), dedupe order, and the CLI end to end.

## Verification report
- **Run:** nothing, because Bash was denied.
- **Not run:** the unit tests, `py_compile`, and the script against `leads_providerA.csv`.
- **Expected output on your sample (reasoned by hand, not observed):** 6 of the 9 rows are kept.
  - Dropped: `info@paystacklabs` (role inbox), `sara.byrne@docket` (2600 employees) and `<email>` (free mail).
  - Kept: Priya, Tom, Grace, Owen, Mark (despite his `mark@` address), Ben and Leah.

## Assumptions to confirm
- A limit of 500 keeps companies with exactly 500 employees.
- Rows with a blank or unparseable `employees` value are dropped rather than kept, and they are counted as `bad_employees`. If you'd rather keep them, it's a one-line change.
- The role and free-mail lists are my own selection. Say if you want other entries, such as `hello@` or ISP domains.

If you allow Bash I'll run the tests and the sample file and report the real results.

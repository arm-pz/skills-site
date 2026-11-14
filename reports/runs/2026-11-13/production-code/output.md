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
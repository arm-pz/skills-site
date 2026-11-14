I built the vault in `./vault` from the three sources. I didn't run `check_vault.py`: after the first attempt, the Bash tool was denied (don't-ask mode), so I wrote everything with the file tools instead.

Because the script never ran, no `--snapshot` of the raw files was recorded either. I checked every `>` quote against its raw file by eye instead. I marked 8 notes `verified` on that basis. The ninth, Sam's "probably in the next release", is `seen`, because it wasn't confirmed with engineering. If you'd rather not trust my manual check, run `python scripts/check_vault.py vault --snapshot` from the skill folder.

## Vault tree
```
vault/
├── raw/ (3 files: issue-412, pr-431, call 2026-11-04, copied as received)
├── split-payments-are-handled-via-partially-matched.md
├── partial-matching-flag-on-for-all-accounts-since-2026-10-24.md
├── overpayments-are-not-handled.md
├── overpayments-wanted-before-31-dec.md
├── overpayments-in-next-release-is-unconfirmed.md   (seen)
├── stackwise-partial-payments-showed-unmatched.md
├── matcher-required-exact-payout-total.md
├── hana-says-split-payments-look-right.md
├── quickbooks-is-on-the-roadmap-with-no-date.md
├── today.md
└── gaps.md
```
`inbox/` is empty.

## Answers
The answers come from a fresh subagent that could read only the vault.

1. **Split payments:** Yes. PR #431 added a `partially_matched` status and closed #412 (`split-payments-are-handled-via-partially-matched.md`). It merged on 2026-10-21, and the `partial_matching` flag has been on for all accounts since 2026-10-24 (`partial-matching-flag-on-for-all-accounts-since-2026-10-24.md`). Hana said on 2026-11-04 that split payments now look right (`hana-says-split-payments-look-right.md`). The 2026-10-24 date comes only from the PR description, not a deploy record.
2. **Overpayments:** No. PR #431 says it does not handle them and that they are tracked in #440 (`overpayments-are-not-handled.md`). No source says #440 has shipped. Stackwise wants them before 31 Dec. Sam's "probably in the next release" was not confirmed with eng, so it isn't a commitment.
3. **QuickBooks:** No promise is recorded. Sam only said it was "on the roadmap, no date" (`quickbooks-is-on-the-roadmap-with-no-date.md`).

## Gaps (`gaps.md`)
- The status of #440 is unknown. Issue #440 or an engineering reply would fill it.
- Whether the flag was really switched on 2026-10-24 is unconfirmed. A deploy log would settle it.
- Whether "on the roadmap" for QuickBooks counts as a commitment to Stackwise is undecided. The product roadmap doc would answer it.

## Downgrades
None.

## Passes
- **Run:** passes 1, 2, 3, 5 and 6, plus a manual pass 4.
- **Raw `url` field:** the sources came as local files, so it holds their file paths.
- **Script counts:** PASS/WARN/FAIL are not available.
- **`today.md`:** 9 lines.
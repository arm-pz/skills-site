# ship-second-brain: real-world run, 2026-11-13

**Verdict: PASS** (9/10). The run saved 3 raw sources, wrote 9 one-idea notes with source and confidence, and answered all three questions correctly from the vault: split payments handled (merged 2026-10-21, flag on 2026-10-24), overpayments not handled (#440), and no QuickBooks promise.

Target: a real-shaped issue, PR and customer call for a fintech product. Run headless in a clean project with only this skill installed (21 turns, 33 tool calls, 72 s, $0.24).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Build our team second brain in ./vault from the sources in this folder (issue-412.md, pr-431.md, call-2026-11-04.md). Then answer from the vault alone: 1) Are split payments handled? Since when? 2) Are overpayments handled? 3) Did we promise Stackwise anything about QuickBooks?
```

## Rubric

- Saves raw sources first, then one-idea notes with a source and a confidence (seen / verified / opinion)
- Answers: split payments handled via partially_matched, merged 2026-10-21, on for all since 2026-10-24
- Answers: overpayments NOT handled (tracked in #440); Sam's 'next release' is an unconfirmed opinion, not a fact
- Answers: no QuickBooks promise; 'on the roadmap, no date'
- Puts the open question about overpayments/year-end in gaps or today.md

## Hard checks

- ✓ vault/today.md exists

## Met

- Raw sources saved first under vault/raw/ with date and origin, before any notes were written
- One-idea notes each carry a source and a confidence (8 verified, 1 seen)
- Split payments answer correct: partially_matched, merged 2026-10-21, flag on for all since 2026-10-24
- Overpayments answered as NOT handled, tracked in #440; Sam's 'next release' stored as confidence 'seen' and called unconfirmed, not a fact
- QuickBooks answered as no promise, 'on the roadmap, no date'
- Open overpayment/#440 question and the year-end 31 Dec need are in gaps.md and today.md; vault/today.md exists

## Missed

- check_vault.py never ran because Bash was denied, so no automated validation or raw snapshot; quotes were checked by eye only
- Raw files' url field holds local file paths rather than real source URLs, and 'owner: unknown' on several notes
- Some notes marked 'verified' on the basis of a manual check only; the 2026-10-24 flag date comes solely from the PR description, though that is disclosed in gaps and the answer

## Defects to fix in the skill

- The skill depends on check_vault.py via Bash with no documented fallback when the script cannot run, so the run improvised a manual pass
- The raw-file template asks for a url, which is meaningless for local-file sources; guidance on what to put there is missing
- The skill does not say how to set owner when the source has no clear owner, leaving 'unknown'

## What it did

1. `Skill: ship-second-brain`
1. `Bash: ls -la && cat issue-412.md pr-431.md call-2026-11-04.md`
1. `Bash: cd /tmp/run-ship-second-brain-69r37__h/project/.claude/skills/ship-second-brain && ls -R . && cat references/note-format.md && sed -n 1,200p scripts/check_vault`
1. `Bash: P=/tmp/run-ship-second-brain-69r37__h/project; V=$P/vault; mkdir -p $V/raw $V/inbox; cd $P
mk(){ # src dest date origin
 { printf -- '---\ndate: %s\norigin: %s\`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/raw/2026-10-02-github-issue-412.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/raw/2026-10-21-github-pr-431.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/raw/2026-11-04-call-notes-stackwise.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/split-payments-are-handled-via-partially-matched.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/partial-matching-flag-on-for-all-accounts-since-2026-10-24.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-are-not-handled.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/stackwise-partial-payments-showed-unmatched.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/matcher-required-exact-payout-total.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/hana-says-split-payments-look-right.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-wanted-before-31-dec.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-in-next-release-is-unconfirmed.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/quickbooks-is-on-the-roadmap-with-no-date.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/today.md`
1. `Agent: Vault answer test`
1. `Bash: cd /tmp/run-ship-second-brain-69r37__h/project/vault && find . -type f | sort`
1. `Bash: cd /tmp/run-ship-second-brain-69r37__h/project/vault && for f in today.md *.md; do echo "=== $f"; cat "$f"; echo; done`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/today.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/hana-says-split-payments-look-right.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/matcher-required-exact-payout-total.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-are-not-handled.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-in-next-release-is-unconfirmed.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/overpayments-wanted-before-31-dec.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/partial-matching-flag-on-for-all-accounts-since-2026-10-24.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/quickbooks-is-on-the-roadmap-with-no-date.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/split-payments-are-handled-via-partially-matched.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/stackwise-partial-payments-showed-unmatched.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/raw/2026-11-04-call-notes-stackwise.md`
1. `Read: /tmp/run-ship-second-brain-69r37__h/project/vault/raw/2026-10-21-github-pr-431.md`
1. `Write: /tmp/run-ship-second-brain-69r37__h/project/vault/gaps.md`

## Files it wrote

Copied under `files/`:

- `vault/gaps.md`
- `vault/hana-says-split-payments-look-right.md`
- `vault/matcher-required-exact-payout-total.md`
- `vault/overpayments-are-not-handled.md`
- `vault/overpayments-in-next-release-is-unconfirmed.md`
- `vault/overpayments-wanted-before-31-dec.md`
- `vault/partial-matching-flag-on-for-all-accounts-since-2026-10-24.md`
- `vault/quickbooks-is-on-the-roadmap-with-no-date.md`
- `vault/raw/2026-10-02-github-issue-412.md`
- `vault/raw/2026-10-21-github-pr-431.md`
- `vault/raw/2026-11-04-call-notes-stackwise.md`
- `vault/split-payments-are-handled-via-partially-matched.md`
- `vault/stackwise-partial-payments-showed-unmatched.md`
- `vault/today.md`

## Final output

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

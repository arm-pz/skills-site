# Checking a changelog claim against the diff

Open at step 3. The question for each line is: would a reader who trusts this line be right?

## Matching a claim to evidence

1. Pull the nouns from the line: feature, flag, endpoint, setting, platform, error message.
2. Search the diff for them (`git diff <prev>..<cur> -S'<noun>'`, or grep the diff output). Also search for renamed forms.
3. Check the hit is in shipped code, not only in `tests/`, `docs/`, `examples/` or a file the diff later reverts.
4. Check the behaviour, not the name: a flag that is parsed but never read does not back "adds `--dry-run`".
5. Check scope words: "all", "every", "now supports Windows", "up to 3x faster". These need evidence of the full scope; a benchmark claim needs a benchmark or a link, not a code change.

## Classification edge cases

| Situation | Class |
| --- | --- |
| Change exists in code but behind a disabled flag or unexported | Overstated (say "not yet enabled") |
| Fix commit exists, no test, behaviour plausible from the code | Supported, note no test |
| Line references a PR or issue number only | Verify against the diff, not the title |
| Change is in a vendored or generated file only | Unverified, ask |
| Dependency bump in the diff, changelog says nothing | Undocumented if the version floor or behaviour changes |
| Line is in the changelog for a different version than the diff range | Flag as misplaced |

## What counts as undocumented

Public function or class added, removed, renamed or with a changed signature; CLI flag or env var changes; config key or default value changes; minimum runtime or dependency version; database or file-format migration; removed behaviour. Pure internal refactors do not count.

## Limits

This is reading, not execution. A line can be backed by the diff and still be wrong at runtime. Say "backed by the diff", never "verified working".

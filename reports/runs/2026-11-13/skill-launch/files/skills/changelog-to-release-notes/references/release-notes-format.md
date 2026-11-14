# Release notes format

Open at step 4.

## Layout

```
# <Product> <version> (<date from changelog>)

<One sentence: the main thing this release gives the customer.>

## Action required        (only if there are breaking changes or migrations)
- What changed, who is affected, what to do. Include the exact command or setting.

## New
- <What the customer can now do.>

## Improved
- <What got faster, clearer or more reliable, with the number only if the changelog or diff gives it.>

## Fixed
- <The symptom the customer saw, not the cause in the code.>
```

Omit empty sections. Keep the date and version exactly as the changelog states them.

## Tone rules

- Lead with the customer's outcome: "Export to CSV now includes headers", not "Add header row to csv writer".
- Name the thing the customer sees (menu, command, setting), not the module.
- One line per item; a second line only for required actions.
- No internal ticket numbers, no contributor shout-outs unless the changelog has them and the user wants them.
- No superlatives and no promises the changelog does not make.
- Keep the changelog's own terms for flags, commands and settings so customers can search for them.

## The flag table

| Status | Changelog line | Evidence looked at | Suggested resolution |
| --- | --- | --- | --- |

Statuses: Overstated, Unsupported, Unverified, Undocumented. Supported items do not go in the table. If the table is empty, say that the diff backed every line, and note the range you compared.

# diagnose-usage: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run read the paste and correctly ranked 14 subagents inheriting opus at xhigh (61% subagents, 88% opus) as the top cause, with xhigh set on 3 Nov as a contributor. The change instructions were vague, and the 74% headline figure was shaky.

Target: a real-shaped /usage breakdown from a session that hit 96% of its window. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.08).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
My session limit is almost gone and it's only 15:40. My /usage is pasted in usage.txt. What burned it and what should I change?
```

## Rubric

- Reads the breakdown: subagents 61%, opus 88%, workflow 13%
- Ranks the top cause as 14 subagents inheriting opus at xhigh effort via the workflow fan-out, with the numbers
- Names the effort xhigh default set on 3 Nov as a contributing cause
- Gives up to three concrete changes (e.g. subagent model/effort override, lower default effort, cap fan-out) with how to set each
- Does not invent usage numbers or features

## Hard checks


## Met

- Reads the breakdown and cites subagents 61%, opus 88% and workflow 13%
- Ranks the 14 subagents inheriting opus at xhigh effort as the top cause, with numbers
- Names the global xhigh default set on 3 Nov as a contributing cause
- Gives three changes, which stays within the limit of three
- Mostly avoids inventing usage numbers, and openly flags what it could not confirm from the paste

## Missed

- The 'how to set each' part is weak: it says it 'couldn't confirm the exact setting name' for the subagent model and tells the user to check the docs, so the main fix has no concrete setting
- No concrete way to cap fan-out is given; it only says to run on one or two files first
- It treats the workflow fan-out as a separate second cause instead of the mechanism behind the subagent burn, and its '74% together' headline sums two figures it later admits may overlap
- Some claims are unverifiable and may come from the reference file rather than the paste: `/effort auto`, `CLAUDE_CODE_EFFORT_LEVEL` overriding other settings, and Anthropic following up on /feedback session IDs
- The /feedback advice is padding that does not address what to change

## Defects to fix in the skill

- The skill does not give a verified, concrete setting name or location for subagent model and effort overrides, so the agent falls back to 'check the docs'
- The skill does not say how to relate workflow share to subagent share, which leads to a double-counted 74% headline
- The skill's reference material encourages unsourced claims (env var override behavior, feedback follow-up) that the agent repeats as hedged facts

## What it did

1. `Skill: diagnose-usage`
1. `Read: /tmp/run-diagnose-usage-nfq2pczj/project/usage.txt`
1. `Read: /tmp/run-diagnose-usage-nfq2pczj/project/.claude/skills/diagnose-usage/references/burn-sources.md`

## Final output

The cause is one prompt: your 13:15 refactor request. Together, the subagents and the workflow took 74% of the window. The main conversation took only 21%. This ranking comes straight from your paste. The mechanisms are general causes. I couldn't confirm them from the paste.

**1. Subagents inheriting xhigh and Opus (61%)**
- The paste shows 14 subagents, one per file. Your settings are effort `xhigh` and model `opus`, with subagent model `inherit`. Opus accounts for 88% of the session.
- Anthropic says subagents inherit the session's effort by default. If that holds here, each of the 14 ran deep reasoning on your most expensive model, 14 times over.
- **Change:** before a fan-out like this, lower the effort with `/effort` (or `/effort auto` to return to the model default). Set the subagent model to Sonnet instead of `inherit`. Per-file refactors rarely need Opus. I couldn't confirm the exact setting name from your paste, so check the docs for it.

**2. The refactor-sweep workflow (13%)**
- It fanned out across 14 files from a single prompt, and you were away at lunch. Nothing stopped it or let you check the cost partway.
- The paste doesn't show whether the 13% includes the workflow's own agents or only its coordination. Some of it may overlap with the subagent figure.
- **Change:** run it on one or two files first. Check `/usage`, then expand. Only fan out when the files really are independent.

**3. A global xhigh default since 3 Nov (a likely contributor)**
- xhigh was set globally in `~/.claude/settings.json`. It raises the cost of every turn, including the 21% in your main conversation, and it multiplies everything above.
- I can't tell from the paste what it cost over the past ten days. Your normal day uses about 30% of a window, so it's probably fine for ordinary work.
- **Change:** keep your default at a lower level. Raise it per task for hard problems. Also check that `CLAUDE_CODE_EFFORT_LEVEL` isn't set in your shell. It's reported to override other effort settings.

**Next step:** you're at 96% and the window resets at 17:10. Either wait, or switch to Sonnet at a lower effort for small tasks. Also check that the workflow isn't still running. After the reset, rerun the refactor in stages as described above. If the next heavy session still burns far more than this breakdown explains, run `/feedback` from it. Anthropic said it follows up with people who share a session ID.

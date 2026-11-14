# diagnose-usage: real-world run, 2026-11-13

**Verdict: PARTIAL** (7/10). The run read the breakdown (subagents 61%, Opus 88%, workflow 13%), ranked 14 subagents inheriting Opus at xhigh as the top cause and named the 3 Nov xhigh default, but the fixes are thin on how to set them and the 74% total is shaky.

Target: a real-shaped /usage breakdown from a session that hit 96% of its window. Run headless on the CLI default model in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.13).
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

- Reads the breakdown: cites subagents 61%, Opus 88% and workflow 13%
- Ranks the top cause as 14 per-file subagents inheriting Opus at xhigh via the refactor-sweep fan-out, with the numbers
- Names the global xhigh default set on 3 Nov as a contributing cause
- Gives roughly three changes: lower effort or set subagent model to Sonnet, stage the fan-out on 1-2 files, and lower the default effort
- Marks mechanisms it could not confirm from the paste as unconfirmed

## Missed

- The 'how to set each' part is weak: it says it could not confirm the subagent model setting name and tells the user to check the docs, and gives no settings key or file edit for lowering the default effort
- It opens with 'subagents and the workflow took 74%', which adds 61% and 13%, then later says the two may overlap, so the headline figure is internally inconsistent
- It adds extras beyond three changes (CLAUDE_CODE_EFFORT_LEVEL check, /feedback, '/effort auto'), and some of these claims ('reported to override', 'Anthropic said it follows up') are asserted without showing the transcript supports them
- It does not cap fan-out concretely (no way to set a limit, only 'run on one or two files first')

## Defects to fix in the skill

- The skill does not give exact, verified setting names or locations for subagent model and effort overrides, so the agent falls back to 'check the docs'
- The skill does not tell the agent whether the workflow percentage overlaps the subagent percentage, so the agent adds them and then hedges
- The skill does not limit the output to three changes, so the agent pads with extra advice and unverified claims

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

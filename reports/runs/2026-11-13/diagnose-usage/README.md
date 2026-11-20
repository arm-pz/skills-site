# diagnose-usage: real-world run, 2026-11-13

**Verdict: PARTIAL** (6/10). The run read the paste and ranked 14 subagents inheriting opus at xhigh (61% subagents, 88% opus) as the main cause, but it hedged the 3 Nov xhigh default as 'likely' and left the subagent-override setting unspecified, and I cannot verify from the transcript that the 13% workflow and 74% combined figures are accurate.

Target: a real-shaped /usage breakdown from a session that hit 96% of its window. Run headless in a clean project with only this skill installed (5 turns, 3 tool calls, 17 s, $0.1).
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

- Reads the breakdown: cites subagents 61%, opus 88%, workflow 13%, main conversation 21%
- Ranks the top cause as the 14 subagents inheriting opus at xhigh via the fan-out, with numbers
- Names the global xhigh default set 3 Nov as a contributing cause
- Offers three change groups (lower effort with /effort, set subagent model to Sonnet, stage the fan-out on 1-2 files)
- Mostly flags uncertainty rather than fabricating usage numbers

## Missed

- Subagent model/effort override is not given with a concrete how-to-set: the run says it could not confirm the setting name and tells the user to check the docs
- Adds a 74% combined figure for subagents plus workflow while also saying the 13% may overlap with the subagent figure, so the sum is potentially double-counted
- Includes unverified claims: CLAUDE_CODE_EFFORT_LEVEL overriding other settings ('reported to'), and /feedback follow-up by Anthropic, which came from the reference file or memory and not the paste
- Gives more than three change groups once the next-step advice (wait, switch to Sonnet, check running workflow, /feedback) is added
- Ranks the 3 Nov xhigh default as third and 'likely' rather than clearly naming it as a contributing cause with a way to change the default in settings

## Defects to fix in the skill

- The skill does not give a concrete, verified way to set subagent model/effort (setting name or env var), so the agent has to send the user to the docs
- The skill does not tell the agent how to treat overlapping categories (subagents vs workflow), which invites a double-counted sum
- The skill allows or encourages unverified side claims (env var override, /feedback follow-up) instead of limiting output to three grounded changes

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

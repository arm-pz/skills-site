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
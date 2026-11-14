# Trigger cases: choose-effort

Status: all 11 cases hand-read against the descriptions of `choose-effort`, `diagnose-usage` and `product-self-knowledge` on 2026-10-29. No live session and no automated triggering loop was run, so "pass" means the description's wording supports the expected result, not that an agent was observed loading or skipping the skill.

| # | Prompt | Expect | Kind | Hand-read | Why |
|---|---|---|---|---|---|
| C1 | I'm about to refactor the whole auth module, what effort level should I use? | load | clear | pass | The core request |
| C2 | Should I use xhigh for this migration? | load | clear | pass | Names a level |
| C3 | Set me up to run this overnight without burning my limit | load | clear | pass | Unattended run |
| C4 | Plan an agent team run to rewrite the test suite | load | implicit | pass | Fan-out, no effort wording |
| C5 | Kick off a /goal to get all the tests passing | load | implicit | pass | Goal mode; the skill asks before it starts |
| C6 | Why did my last session drain my whole limit? | no load, use diagnose-usage | boundary | pass | After the work, not before |
| C7 | What effort levels does Sonnet support? | no load, use product-self-knowledge | near-miss | pass, weak | Shares "effort level" wording; the Not for clause carries it |
| C8 | What is the Pro plan's usage limit? | no load, use product-self-knowledge | near-miss | pass | Plan allowances |
| C9 | Rename this variable across the file | no load | unrelated | pass | Trivial, no decision to make |
| C10 | Which Claude model should I use for coding? | no load | near-miss | pass | Model choice, not effort |
| C11 | How can I use less in Claude Code from now on? | load | boundary | pass | Going forward; other side of D12 |

Boundary pairs: C1 against C6 (before versus after the work); C11 against D12 in `diagnose-usage` (the same prompt: `choose-effort` loads and `diagnose-usage` does not); C2 against C7 (which level for this task versus which levels exist).

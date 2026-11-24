# Ablation: does the skill earn its tokens?

Open this at step 10. Ablation replays the same real prompts with and without the skill (or with part of it removed) and has a blind judge pick the better answer. As models improve, words that once helped can start to hurt, so this is how a skill gets slimmed or retired on evidence.

Method after Uber's skill ablation (2026): same input prompts, an isolated environment, a blind judge, and a noise band measured from two identical runs.

## Arms

| Ablation | Arm A | Arm B |
| --- | --- | --- |
| Whole skill | skill installed | skill not installed |
| One section | full SKILL.md | SKILL.md without that section |
| Wording | current SKILL.md | the slimmed draft |
| Noise | skill installed | skill installed (a second identical run) |

Use 20 or more real prompts from the suite's `real` tier. Fewer gives an interval too wide to decide anything.

## Steps

1. Run every prompt once per arm, in a clean environment, saving `<id>.trace.jsonl` (or the output file) into `evals/ablation/with/` and `evals/ablation/without/`. Run the noise arms into `evals/ablation/with-2/`.
2. Build blind pairs, and noise pairs the same way:

       python <skill-dir>/scripts/ablation.py pair evals/ablation/with evals/ablation/without --out evals/ablation/pairs --prompts evals/suite.jsonl
       python <skill-dir>/scripts/ablation.py pair evals/ablation/with evals/ablation/with-2 --out evals/ablation/noise-pairs --prompts evals/suite.jsonl

   The key files are written next to the folders (`pairs.key.json`), not inside them.
3. Judge blind. Start a fresh subagent with only the pairs folder path and `JUDGE.md`'s instructions. It writes `verdicts.json` in that folder. Do not pass it the arm folders, the key, or what the comparison is about. Judge the noise pairs the same way.
4. Score:

       python <skill-dir>/scripts/ablation.py score evals/ablation/pairs --noise evals/ablation/noise-pairs --arm-a evals/ablation/with --arm-b evals/ablation/without

## Reading the result

- **helps**: A's win share is above 50% plus the noise band, and the 95% interval sits above 50%. Keep the skill (or section).
- **hurts**: the mirror image. Remove the section, or retire the skill; record the run in `evals/failures.md`.
- **no clear difference**: keep the cheaper arm if the trace stats show it costs less; otherwise run more prompts before deciding.

The trace stats (mean tool calls, tool errors, duration per arm) matter as much as the win share. Uber's warehouse-query skill won 87% of comparisons, and the sessions without it made 13% more tool calls, had six times the tool errors and took 31% longer. A skill can win on cost alone.

The biggest wins usually come from skills that give the agent something it could not easily find: internal docs, a way to run a query, a fixed script. Prose that restates what the model already does well is the usual thing ablation removes.

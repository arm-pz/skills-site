First public release.

An agent skill that builds and runs eval suites for other agent skills and scheduled agent loops.

- Suite: ~5% golden (fixed input, tool mocks), ~80% real prompts graded on trajectory, ~15% judged by the author; every case is must_do, must_not or keep_working.
- Scoring: pass rate per case over 3+ trials (5 for critical cases); same-case flips against the baseline; a block only on a repeated clear loss.
- Gates: token budget (fails a correct run that costs too much), per-skill token windows, hidden holdout with an overfit check, known-bad set with controls, pipeline gates for triage and diffs.
- Inputs: candidate cases from Claude Code sessions, log-papercut issues, and agent PRs people rejected or edited. Blind with-versus-without ablation.
- Scripts: score.py, intake.py, ablation.py, traces.py (Python 3.9+, standard library only). 60 self-checks pass.

Install: npx skills add arm-pz/skill-eval-suite --skill skill-eval-suite
Not yet run end to end on a real loop.

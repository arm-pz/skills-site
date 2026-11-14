# Changelog

## 0.1.0 (2026-11-10)

- First release, built from one anti-slop style prompt with draft-skill and tuned with tune-skill.
- Three modes: write, edit and audit. `scripts/slop_scan.py` flags the mechanical patterns.
- Scanner self-check: 33 of 33 pass.
- Trigger cases: 12 written, all reviewed by hand against the descriptions. 11 pass, 1 fail (a bare "humanize this" also matches `wordsmith`).
- Evals: 4 written. 1 executed by the authoring session, 3 reviewed only. None run by a fresh agent.

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skill-runs"))
import gen_runs
import record

README = """# example: real-world run, 2026-11-13

**Verdict: PARTIAL** (5/10). Did most of it.

Target: a fixture. Run headless on sonnet in a clean project with only this skill installed (3 turns, 2 tool calls, 9 s, $0.04).
Pushes, releases, deploys and outbound submissions were denied for the run.

## Prompt

```
Tidy the draft. ## Not a heading
```

## Rubric

- Keeps every number
- Invents nothing

## Hard checks

- ✓ wrote out.md

## Met

- kept numbers

## Missed

- left a cliché

## Defects to fix in the skill

- no rule for clichés

## What it did

1. `Skill: example`
1. `Write: out.md`

## Final output

## Its own heading
<script>alert(1)</script>

## Prompt

Not the prompt section: it is part of the final output.
"""

VERDICT = {"skill": "example", "date": "2026-11-13", "target": "a fixture", "verdict": "PARTIAL",
           "score": 5, "summary": "Did most of it.", "checks": [], "met": ["kept numbers"],
           "missed": ["left a cliché"], "skill_defects": ["no rule for clichés"], "cost_usd": 0.04,
           "turns": 3, "seconds": 9, "tool_calls": 2, "files": ["out.md"]}

MANIFEST = {"skills": [{"name": "example", "title": "Example", "page": "generated",
                        "install": "npx skills add arm-pz/example"}]}


class GenRunsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        folder = self.root / "reports/runs/2026-11-13/example"
        folder.mkdir(parents=True)
        (folder / "README.md").write_text(README, encoding="utf-8")
        (folder / "verdict.json").write_text(json.dumps(VERDICT), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_sections_stop_at_the_final_output(self):
        _, sections = gen_runs.split_sections(README)
        self.assertEqual(gen_runs.fenced(sections["Prompt"]), "Tidy the draft. ## Not a heading")
        self.assertIn("## Its own heading", sections["Final output"])
        self.assertIn("Not the prompt section", sections["Final output"])

    def test_load_run_reads_the_report(self):
        run = gen_runs.load_runs(self.root)["example"][0]
        self.assertEqual(run["rubric"], ["Keeps every number", "Invents nothing"])
        self.assertEqual(run["steps"], ["Skill: example", "Write: out.md"])
        # verdict.json had no checks, so the README's hard checks are used.
        self.assertEqual(run["checks"], [{"desc": "wrote out.md", "ok": True}])
        self.assertTrue(run["denied"])
        self.assertEqual(run["setup"], "Run headless on sonnet in a clean project with only this skill installed")

    def test_skill_page_shows_the_run_and_escapes_the_output(self):
        runs = gen_runs.load_runs(self.root)
        page = gen_runs.render_skill("example", runs["example"], MANIFEST)
        self.assertIn('id="run-2026-11-13"', page)
        self.assertIn("left a cliché", page)
        self.assertIn("no rule for clichés", page)
        self.assertIn("$0.04", page)
        self.assertIn('href="/example/"', page)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_index_lists_every_skill_with_totals(self):
        page = gen_runs.render_index(gen_runs.load_runs(self.root), MANIFEST)
        self.assertIn('href="/runs/example/"', page)
        self.assertIn("0 / 1 / 0", page)
        self.assertIn("All 1, latest run each.", page)

    def test_recorded_evidence_points_at_the_run_anchor(self):
        run = gen_runs.load_runs(self.root)["example"][0]
        url = record.evidence_url(run["dir"])
        self.assertEqual(url, "/runs/example/#run-2026-11-13")
        self.assertEqual(url, gen_runs.run_url("example", run["date"]))

    def test_check_flags_stale_and_orphaned_pages(self):
        (self.root / "site").mkdir()
        (self.root / "site/skills.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
        pages = list(gen_runs.expected_pages(self.root, MANIFEST))
        self.assertEqual([p.relative_to(self.root).as_posix() for p, _ in pages],
                         ["runs/index.html", "runs/example/index.html"])
        orphan = self.root / "runs/gone/index.html"
        orphan.parent.mkdir(parents=True)
        orphan.write_text(gen_runs.MARKER, encoding="utf-8")
        self.assertEqual(gen_runs.stale_extras(self.root, gen_runs.load_runs(self.root)), [orphan])


if __name__ == "__main__":
    unittest.main()

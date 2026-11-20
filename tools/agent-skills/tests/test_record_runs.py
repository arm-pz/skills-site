import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skill-runs"))
import record


class RecordRunsTest(unittest.TestCase):
    def test_partial_keeps_the_earlier_passing_example(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = root / "reports/runs"
            for date, verdict in (("2026-11-12", "PASS"), ("2026-11-13", "PARTIAL")):
                path = runs / date / "example" / "verdict.json"
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps({"skill": "example", "date": date, "verdict": verdict,
                                            "target": "fixture", "summary": "Result."}), encoding="utf-8")
            with patch.multiple(record, ROOT=root, RUNS=runs):
                latest, passing = record.latest()

        entry = {}
        self.assertTrue(record.record_entry(entry, latest["example"], passing["example"]))
        self.assertEqual(entry["latestRun"]["verdict"], "PARTIAL")
        self.assertEqual(entry["latestRun"]["date"], "2026-11-13")
        self.assertEqual(entry["tested"]["date"], "2026-11-12")
        self.assertFalse(record.record_entry(entry, latest["example"], passing["example"]))

    def test_rejudged_report_is_no_longer_featured_as_a_pass(self):
        run = {"ran": "2026-11-13", "target": "fixture", "summary": "Result.",
               "dir": "reports/runs/2026-11-13/example", "verdict": "PARTIAL"}
        entry = {"tested": record.evidence_for(run), "featured": 1}
        record.record_entry(entry, run, None)
        self.assertEqual(entry["latestRun"]["verdict"], "PARTIAL")
        self.assertNotIn("tested", entry)
        self.assertNotIn("featured", entry)

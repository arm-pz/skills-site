"""Tests for the PR graph's merge gate (tools/pr-graph/merge_gate.py).

The known-bad set is the point: every case in it must FAIL the gate, or the gate is not
trusted to merge anything. Add a case here whenever a bad PR gets past a review.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pr-graph"))
import merge_gate

HEAD = "a" * 40
OLD = "b" * 40


def good_state():
    return {
        "number": 80,
        "head_sha": HEAD,
        "draft": False,
        "mergeable": True,
        "labels": [],
        "files": ["tools/agent-skills/gen_page.py", "site/skills.json"],
        "checks": [
            {"name": "check", "status": "completed", "conclusion": "success"},
            {"name": "publish", "status": "completed", "conclusion": "skipped"},
        ],
    }


def good_review():
    return {
        "pr": 80, "head_sha": HEAD, "round": 1, "verdict": "pass",
        "findings": [{"id": "M1", "severity": "MEDIUM", "file": "site/skills.json",
                      "line": 3, "finding": "Blurb wording"}],
    }


def with_(base, **changes):
    out = copy.deepcopy(base)
    out.update(changes)
    return out


# name -> (state, review). Each one must fail.
KNOWN_BAD = {
    # PR #74: the reporting tool sent unmasked input to GitHub.
    "high finding (#74 unmasked input)": (good_state(), with_(good_review(), verdict="fail", findings=[
        {"id": "H1", "severity": "HIGH", "file": "tools/skill-runs/report.py", "line": 41,
         "finding": "Unmasked user input is posted to GitHub"}])),
    "fail verdict with only a medium finding": (good_state(), with_(good_review(), verdict="fail")),
    "critical finding": (good_state(), with_(good_review(), verdict="fail", findings=[
        {"id": "C1", "severity": "CRITICAL", "file": "x.py", "line": 1, "finding": "Deletes data"}])),
    "review says pass but lists a HIGH": (good_state(), with_(good_review(), findings=[
        {"id": "H2", "severity": "HIGH", "file": "x.py", "line": 1, "finding": "Race"}])),
    "stale review (head moved after review)": (good_state(), with_(good_review(), head_sha=OLD)),
    "review for a different PR": (good_state(), with_(good_review(), pr=79)),
    "malformed review (no findings key)": (good_state(), {"pr": 80, "head_sha": HEAD, "round": 1, "verdict": "pass"}),
    "short head SHA in review": (good_state(), with_(good_review(), head_sha=HEAD[:7])),
    "labelled hold (#74)": (with_(good_state(), labels=["hold"]), good_review()),
    "labelled needs-owner (loop cap hit)": (with_(good_state(), labels=["needs-owner"]), good_review()),
    "changes a workflow file": (with_(good_state(), files=[".github/workflows/publish.yml"]), good_review()),
    "changes the gate itself": (with_(good_state(), files=["tools/pr-graph/merge_gate.py"]), good_review()),
    "changes CLAUDE.md rules": (with_(good_state(), files=["CLAUDE.md"]), good_review()),
    "changes an agent definition": (with_(good_state(), files=[".claude/agents/pr-fixer.md"]), good_review()),
    "merge conflict": (with_(good_state(), mergeable=False), good_review()),
    "mergeability not computed yet": (with_(good_state(), mergeable=None), good_review()),
    "check failed": (with_(good_state(), checks=[
        {"name": "check", "status": "completed", "conclusion": "failure"}]), good_review()),
    "check still running": (with_(good_state(), checks=[
        {"name": "check", "status": "in_progress", "conclusion": None}]), good_review()),
    "check never ran": (with_(good_state(), checks=[
        {"name": "publish", "status": "completed", "conclusion": "skipped"}]), good_review()),
    "check skipped instead of passing": (with_(good_state(), checks=[
        {"name": "check", "status": "completed", "conclusion": "skipped"}]), good_review()),
    "another check timed out": (with_(good_state(), checks=good_state()["checks"] + [
        {"name": "lint", "status": "completed", "conclusion": "timed_out"}]), good_review()),
}


class MergeGateTest(unittest.TestCase):
    def test_clean_pr_passes(self):
        verdict = merge_gate.evaluate(good_state(), good_review())
        self.assertTrue(verdict["pass"], verdict["reasons"])

    def test_medium_and_low_findings_do_not_block(self):
        review = with_(good_review(), findings=[
            {"id": "M1", "severity": "MEDIUM", "file": "a", "line": 1, "finding": "x"},
            {"id": "L1", "severity": "LOW", "file": "a", "line": None, "finding": "y"}])
        self.assertTrue(merge_gate.evaluate(good_state(), review)["pass"])

    def test_every_known_bad_case_fails(self):
        for name, (state, review) in KNOWN_BAD.items():
            with self.subTest(name):
                verdict = merge_gate.evaluate(state, review)
                self.assertFalse(verdict["pass"], f"gate let through: {name}")
                self.assertTrue(verdict["reasons"])

    def test_known_bad_set_is_large_enough_to_trust(self):
        self.assertGreaterEqual(len(KNOWN_BAD), 10)

    def test_draft_passes_but_is_flagged_for_ready(self):
        verdict = merge_gate.evaluate(with_(good_state(), draft=True), good_review())
        self.assertTrue(verdict["pass"])
        self.assertTrue(verdict["draft"])

    def test_reasons_name_every_problem(self):
        state = with_(good_state(), labels=["hold"], mergeable=False)
        review = with_(good_review(), head_sha=OLD)
        reasons = " | ".join(merge_gate.evaluate(state, review)["reasons"])
        for word in ("stale review", "merge conflict", "hold"):
            self.assertIn(word, reasons)

    def test_renamed_protected_file_is_protected(self):
        self.assertTrue(merge_gate.is_protected(".github/workflows/health.yml"))
        self.assertFalse(merge_gate.is_protected("github/notes.md"))


if __name__ == "__main__":
    unittest.main()

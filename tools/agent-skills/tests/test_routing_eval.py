import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skill-runs"))
import routing_eval as evaluation


class RoutingEvalTest(unittest.TestCase):
    def test_default_matrix_pairs_identical_tasks(self):
        jobs = list(evaluation.trial_order(evaluation.CASES, 3))
        self.assertEqual(len(jobs), 24)
        for first, second in zip(jobs[::2], jobs[1::2]):
            self.assertEqual((first[0], first[2]), (second[0], second[2]))
            self.assertEqual({first[1], second[1]}, {"control", "router"})
        self.assertEqual([jobs[i][1] for i in (0, 8, 16)], ["control", "router", "control"])

    def test_grade_inventory_against_the_fixture_and_score_it_separately(self):
        case = evaluation.CASES["mixed-inventory"]
        installed = set(evaluation.BASE_SKILLS)
        answer = {"workflows": ["get-found"], "approval_points": ["get-indexed"], "inventory": [
            {"skill": name, "status": "installed" if name in installed else "missing"}
            for name in case["skills"]
        ]}
        names = evaluation.catalog()["skills"].keys()
        scores = evaluation.score(case, answer, installed, True, "router", names)
        self.assertTrue(all(scores.values()))
        answer["inventory"][0]["status"] = "missing"
        answer["approval_points"] = []
        self.assertEqual(evaluation.score(case, answer, installed, True, "router", names),
                         {"activation": True, "route": True, "inventory": False, "approvals": False})

    def test_near_miss_does_not_require_router_activation(self):
        case = evaluation.CASES["single-skill-near-miss"]
        answer = {"workflows": [], "approval_points": [],
                  "inventory": [{"skill": "wordsmith", "status": "installed"}]}
        names = evaluation.catalog()["skills"].keys()
        self.assertTrue(all(evaluation.score(case, answer, {"wordsmith"}, False, "router", names).values()))
        self.assertFalse(evaluation.score(case, answer, {"wordsmith"}, True, "router", names)["activation"])

    def test_router_activation_comes_from_skill_tool_use(self):
        event = {"type": "assistant", "message": {"content": [{"type": "text", "text": evaluation.ROUTER}]}}
        self.assertFalse(evaluation.router_activated([event]))
        event["message"]["content"].append(
            {"type": "tool_use", "name": "Skill", "id": "router-call", "input": {"skill": evaluation.ROUTER}}
        )
        result = {"type": "tool_result", "tool_use_id": "router-call", "is_error": True}
        events = [event, {"type": "user", "message": {"content": [result]}}]
        self.assertFalse(evaluation.router_activated(events))
        result["is_error"] = False
        self.assertTrue(evaluation.router_activated(events))

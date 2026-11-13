"""Runs the JavaScript self-checks for the free tools' cores when Node is available."""
import shutil
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class ToolCoresTest(unittest.TestCase):
    def run_node(self, name):
        run = subprocess.run(["node", str(HERE / name)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_prose(self):
        self.run_node("prose_cases.mjs")

    def test_map_resume_list(self):
        self.run_node("tools_cases.mjs")


if __name__ == "__main__":
    unittest.main()

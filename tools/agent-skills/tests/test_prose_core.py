"""Runs the JavaScript self-check for /prose/prose-core.js when Node is available."""
import shutil
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class ProseCoreTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_cases(self):
        run = subprocess.run(["node", str(HERE / "prose_cases.mjs")], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()

import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import indexnow

KEY = "0123456789abcdef0123456789abcdef"


class IndexNowTest(unittest.TestCase):
    def test_changed_files_map_to_page_urls(self):
        changed = ["public/index.html", "public/index.md", "public/alpha/index.html",
                   "public/alpha/index.md", "public/fonts/fonts.css", "public/version.json",
                   "functions/_middleware.js", "README.md"]
        self.assertEqual(indexnow.page_urls(changed),
                         ["https://skills.caffeinity.com/", "https://skills.caffeinity.com/alpha/"])

    def test_payload(self):
        body = indexnow.payload(KEY, ["https://skills.caffeinity.com/"])
        self.assertEqual(body["host"], "skills.caffeinity.com")
        self.assertEqual(body["keyLocation"], f"https://skills.caffeinity.com/{KEY}.txt")

    def test_key_file_must_hold_its_own_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(SystemExit):
                indexnow.key_file(root)
            (root / f"{KEY}.txt").write_text(KEY + "\n")
            self.assertEqual(indexnow.key_file(root).name, f"{KEY}.txt")
            (root / f"{KEY}.txt").write_text("other")
            with self.assertRaises(SystemExit):
                indexnow.key_file(root)

    def test_repo_has_exactly_one_key(self):
        indexnow.key_file(Path(__file__).resolve().parents[3])

    def test_rejection_is_reported_not_raised(self):
        def refuse(request, timeout):
            raise urllib.error.HTTPError(request.full_url, 403, "Forbidden", {},
                                         io.BytesIO(b"key not valid"))
        status, detail = indexnow.submit({"urlList": []}, opener=refuse)
        self.assertEqual((status, detail), (403, "key not valid"))

    def test_request_shape(self):
        seen = {}

        class Ok:
            status = 202
            def __enter__(self): return self
            def __exit__(self, *a): return False

        def accept(request, timeout):
            seen["url"], seen["body"] = request.full_url, json.loads(request.data)
            return Ok()
        self.assertEqual(indexnow.submit({"urlList": ["x"]}, opener=accept), (202, ""))
        self.assertEqual(seen["url"], indexnow.ENDPOINT)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gen_sitemap

MANIFEST = {
    "skills": [
        {"name": "alpha", "page": "bespoke", "order": 2},
        {"name": "beta", "page": "none", "order": 3},
        {"name": "gamma", "page": "generated", "order": 1},
    ]
}


class SitemapTest(unittest.TestCase):
    def test_url_set_and_order(self):
        self.assertEqual([u for u, _ in gen_sitemap.urls(MANIFEST)],
                         ["https://skills.caffeinity.com/",
                          "https://skills.caffeinity.com/gamma/",
                          "https://skills.caffeinity.com/alpha/"])

    def test_xml_parses(self):
        xml = gen_sitemap.render(MANIFEST, lambda path: "2026-10-21")
        root = ET.fromstring(xml)
        locs = [el.text for el in root.iter(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(locs), 3)


if __name__ == "__main__":
    unittest.main()

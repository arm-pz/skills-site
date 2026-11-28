import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skilllib

ROOT = Path(__file__).resolve().parents[3]
# The brand is always "Skillsmith by Caffeinity": other projects use the bare name (an MCP Market
# skill drafter, an npm package, a skill hub). The one allowed bare mention names that other registry.
BARE = re.compile(r"\bSkillsmith\b(?! by Caffeinity)(?! by <a href=\"https://caffeinity\.com/\">)(?! registry)")


QUOTED = re.compile(r"<details>.*?</details>", re.S)


def own_words(path):
    """The page's text minus what it quotes. A run page's <details> blocks are the agent's
    commands and answer verbatim; evidence is never rewritten to fit house style."""
    text = path.read_text(encoding="utf-8")
    return QUOTED.sub("", text) if path.relative_to(ROOT).parts[0] == "runs" else text


class BrandTest(unittest.TestCase):
    def test_pages_and_templates_qualify_the_brand(self):
        files = list(ROOT.glob("*/index.html")) + list(ROOT.glob("*/*/index.html")) + [ROOT / "index.html"]
        files += list((ROOT / "tools" / "agent-skills" / "templates").glob("*.html"))
        bad = [f"{f.relative_to(ROOT)}: {m.group(0)}…" for f in files if f.is_file()
               for m in BARE.finditer(own_words(f))
               if "dist" not in f.parts and "out" not in f.parts]
        self.assertEqual(bad, [], "write 'Skillsmith by Caffeinity'")

    def test_llms_txt_qualifies_the_brand(self):
        import json
        manifest = json.loads((ROOT / "site" / "skills.json").read_text(encoding="utf-8"))
        self.assertFalse(BARE.search(skilllib.llms_txt(manifest)))
        self.assertFalse(BARE.search(skilllib.llms_full_txt(manifest)))


if __name__ == "__main__":
    unittest.main()

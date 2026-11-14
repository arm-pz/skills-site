#!/usr/bin/env python3
"""Self-check for slop_scan.py. Run: python -I scripts/test_slop_scan.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from slop_scan import scan  # noqa: E402


def rules(text, **kw):
    return {rule for _, rule, _ in scan(text, **kw)}


CASES = [
    # (label, text, rules that must appear, rules that must not appear)
    ("em dash", "It works — mostly.", {"em-dash"}, set()),
    ("hyphen and en dash in a range are fine", "A well-known fix, pages 3–5.", set(), {"em-dash"}),
    ("vocabulary with inflection", "We delved into the tapestry.", {"vocabulary"}, set()),
    ("'key' alone is not flagged", "Press the key and turn the key.", set(), {"vocabulary"}),
    ("promotional", "A renowned, world-class venue.", {"promotional"}, set()),
    ("significance", "This marks a turning point for the town.", {"significance"}, set()),
    ("vague attribution", "Experts say the plan failed.", {"vague-attribution"}, set()),
    ("chatbot phrase", "Great question! I hope this helps.", {"chatbot-phrase"}, set()),
    ("not only but", "It is not only fast but cheap.", {"negative-parallelism"}, set()),
    ("it's not X, it's Y", "It's not a bug, it's a feature.", {"negative-parallelism"}, set()),
    ("isn't X. It's Y.", "This isn't a tool. It's a platform.", {"negative-parallelism"}, set()),
    ("not just X, it's Y", "It's not just a museum, it's a workshop.", {"negative-parallelism"}, set()),
    ("plain negation is fine", "The server is not running.", set(), {"negative-parallelism"}),
    ("ing tail", "Sales rose 4%, highlighting strong demand.", {"ing-tail"}, set()),
    ("canned opener", "In conclusion, it rained.", {"canned-opener"}, set()),
    ("'overall' mid-sentence is fine", "The overall cost fell.", set(), {"canned-opener"}),
    ("placeholder", "Regards, [Your Name]", {"placeholder"}, set()),
    ("a Markdown link is not a placeholder", "See [the docs](https://example.com).", set(), {"placeholder"}),
    ("tool markup", "Rain fell :contentReference[oaicite:2]", {"tool-markup"}, set()),
    ("tracking parameter", "https://example.com/a?utm_source=x", {"tool-markup"}, set()),
    ("title-case heading", "## Challenges And Future Outlook", {"title-case-heading"}, set()),
    ("sentence-case heading", "## Challenges and future outlook", set(), {"title-case-heading"}),
    ("acronyms do not make title case", "## Using the API with JSON", set(), {"title-case-heading"}),
    ("emoji heading", "## \U0001F680 Launch", {"emoji-decoration"}, set()),
    ("horizontal rule", "one\n\n---\n\ntwo", {"horizontal-rule"}, set()),
    ("frontmatter is skipped", "---\nname: delve\n---\nbody", set(), {"vocabulary", "horizontal-rule"}),
    ("fenced code is skipped", "```\ndelve —\n```", set(), {"vocabulary", "em-dash"}),
    ("inline code is skipped", "Use `delve` here.", set(), {"vocabulary"}),
    ("three bold-label bullets", "- **Fast:** a\n- **Cheap:** b\n- **Good:** c", {"bold-label-list"}, set()),
    ("one bold-label bullet is fine", "- **Note:** a\n- plain", set(), {"bold-label-list"}),
    ("curly quotes off by default", "“Hi”", set(), {"curly-quote"}),
]


def main():
    failed = 0
    for label, text, want, forbid in CASES:
        got = rules(text)
        if not want <= got or got & forbid:
            failed += 1
            print(f"FAIL  {label}: got {sorted(got)}, want {sorted(want)}, forbid {sorted(forbid)}")
    if "curly-quote" not in rules("“Hi”", plain_text=True):
        failed += 1
        print("FAIL  curly quotes with --plain-text")
    hits = scan("a\nb — c")
    if not hits or hits[0][0] != 2:
        failed += 1
        print(f"FAIL  line number: {hits}")
    total = len(CASES) + 2
    print(f"{total - failed} of {total} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

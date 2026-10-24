"""Tell IndexNow (Bing, Yandex, Seznam, Naver and the engines that share it) which pages changed.

The key is public by design: IndexNow checks that https://<host>/<key>.txt holds it, so the key
file lives at the repo root and make_dist.sh copies it into dist/. The publish workflow calls this
after the live site matches the build, with the files that deploy changed:

  python tools/agent-skills/indexnow.py --changed changed.txt    # one dist-relative path per line
  python tools/agent-skills/indexnow.py --key-file               # print the key file's name

A failed ping is reported and never fails the run: the sitemap still carries every page.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import skilllib

ENDPOINT = "https://api.indexnow.org/indexnow"
KEY_RE = re.compile(r"^[0-9a-f]{32}\.txt$")


def key_file(root):
    found = sorted(p for p in Path(root).iterdir() if KEY_RE.match(p.name))
    if len(found) != 1:
        raise SystemExit(f"expected one IndexNow key file at the repo root, found {len(found)}")
    key = found[0].read_text(encoding="utf-8").strip()
    if key != found[0].stem:
        raise SystemExit(f"{found[0].name} must contain exactly its own name, {found[0].stem}")
    return found[0]


def page_urls(paths):
    """Page URLs for the changed files: a page or its Markdown twin, nothing else."""
    urls = []
    for raw in paths:
        path = raw.strip().removeprefix("public/")
        match = re.fullmatch(r"(?:([a-z0-9-]+)/)?index\.(?:html|md)", path)
        if not match:
            continue
        url = f"{skilllib.SITE}/{match.group(1)}/" if match.group(1) else f"{skilllib.SITE}/"
        if url not in urls:
            urls.append(url)
    return urls


def payload(key, urls):
    host = skilllib.SITE.split("://", 1)[1]
    return {"host": host, "key": key, "keyLocation": f"{skilllib.SITE}/{key}.txt",
            "urlList": urls}


def submit(body, opener=urllib.request.urlopen):
    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with opener(request, timeout=30) as response:
            return response.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")[:300]
    except (urllib.error.URLError, TimeoutError) as exc:
        return None, str(exc)


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--changed", help="file listing changed dist-relative paths")
    mode.add_argument("--key-file", action="store_true")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    path = key_file(args.root)
    if args.key_file:
        print(path.name)
        return 0
    urls = page_urls(Path(args.changed).read_text(encoding="utf-8").splitlines())
    if not urls:
        print("indexnow: no page changed; nothing to submit")
        return 0
    status, detail = submit(payload(path.stem, urls))
    # 200 and 202 both mean accepted; 202 is the usual answer while the key is first checked.
    verdict = "accepted" if status in (200, 202) else "not accepted"
    print(f"indexnow: {len(urls)} URL(s) {verdict} (HTTP {status}) {detail}".rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())

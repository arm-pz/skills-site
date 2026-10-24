// node --test tools/agent-skills/tests/test_middleware.mjs
import assert from "node:assert/strict";
import { test } from "node:test";
import { onRequest, prefersMarkdown, quality } from "../../../functions/_middleware.js";

const files = {
  "/wordsmith/index.html": ["<h1>Wordsmith</h1>", "text/html"],
  "/wordsmith/index.md": ["# Wordsmith\n", "application/octet-stream"],
};

function serve(path) {
  const key = path.endsWith("/") ? `${path}index.html` : path;
  const file = files[key];
  return file
    ? new Response(file[0], { headers: { "Content-Type": file[1] } })
    : new Response("not found", { status: 404 });
}

function call(path, accept, method = "GET") {
  const request = new Request(`https://skills.caffeinity.com${path}`, {
    method,
    headers: accept ? { Accept: accept } : {},
  });
  return onRequest({
    request,
    next: async () => serve(new URL(request.url).pathname),
    env: { ASSETS: { fetch: async (url) => serve(new URL(url).pathname) } },
  });
}

const BROWSER = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8";

test("Accept parsing", () => {
  assert.equal(quality(BROWSER, "text/html"), 1);
  assert.equal(quality(BROWSER, "text/markdown"), 0.8);
  assert.equal(quality("text/*;q=0.5", "text/markdown"), 0.5);
  assert.equal(prefersMarkdown(BROWSER), false);
  assert.equal(prefersMarkdown("*/*"), false);
  assert.equal(prefersMarkdown(""), false);
  assert.equal(prefersMarkdown("text/markdown"), true);
  assert.equal(prefersMarkdown("text/markdown, text/html;q=0.9"), true);
  assert.equal(prefersMarkdown("text/markdown;q=0, text/html"), false);
});

test("browsers get the HTML, marked Vary: Accept", async () => {
  const res = await call("/wordsmith/", BROWSER);
  assert.equal(await res.text(), "<h1>Wordsmith</h1>");
  assert.match(res.headers.get("Vary"), /Accept/);
});

test("agents that prefer Markdown get the twin with a canonical link", async () => {
  const res = await call("/wordsmith/", "text/markdown, text/html;q=0.5");
  assert.equal(await res.text(), "# Wordsmith\n");
  assert.equal(res.headers.get("Content-Type"), "text/markdown; charset=utf-8");
  assert.equal(res.headers.get("Link"), '<https://skills.caffeinity.com/wordsmith/>; rel="canonical"');
  assert.match(res.headers.get("Vary"), /Accept/);
});

test("the twin's own URL is typed and canonicalised too", async () => {
  const res = await call("/wordsmith/index.md");
  assert.equal(res.headers.get("Content-Type"), "text/markdown; charset=utf-8");
  assert.equal(res.headers.get("Link"), '<https://skills.caffeinity.com/wordsmith/>; rel="canonical"');
});

test("a page without a twin falls back to the HTML answer", async () => {
  const res = await call("/missing/", "text/markdown");
  assert.equal(res.status, 404);
});

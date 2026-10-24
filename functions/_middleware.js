// Content negotiation for agents. Every page at /<name>/ has a Markdown twin at /<name>/index.md
// (written by tools/agent-skills/twins.py). A request whose Accept header prefers text/markdown
// over text/html gets the twin at the page's own URL; browsers keep the HTML. Both answers carry
// Vary: Accept so a cache never hands one to the other, and every Markdown answer names the HTML
// page as canonical so search engines do not count the two as duplicates.
// _routes.json keeps fonts, archives and indexes from running this at all.

const SITE = "https://skills.caffeinity.com";
const MARKDOWN = "text/markdown; charset=utf-8";

// The q-value the Accept header gives a media type: its own entry, else type/*, else */*.
export function quality(accept, type) {
  const [major] = type.split("/");
  let best = { rank: -1, q: 0 };
  for (const part of (accept || "").split(",")) {
    const [range, ...params] = part.trim().toLowerCase().split(";");
    const rank = range === type ? 2 : range === `${major}/*` ? 1 : range === "*/*" ? 0 : -1;
    if (rank < best.rank || rank < 0) continue;
    const q = params.map((p) => p.trim()).find((p) => p.startsWith("q="));
    best = { rank, q: q ? Number.parseFloat(q.slice(2)) || 0 : 1 };
  }
  return best.q;
}

export function prefersMarkdown(accept) {
  const md = quality(accept, "text/markdown");
  return md > 0 && md > quality(accept, "text/html");
}

function canonicalFor(pathname) {
  return SITE + pathname.replace(/index\.md$/, "");
}

function markdown(response, pathname) {
  const headers = new Headers(response.headers);
  headers.set("Content-Type", MARKDOWN);
  headers.set("Link", `<${canonicalFor(pathname)}>; rel="canonical"`);
  headers.append("Vary", "Accept");
  return new Response(response.body, { status: response.status, headers });
}

export async function onRequest({ request, next, env }) {
  const url = new URL(request.url);
  const { pathname } = url;
  const read = request.method === "GET" || request.method === "HEAD";

  if (read && pathname.endsWith("/") && prefersMarkdown(request.headers.get("Accept"))) {
    const twin = await env.ASSETS.fetch(new URL(`${pathname}index.md`, url));
    if (twin.ok) return markdown(twin, `${pathname}index.md`);
  }

  const response = await next();
  if (read && pathname.endsWith("/index.md") && response.ok) return markdown(response, pathname);
  if (!read || !pathname.endsWith("/")) return response;
  const varied = new Response(response.body, response);
  varied.headers.append("Vary", "Accept");
  return varied;
}

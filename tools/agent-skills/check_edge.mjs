// Check what the edge actually serves, which no build gate can see.
//
// check_dist.py and verify.mjs prove dist/ matches the manifest. Cloudflare can still change
// the response after that: Email Address Obfuscation rewrites mailto: links into
// /cdn-cgi/l/email-protection, and a Redirect Rule can be 302 when PROJECT.md says 301.
// Both happened on skillsmith.tech with every gate green. This reads the live site.
//
//   node tools/agent-skills/check_edge.mjs                          # https://skillsmith.tech
//   node tools/agent-skills/check_edge.mjs https://skillsmith.tech
//
// Exit 0 = clean, 1 = an edge problem, 2 = could not run (network).

const site = (process.argv[2] ?? "https://skillsmith.tech").replace(/\/$/, "");
// Hostnames that must send visitors to `site` with the path kept, permanently.
const LEGACY = process.env.EDGE_LEGACY?.split(",") ?? ["https://skills.caffeinity.com", "https://www.skillsmith.tech"];
const PROBE = "/skills/";
const bust = process.env.CACHE_BUST ? `?v=${encodeURIComponent(process.env.CACHE_BUST)}` : "";

const problems = [];
const fail = (msg) => problems.push(msg);

async function text(url) {
  const res = await fetch(url + bust, { redirect: "follow" });
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  return res.text();
}

let locs;
try {
  const xml = await text(`${site}/sitemap.xml`);
  locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
} catch (err) {
  console.error(`cannot read the sitemap: ${err.message}`);
  process.exit(2);
}

// 1. No page may carry Cloudflare's obfuscated email links. Wrap addresses in
//    <!--email_off-->…<!--/email_off--> or turn Scrape Shield > Email Address Obfuscation off.
const pages = [...new Set(locs)];
const queue = [...pages];
await Promise.all(Array.from({ length: 6 }, async () => {
  for (let url; (url = queue.shift()); ) {
    try {
      const html = await text(url);
      const n = (html.match(/\/cdn-cgi\/l\/email-protection/g) ?? []).length;
      if (n) fail(`${new URL(url).pathname}: ${n} link(s) rewritten by Cloudflare email obfuscation`);
    } catch (err) {
      fail(err.message);
    }
  }
}));

// 2. Retired and alternate hosts must answer 301 to the same path on the canonical host.
for (const host of LEGACY) {
  try {
    const res = await fetch(host + PROBE, { redirect: "manual" });
    const to = res.headers.get("location");
    if (res.status !== 301) fail(`${host}${PROBE}: HTTP ${res.status}, expected 301 (search engines do not move ranking on ${res.status})`);
    if (to !== `${site}${PROBE}`) fail(`${host}${PROBE}: redirects to ${to}, expected ${site}${PROBE}`);
  } catch (err) {
    fail(`${host}: ${err.message}`);
  }
}

// 3. llms.txt and the homepage must state the same catalogue size.
try {
  const headline = (s) => (s.match(/(\d+)\s+skills?\s+and\s+(\d+)\s+mods?/i) ?? []).slice(1, 3).join("/");
  const llms = headline(await text(`${site}/llms.txt`));
  const home = headline((await text(`${site}/`)).replace(/<[^>]+>/g, " ").replace(/\s+/g, " "));
  if (!llms || llms !== home) fail(`llms.txt says ${llms || "no 'N skills and M mods'"}, homepage says ${home || "nothing"}`);
} catch (err) {
  fail(err.message);
}

console.log(`${pages.length} pages and ${LEGACY.length} legacy hosts checked on ${site}`);
for (const p of problems) console.log(`FAIL ${p}`);
console.log(problems.length ? `${problems.length} edge problem(s)` : "edge: OK");
process.exit(problems.length ? 1 : 0);

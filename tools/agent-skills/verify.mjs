// Verify a discovery index the way the `npx skills` client does:
// parse index.json, fetch each artifact, recompute its digest, unpack it and
// require a root SKILL.md with name + description frontmatter.
//
//   node verify.mjs local                     # check ./out
//   node verify.mjs https://skillsmith.tech   # check a deployed host

import { createHash } from "node:crypto";
import { gunzipSync } from "node:zlib";
import { join } from "node:path";
import { readFile } from "node:fs/promises";

const SCHEMA = "https://schemas.agentskills.io/discovery/0.2.0/schema.json";
const mode = process.argv[2] ?? "local";
const base = mode === "local" ? null : mode.replace(/\/$/, "");
const indexUrl = base ? `${base}/.well-known/agent-skills/index.json` : "out/index.json";

const bust = process.env.CACHE_BUST
  ? `?v=${encodeURIComponent(process.env.CACHE_BUST)}`
  : "";
const withBust = (url) =>
  bust ? `${url}${url.includes("?") ? "&" : "?"}${bust.slice(1)}` : url;

const get = async (url) => {
  if (base) return new Uint8Array(await (await fetch(withBust(url))).arrayBuffer());
  const path = url.startsWith("http")
    ? join("out", new URL(url).pathname.split("/").pop())
    : url;
  return await readFile(join(process.cwd(), path));
};

const untar = (bytes) => {
  const tar = gunzipSync(Buffer.from(bytes));
  const files = new Map();
  let offset = 0;
  while (offset + 512 <= tar.length) {
    const header = tar.subarray(offset, offset + 512);
    if (header.every((b) => b === 0)) break;
    const str = (o, l) => {
      const s = header.subarray(o, o + l);
      const nul = s.indexOf(0);
      return new TextDecoder().decode(nul >= 0 ? s.subarray(0, nul) : s);
    };
    const name = str(0, 100);
    const prefix = str(345, 155);
    const size = Number.parseInt(str(124, 12).trim() || "0", 8);
    const typeFlag = header[156];
    offset += 512;
    if (typeFlag === 0x31 || typeFlag === 0x32) throw new Error("archive contains links");
    if (typeFlag === 0 || typeFlag === 0x30) {
      files.set(prefix ? `${prefix}/${name}` : name, tar.subarray(offset, offset + size));
    }
    offset += Math.ceil(size / 512) * 512;
  }
  return files;
};

const frontmatter = (text) => {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!m) return {};
  const fields = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (kv) fields[kv[1]] = kv[2];
  }
  return fields;
};

const index = JSON.parse(new TextDecoder().decode(await get(indexUrl)));
const problems = [];
if (index.$schema !== SCHEMA) problems.push(`$schema is ${index.$schema}`);
if (!Array.isArray(index.skills) || index.skills.length === 0) problems.push("no skills[]");

for (const entry of index.skills) {
  const fails = [];
  if (!/^[a-z0-9-]{1,64}$/.test(entry.name) || /^-|-$|--/.test(entry.name)) fails.push("bad name");
  if (typeof entry.description !== "string" || !entry.description || entry.description.length > 1024)
    fails.push("bad description");
  if (entry.type !== "skill-md" && entry.type !== "archive") fails.push("bad type");
  if (!/^sha256:[a-f0-9]{64}$/.test(entry.digest ?? "")) fails.push("bad digest format");

  let files = new Map();
  try {
    const bytes = await get(entry.url);
    const actual = `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
    if (actual !== entry.digest) fails.push(`digest mismatch, served ${actual.slice(0, 18)}…`);
    files = untar(bytes);
  } catch (err) {
    fails.push(`fetch/untar: ${err.message}`);
  }

  if (files.size && !files.has("SKILL.md")) fails.push("archive missing root SKILL.md");
  const fm = files.has("SKILL.md") ? frontmatter(new TextDecoder().decode(files.get("SKILL.md"))) : {};
  if (files.has("SKILL.md") && (!fm.name || !fm.description)) fails.push("SKILL.md frontmatter incomplete");

  const status = fails.length ? `FAIL ${fails.join("; ")}` : `ok  ${files.size} files, name=${fm.name}`;
  console.log(`${String(entry.name).padEnd(15)} ${status}`);
  if (fails.length) problems.push(entry.name);
}

console.log(`\n${index.skills?.length ?? 0} entries, ${problems.length} problem(s)`);
if (problems.length) process.exitCode = 1;

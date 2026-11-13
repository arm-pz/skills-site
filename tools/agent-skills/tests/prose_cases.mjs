// Self-check for /prose/prose-core.js: the cases from straight-prose's scripts/test_slop_scan.py,
// plus the positions the page uses to mark a hit. Run: node tools/agent-skills/tests/prose_cases.mjs
import {createRequire} from "node:module";
const require=createRequire(import.meta.url);
const {scan,report}=require("../../../prose/prose-core.js");
const rules=(text,opts)=>new Set(scan(text,opts).map(h=>h.rule));
const CASES=[
  // [label, text, rules that must appear, rules that must not appear]
  ["em dash","It works — mostly.",["em-dash"],[]],
  ["hyphen and en dash in a range are fine","A well-known fix, pages 3–5.",[],["em-dash"]],
  ["vocabulary with inflection","We delved into the tapestry.",["vocabulary"],[]],
  ["'key' alone is not flagged","Press the key and turn the key.",[],["vocabulary"]],
  ["promotional","A renowned, world-class venue.",["promotional"],[]],
  ["significance","This marks a turning point for the town.",["significance"],[]],
  ["vague attribution","Experts say the plan failed.",["vague-attribution"],[]],
  ["chatbot phrase","Great question! I hope this helps.",["chatbot-phrase"],[]],
  ["not only but","It is not only fast but cheap.",["negative-parallelism"],[]],
  ["it's not X, it's Y","It's not a bug, it's a feature.",["negative-parallelism"],[]],
  ["isn't X. It's Y.","This isn't a tool. It's a platform.",["negative-parallelism"],[]],
  ["not just X, it's Y","It's not just a museum, it's a workshop.",["negative-parallelism"],[]],
  ["plain negation is fine","The server is not running.",[],["negative-parallelism"]],
  ["ing tail","Sales rose 4%, highlighting strong demand.",["ing-tail"],[]],
  ["canned opener","In conclusion, it rained.",["canned-opener"],[]],
  ["'overall' mid-sentence is fine","The overall cost fell.",[],["canned-opener"]],
  ["placeholder","Regards, [Your Name]",["placeholder"],[]],
  ["a Markdown link is not a placeholder","See [the docs](https://example.com).",[],["placeholder"]],
  ["tool markup","Rain fell :contentReference[oaicite:2]",["tool-markup"],[]],
  ["tracking parameter","https://example.com/a?utm_source=x",["tool-markup"],[]],
  ["title-case heading","## Challenges And Future Outlook",["title-case-heading"],[]],
  ["sentence-case heading","## Challenges and future outlook",[],["title-case-heading"]],
  ["acronyms do not make title case","## Using the API with JSON",[],["title-case-heading"]],
  ["emoji heading","## \u{1F680} Launch",["emoji-decoration"],[]],
  ["horizontal rule","one\n\n---\n\ntwo",["horizontal-rule"],[]],
  ["frontmatter is skipped","---\nname: delve\n---\nbody",[],["vocabulary","horizontal-rule"]],
  ["fenced code is skipped","```\ndelve —\n```",[],["vocabulary","em-dash"]],
  ["inline code is skipped","Use `delve` here.",[],["vocabulary"]],
  ["three bold-label bullets","- **Fast:** a\n- **Cheap:** b\n- **Good:** c",["bold-label-list"],[]],
  ["one bold-label bullet is fine","- **Note:** a\n- plain",[],["bold-label-list"]],
  ["curly quotes off by default","“Hi”",[],["curly-quote"]],
];
let failed=0,total=CASES.length;
const fail=msg=>{failed++;console.log("FAIL  "+msg);};
for(const [label,text,want,forbid] of CASES){
  const got=rules(text);
  if(!want.every(r=>got.has(r))||forbid.some(r=>got.has(r)))fail(`${label}: got ${[...got].sort()}, want ${want}, forbid ${forbid}`);
}
total++;if(!rules("“Hi”",{plainText:true}).has("curly-quote"))fail("curly quotes with plainText");
total++;{const h=scan("a\nb — c");if(!h.length||h[0].line!==2)fail("line number: "+JSON.stringify(h));}
// Every hit with a position must point at its own text in the original line, inline code and
// leading spaces included, or the page would mark the wrong words.
total++;{
  const src="  Overall, use `x — y` to delve — carefully, not only `a` but b.\n## Big Plans For The Team\n- \u{1F680} go";
  const lines=src.split("\n");
  for(const h of scan(src)){
    if(h.col<0)continue;
    const got=lines[h.line-1].slice(h.col,h.col+h.len);
    if(got.replace(/`[^`\n]*`/g,"")!==h.text){fail(`position of ${h.rule}: marked ${JSON.stringify(got)}, hit ${JSON.stringify(h.text)}`);break;}
  }
}
total++;if(!/^    1  em-dash {15}—\n\n1 hits: em-dash 1\nNot checked:/.test(report(scan("a — b"))))fail("report format: "+JSON.stringify(report(scan("a — b"))));
console.log(`${total-failed} of ${total} passed`);
process.exit(failed?1:0);

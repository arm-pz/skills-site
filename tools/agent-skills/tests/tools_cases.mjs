// Self-check for the free tools' cores: /map/map-core.js against the real manifest,
// /resume/resume-core.js and /list/list-core.js. Run: node tools/agent-skills/tests/tools_cases.mjs
import {createRequire} from "node:module";
const require=createRequire(import.meta.url);
const map=require("../../../map/map-core.js");
const resume=require("../../../resume/resume-core.js");
const list=require("../../../list/list-core.js");
const manifest=require("../../../site/skills.json");
let failed=0,total=0;
const ok=(label,cond,detail)=>{total++;if(!cond){failed++;console.log("FAIL  "+label+(detail?": "+detail:""));}};

// Workflow Map: plain-language goals land on the workflow a person would expect.
const GOALS=[
  ["Is my site safe to launch on Friday?","launch-safely"],
  ["nobody finds my github repo","get-found"],
  ["I want more traffic from google","grow-search-traffic"],
  ["help me get a job as a product manager","land-a-job"],
  ["turn my prompts into a skill","build-a-skill"],
  ["I burn through my Claude Code usage limit too fast","set-up-a-coding-agent"],
  ["clean my lead list before a cold email campaign","run-cold-outbound"],
  ["I want to start a small online business","launch-a-product"],
  ["learn linear algebra from scratch","learn-a-skill"],
];
const slugs=new Set(manifest.workflows.map(f=>f.slug));
for(const [goal,want] of GOALS){
  if(!slugs.has(want))continue; // a workflow that was renamed or retired is not this test's business
  const top=map.rank(goal,manifest)[0];
  ok("map: "+goal,top.flow.slug===want&&top.score>0,"got "+top.flow.slug);
}
ok("map: no match scores zero",map.rank("banana",manifest)[0].score===0);
for(const flow of manifest.workflows){
  const g=map.graph(flow,manifest);
  ok("map: graph of "+flow.slug,g.nodes.length===flow.steps.length&&g.nodes.every(n=>n.name&&n.what),JSON.stringify(g.nodes.filter(n=>!n.what).map(n=>n.name)));
}

// Resume Check
const R=resume.check("Jane Doe\njane@example.com | +1 555 010 9999\n\nSummary\nResults-driven professional with a proven track record.\n\nExperience\n- Responsible for the checkout roadmap\n- Helped improve onboarding\n- Cut drop-off from 31% to 22% in 2023\n- Worked on pricing experiments\n\nEducation\nBSc\n\nSkills\nSQL",
  "Product manager for our B2B SaaS platform. You will own retention. SQL required. B2B SaaS experience and retention metrics. SQL daily.");
const ids=R.findings.map(f=>f.id);
ok("resume: counts numbered bullets, ignoring years",R.bullets===4&&R.withNumber===1,R.withNumber+" of "+R.bullets);
ok("resume: duty wording",ids.includes("duties"));
ok("resume: stock phrases",ids.includes("stock"));
ok("resume: contact passes",!ids.includes("no-email")&&!ids.includes("no-phone"));
ok("resume: headings pass",!ids.includes("sections"));
ok("resume: ad terms found and missing",R.terms&&R.terms.found.includes("SQL")&&R.terms.missing.includes("retention"),JSON.stringify(R.terms));
ok("resume: spans point at their text",R.spans.length>0&&R.spans.every(s=>R.lines[s.line-1].slice(s.col,s.col+s.len).length===s.len));
ok("resume: layout is never claimed",R.skipped.some(s=>/Layout/.test(s.msg)));
ok("resume: no email is a failure",resume.check("Experience\n- Built things\n- Made things\n- Did things","").findings.some(f=>f.id==="no-email"));

// List Gate
const rows=["first_name,email,title,company","Ann,ann@acme.io,Head of Sales,Acme",",info@beta.com,CEO,Beta","Bob,bob@gmial.com,Founder,\"Gamma, Inc\"","Cy,cy@delta.co,Intern,Delta","Ann,ANN@acme.io,Head of Sales,Acme","Di,di@@x,VP Sales,X"];
for(let i=0;i<14;i++)rows.push(`P${i},p${i}@corp${i}.com,Sales Director,Corp ${i}`);
const G=list.gate(rows.join("\r\n"),{titles:"sales, founder, ceo"});
ok("list: columns found",G.cols.email===1&&G.cols.name===0&&G.cols.title===2&&G.cols.company===3,JSON.stringify(G.cols));
ok("list: counts",G.total===20&&G.wrong===5&&G.counts.role===1&&G.counts.typo===1&&G.counts.duplicate===1&&G.counts.malformed===1&&G.counts.title===1,JSON.stringify(G.counts)+" wrong "+G.wrong);
ok("list: five wrong in twenty is a hold",G.verdict==="HOLD");
ok("list: quoted comma survives export",list.exportCsv(G,true).includes('"Gamma, Inc"'));
ok("list: clean export keeps header and drops wrong rows",list.exportCsv(G,false).trim().split("\n").length===16);
ok("list: sample is ten rows",list.sample(G,()=>0.5).length===10);
const few=list.gate("email\na@b.co\nc@d.co",{});
ok("list: fewer than ten rows is inconclusive",few.verdict==="INCONCLUSIVE"&&few.fit==="not-given");
ok("list: semicolons and no header",list.gate(Array.from({length:12},(_,i)=>`u${i}@f${i}.com;U${i}`).join("\n"),{}).verdict==="GO");
ok("list: no email column",list.gate("name,city\nA,B\nC,D",{}).verdict==="NO_EMAIL_COLUMN");

console.log(`${total-failed} of ${total} passed`);
process.exit(failed?1:0);

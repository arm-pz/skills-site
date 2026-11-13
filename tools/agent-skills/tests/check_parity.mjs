// Parity check: /check/check-core.js must print exactly what tune-skill's check_skill.py prints
// (its no-PyYAML path) for every skill folder under the given roots.
//   node tools/agent-skills/tests/check_parity.mjs <check_skill.py> <root> [more roots]
import {createRequire} from "node:module";
import {execFileSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
const require=createRequire(import.meta.url);
const {check,report}=require("../../../check/check-core.js");
const [script,...roots]=process.argv.slice(2);
if(!script||!roots.length){console.error("usage: check_parity.mjs <check_skill.py> <root>...");process.exit(2);}
const PY=`import sys,runpy
sys.modules['yaml']=None
sys.argv=['check_skill.py',sys.argv[2]]
try:
    runpy.run_path(SCRIPT,run_name='__main__')
except SystemExit:
    pass
`.replace("SCRIPT",JSON.stringify(path.resolve(script)));
function walk(dir,out){
  for(const e of fs.readdirSync(dir,{withFileTypes:true})){
    if(e.name===".git"||e.name==="node_modules")continue;
    const p=path.join(dir,e.name);
    if(e.isDirectory())walk(p,out);else if(e.name==="SKILL.md")out.push(dir);
  }
  return out;
}
let n=0,bad=0;
for(const root of roots)for(const folder of walk(path.resolve(root),[])){
  n++;
  const py=execFileSync("python3",["-I","-c",PY,"x",folder],{encoding:"utf8"})
    .split("\n").filter(l=>!l.includes("PyYAML not installed")).join("\n").trim();
  const js=report(check(fs.readFileSync(path.join(folder,"SKILL.md"),"utf8"),
    {folder:path.basename(folder),exists:ref=>fs.existsSync(path.join(folder,ref))})).trim();
  // Python counts its own "PyYAML not installed" warning; take one off its total to compare.
  const norm=py.replace(/(\d+) fail, (\d+) warn/,(m,f,w)=>`${f} fail, ${Math.max(0,w-1)} warn`)
    .replace(/^FAIL {2}no SKILL\.md.*$/m,"");
  const tidy=t=>t.split("\n").filter(l=>l.trim()&&!l.startsWith("OK ")).join("\n");
  const jsCmp=tidy(js), pyCmp=tidy(norm);
  if(jsCmp!==pyCmp){bad++;console.log("MISMATCH "+folder+"\n--- python\n"+pyCmp+"\n--- js\n"+jsCmp+"\n");}
}
console.log(`${n} skill folders compared, ${bad} mismatched`);
process.exit(bad?1:0);

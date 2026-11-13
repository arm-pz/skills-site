// Parity check: /prose/prose-core.js must print exactly what straight-prose's slop_scan.py prints
// for every text file under the given roots (.md, .txt, .html), with and without --plain-text.
//   node tools/agent-skills/tests/prose_parity.mjs <slop_scan.py> <root> [more roots]
import {createRequire} from "node:module";
import {execFileSync} from "node:child_process";
import fs from "node:fs";
import path from "node:path";
const require=createRequire(import.meta.url);
const {scan,report}=require("../../../prose/prose-core.js");
const [script,...roots]=process.argv.slice(2);
if(!script||!roots.length){console.error("usage: prose_parity.mjs <slop_scan.py> <root>...");process.exit(2);}
function walk(dir,out){
  for(const e of fs.readdirSync(dir,{withFileTypes:true})){
    if(e.name===".git"||e.name==="node_modules"||e.name==="dist"||e.name==="out")continue;
    const p=path.join(dir,e.name);
    if(e.isDirectory())walk(p,out);else if(/\.(md|txt|html)$/i.test(e.name))out.push(p);
  }
  return out;
}
let n=0,bad=0;
for(const root of roots)for(const file of walk(path.resolve(root),[])){
  for(const plain of [false,true]){
    n++;
    const args=["-I","-X","utf8",path.resolve(script),file].concat(plain?["--plain-text"]:[]);
    const py=execFileSync("python3",args,{encoding:"utf8",maxBuffer:1<<28});
    // Python opens the file in text mode, which reads a lone \r as a line break too.
    const text=fs.readFileSync(file,"utf8").replace(/\r\n?/g,"\n");
    const js=report(scan(text,{plainText:plain}))+"\n";
    if(js!==py){
      bad++;
      const a=py.split("\n"),b=js.split("\n");let i=0;while(i<a.length&&a[i]===b[i])i++;
      console.log("MISMATCH "+file+(plain?" --plain-text":"")+"\n  python: "+a[i]+"\n  js:     "+b[i]+"\n");
    }
  }
}
console.log(`${n} scans compared, ${bad} mismatched`);
process.exit(bad?1:0);

/* List Gate page: runs /list/list-core.js on the CSV in the browser. The list is read from the
   file on your own machine and is never uploaded; this file makes no network request. */
(function(){
  var T=window.Tool,L=window.ListGate,$=function(id){return document.getElementById(id);};
  var form=$("form"),file=$("file"),text=$("text"),titles=$("titles"),statusEl=$("status"),result=$("result");
  if(!form||!T||!L)return;
  var el=T.el,urls=[];
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}
  function download(label,name,body,cls){
    var a=el("a","btn "+cls,label),u=URL.createObjectURL(new Blob([body],{type:"text/csv;charset=utf-8"}));
    urls.push(u);a.href=u;a.download=name;return a;
  }

  function render(r,name){
    urls.forEach(function(u){URL.revokeObjectURL(u);});urls=[];
    result.textContent="";
    if(r.verdict==="EMPTY"){say("That file has no rows.",true);result.hidden=true;return;}
    if(r.verdict==="NO_EMAIL_COLUMN"){say("No column in that file holds email addresses. Check that it is a CSV with one contact per row.",true);result.hidden=true;return;}
    var ready=r.total-r.wrong,pct=Math.round(r.share*100);
    var gate=el("div","gate"+(r.verdict==="HOLD"?" hold":"")),left=el("div");
    left.appendChild(el("p","k","VERDICT"+(r.fit==="checked"?"":" · MAILBOXES ONLY")));
    left.appendChild(el("p","v",r.verdict==="HOLD"?"Hold. Do not load this list yet."
      :r.verdict==="INCONCLUSIVE"?"Too few rows to call."
      :r.wrong?"Go, once "+T.plural(r.wrong,"row is","rows are")+" removed.":"Go. Nothing wrong was found."));
    gate.appendChild(left);
    gate.appendChild(el("p","why",r.verdict==="HOLD"
      ?r.wrong.toLocaleString("en")+" of "+r.total.toLocaleString("en")+" rows ("+pct+"%) are wrong, mostly "+r.pattern+". Two wrong in ten is a pattern: fix the filter or the source that built the list, then check a fresh export. Deleting rows hides the cause."
      :r.verdict==="INCONCLUSIVE"?"A gate needs at least ten rows. The "+T.plural(r.total,"row","rows")+" here were all checked and are listed below."
      :r.wrong?ready.toLocaleString("en")+" of "+r.total.toLocaleString("en")+" rows are ready. The rest are named below"+(r.pattern?", mostly "+r.pattern:"")+"."
      :"All "+r.total.toLocaleString("en")+" addresses are well formed, personal and unique."));
    result.appendChild(gate);

    var tiles=el("div","tiles");
    function tile(n,label,body){if(!n)return;var d=el("div");d.appendChild(el("b",null,n.toLocaleString("en")));d.appendChild(el("strong",null,label));d.appendChild(el("span",null,body));tiles.appendChild(d);}
    tile(r.counts.role,"Role addresses","info@, sales@, support@. Shared inboxes mark cold email as spam.");
    tile(r.counts.duplicate,"Duplicates","The same address more than once.");
    tile((r.counts.malformed||0)+(r.counts.empty||0),"Malformed or empty","A missing @, a space, or no address at all.");
    tile(r.counts.typo,"Typo domains","Such as gmial.com or a .con ending. These bounce.");
    tile(r.counts.title,"Outside your target","The title holds none of the words you gave.");
    if(tiles.children.length)result.appendChild(tiles);

    var list=el("ul","findings");
    r.notes.forEach(function(n){list.appendChild(T.finding("NOTE",n));});
    if(r.fit==="not-given")list.appendChild(T.finding("NOT CHECKED","Whether these are the right people",{why:"No target titles were given, so only the addresses were checked. Add the titles you are targeting above, and read the ten rows below as a prospect would: right company, right title, right size."}));
    if(r.fit==="no-title-column")list.appendChild(T.finding("NOT CHECKED","Whether these are the right people",{why:"You gave target titles, but the file has no column named title, role or position to check them against."}));
    list.appendChild(T.finding("NOT CHECKED","Whether each mailbox exists",{why:"That takes a verification service that contacts the mail server. This check finds what is wrong on the page."}));
    list.appendChild(T.finding("NOT CHECKED","Company and size fit",{why:"A script cannot tell whether a company is one you should be writing to. The sample below is for you to read."}));
    result.appendChild(list);

    var sample=L.sample(r);
    result.appendChild(el("p","passed",(r.total<=10?"Every row":"Ten rows picked at random")+", to read as a prospect would."));
    var box=el("div","tablebox"),table=el("table"),thead=el("thead"),hr=el("tr"),tbody=el("tbody");
    ["Row","Email","Title","Company","Finding"].forEach(function(h){var th=el("th",null,h);th.scope="col";hr.appendChild(th);});
    thead.appendChild(hr);table.appendChild(thead);
    sample.forEach(function(row){
      var tr=el("tr");
      tr.appendChild(el("td",null,String(row.n)));tr.appendChild(el("td","m",row.email||"(none)"));
      tr.appendChild(el("td",null,row.title));tr.appendChild(el("td",null,row.company));
      tr.appendChild(el("td",row.problems.length?"bad":null,row.problems.join("; ")||"Nothing found"));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);box.appendChild(table);result.appendChild(box);

    var actions=el("div","result-actions"),base=(name||"list").replace(/\.[^.]+$/,"");
    if(r.wrong){
      if(ready)actions.appendChild(download("Download the "+ready.toLocaleString("en")+" clean rows",base+"-clean.csv",L.exportCsv(r,false),r.verdict==="HOLD"?"btn-quiet":"btn-accent"));
      actions.appendChild(download("Download the "+r.wrong.toLocaleString("en")+" removed rows, with reasons",base+"-removed.csv",L.exportCsv(r,true),"btn-quiet"));
      result.appendChild(actions);
    }
    result.appendChild(T.upsell("A clean list is step one of three.","cold-email-list-gate is the free skill behind this page: your agent reads the sample against your ideal customer and compares data providers. The outbound workflow carries on to sending capacity and the copy.","See the outbound workflow","/workflows/run-cold-outbound/"));
    result.hidden=false;T.reveal(result);
  }

  function run(body,name){
    if(!body.trim()){say("Choose a CSV file, or paste rows below.",true);return;}
    say("");render(L.gate(body,{titles:titles.value}),name);
  }
  var lastName="";
  file.addEventListener("change",function(){
    var f=file.files&&file.files[0];if(!f)return;
    if(f.size>20000000){say("That file is over 20 MB. Split it and check a part at a time.",true);return;}
    lastName=f.name;say("Reading "+f.name+" ...");
    var rd=new FileReader();
    rd.onload=function(){text.value="";text.dataset.file=String(rd.result);run(String(rd.result),f.name);};
    rd.onerror=function(){say("Could not read that file.",true);};
    rd.readAsText(f);
  });
  form.addEventListener("submit",function(e){
    e.preventDefault();
    if(text.value.trim()){delete text.dataset.file;file.value="";run(text.value,"list.csv");}
    else run(text.dataset.file||"",lastName);
  });
  $("sample").addEventListener("click",function(){
    var rows=["first_name,email,title,company","Asha,asha@northwind.example,Head of Sales,Northwind",",info@contoso.example,CEO,Contoso","Ben,ben@gmial.com,Founder,Fabrikam","Chen,chen@adatum.example,Intern,Adatum","Asha,asha@northwind.example,Head of Sales,Northwind","Dev,dev@@tailspin,VP Sales,Tailspin","Eli,sales@wingtip.example,Sales Director,Wingtip"];
    ["Fay","Gus","Hana","Ivo","Jun","Kit","Lea","Mo","Nia","Oz","Pia","Raj","Sol"].forEach(function(n,i){rows.push(n+","+n.toLowerCase()+"@company"+(i+1)+".example,"+(i%3?"Sales Director":"VP Sales")+",Company "+(i+1));});
    delete text.dataset.file;file.value="";text.value=rows.join("\n");titles.value="sales, founder, ceo";
    run(text.value,"example.csv");
  });
})();

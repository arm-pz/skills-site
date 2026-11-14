/* Skill Check page: fetches a public SKILL.md from GitHub (or takes pasted text), runs
   /check/check-core.js on it in the browser and renders the findings. Nothing is sent to us. */
(function(){
  /* Payment links. Leave a value empty and its order buttons open an email instead.
     Paste a hosted checkout URL (for example a Stripe Payment Link) to take payment directly. */
  var PAY={single:"",family:""};

  var EXPLAIN={
    "no-frontmatter":["An agent reads a skill's name and description from the YAML block at the very top of the file. Without that block the skill cannot be listed or triggered.","Start the file with a line of three hyphens, then name: and description:, then another line of three hyphens."],
    "bad-yaml":["A strict YAML loader stops at this line, so an installer may reject the skill or cut the value short.","Wrap the value in double quotes, or write the key followed by >- and put the text on the indented lines below it."],
    "no-name":["The name is how agents and installers refer to the skill. The format requires it.","Add name: with lowercase words joined by hyphens, the same as the folder."],
    "name-shape":["The Agent Skills format allows only lowercase letters, digits and single hyphens in a name. Installers can reject anything else.","Rename it, for example my-skill, and rename the folder to match."],
    "name-long":["The format caps a name at 64 characters.","Shorten the name and rename the folder to match."],
    "name-folder":["The format expects the name to equal the folder that holds SKILL.md. A mismatch usually means one of them was renamed and the other was forgotten.","Make the two the same. If the folder is right, change name: in the frontmatter."],
    "no-desc":["The description is the only text the agent sees before it decides to load a skill. With none, it has no reason to.","Add description: saying what the skill produces, when to use it and what it is not for."],
    "desc-over":["The format caps a description at 1,024 characters. Past that, a skill can fail to load.","Cut it to 950 or fewer. Move setup notes, tool names and install lines into the body."],
    "desc-close":["You are within a few words of the 1,024-character limit, so the next edit may push it over.","Trim to 950 or fewer so there is room to adjust later."],
    "no-trigger":["The agent matches a request against the description. If the description never names the situations, the skill tends to sit unused. This is a judgement call: some skills trigger well without these exact words.","Add a sentence that starts \"Use when\" and lists requests in the user's own words."],
    "no-boundary":["With no boundary, the skill competes with its neighbours for the same requests. If this skill has no neighbours, ignore this.","Add \"Not for ...\" and name the skill that owns the excluded work."],
    "h1-name":["The first heading and the name disagree. That is often a leftover from a rename, and it confuses people reading the repo. If it is on purpose, ignore this.","Make the heading the name written as words, or rename the skill."],
    "body-long":["The whole body is loaded every time the skill triggers. A long one spends context on detail most runs do not need.","Keep the steps in SKILL.md and move tables, examples and edge cases into references/."],
    "missing-ref":["The body sends the agent to a file that is not in the folder, so that step fails at run time.","Add the file, or correct the path in the body."],
    "count-claim":["The body states a count that no list or table in it matches. One of them is out of date, and the agent may trust the wrong one.","Update the number or the list so they agree."],
    "moment":["The body says the skill must run at a set moment. An agent chooses when to load a skill, so a description cannot guarantee that.","If a skipped run would be costly, pair the skill with a hook. skill-to-mod builds one."]
  };
  var SAMPLE="---\nname: PDF_Helper\ndescription: Helps with PDFs.\n---\n\n# PDF toolkit\n\nThis skill has three modes.\n\n- merge\n- split\n\nRead `references/forms.md` first. Always run it before pushing, and again before you deploy.\n";

  var $=function(id){return document.getElementById(id);};
  var form=$("form"),src=$("src"),text=$("text"),statusEl=$("status"),picker=$("picker"),result=$("result");
  if(!form||!window.SkillCheck)return;
  var skipWhy="";

  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}
  function clear(){result.hidden=true;result.textContent="";picker.hidden=true;picker.textContent="";}

  /* owner/repo, a github.com URL (repo, tree, blob) or a raw.githubusercontent.com URL */
  function parseTarget(input){
    var s=input.trim().replace(/^https?:\/\//i,"").replace(/^www\./i,"").replace(/[?#].*$/,"").replace(/\/+$/,"");
    var m=/^raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/([^\/]+)\/(.+)$/i.exec(s);
    if(m)return {owner:m[1],repo:m[2],ref:m[3],path:m[4]};
    s=s.replace(/^github\.com\//i,"");
    m=/^([\w.-]+)\/([\w.-]+?)(?:\.git)?(?:\/(?:tree|blob)\/([^\/]+)(?:\/(.+))?)?$/.exec(s);
    if(!m)return null;
    return {owner:m[1],repo:m[2],ref:m[3]||"",path:m[4]||""};
  }

  function gh(path,raw){
    return fetch("https://api.github.com"+path,{headers:{Accept:raw?"application/vnd.github.raw+json":"application/vnd.github+json"}}).then(function(r){
      if(r.status===403||r.status===429)throw new Error("GitHub's hourly limit for anonymous lookups is used up on this network. Paste the file below instead; that needs no network.");
      if(r.status===404){var nf=new Error("GitHub could not find that. Check the link, and that the repo is public. For a private skill, paste the file below.");nf.notFound=true;throw nf;}
      if(!r.ok)throw new Error("GitHub answered with an error ("+r.status+"). Try again, or paste the file below.");
      return raw?r.text():r.json();
    },function(){throw new Error("Could not reach GitHub from this browser. Paste the file below instead.");});
  }

  /* Two routes that have no hourly limit, so a busy network or a shared office address never
     leaves the page stuck: jsDelivr's public mirror for the file list, raw.githubusercontent.com
     for the file itself. GitHub's API stays first for the list because it is never stale. */
  function plain(url,asText){
    return fetch(url).then(function(r){
      if(!r.ok){var e=new Error("status "+r.status);e.status=r.status;throw e;}
      return asText?r.text():r.json();
    });
  }
  function enc(p){return p.split("/").map(encodeURIComponent).join("/");}
  function listFiles(t){
    var repo=encodeURIComponent(t.owner)+"/"+encodeURIComponent(t.repo);
    return gh("/repos/"+repo+"/git/trees/"+encodeURIComponent(t.ref||"HEAD")+"?recursive=1").catch(function(apiErr){
      if(apiErr.notFound)throw apiErr;
      return plain("https://data.jsdelivr.com/v1/packages/gh/"+repo+"@"+encodeURIComponent(t.ref||"HEAD")+"?structure=flat").then(function(d){
        /* The mirror can lag a push and can leave files out, so a file it does not list is
           unknown, never missing: the "referenced files exist" check is skipped on this route. */
        return {mirror:true,truncated:true,tree:(d.files||[]).map(function(f){return {type:"blob",path:String(f.name).replace(/^\//,"")};})};
      },function(e){
        if(e.status===404)throw new Error("Could not find that repo. Check the link, and that the repo is public. For a private skill, paste the file below.");
        throw apiErr;
      });
    });
  }
  function readFile(t,path){
    var repo=encodeURIComponent(t.owner)+"/"+encodeURIComponent(t.repo);
    return plain("https://raw.githubusercontent.com/"+repo+"/"+encodeURIComponent(t.ref||"HEAD")+"/"+enc(path),true).catch(function(){
      return gh("/repos/"+repo+"/contents/"+enc(path)+(t.ref?"?ref="+encodeURIComponent(t.ref):""),true);
    });
  }

  function fromGitHub(t){
    clear();say("Looking in "+t.owner+"/"+t.repo+" ...");
    return listFiles(t).then(function(tree){
      var files={},skills=[];
      (tree.tree||[]).forEach(function(n){
        if(n.type!=="blob")return;
        files[n.path]=true;
        if(n.path==="SKILL.md"||/\/SKILL\.md$/.test(n.path))skills.push(n.path);
      });
      var want=t.path.replace(/\/+$/,"");
      if(want){
        skills=/(^|\/)SKILL\.md$/.test(want)?skills.filter(function(p){return p===want;})
          :skills.filter(function(p){return p===want+"/SKILL.md"||p.indexOf(want+"/")===0;});
      }
      function run(path,known){
        say("Reading "+path+" ...");picker.hidden=true;
        var dir=path==="SKILL.md"?"":path.slice(0,-"/SKILL.md".length);
        return (known!=null?Promise.resolve(known):readFile(t,path)).then(function(body){
          var opts={folder:dir?dir.split("/").pop():t.repo};
          if(!tree.truncated)opts.exists=function(ref){return !!files[(dir?dir+"/":"")+ref];};
          var label=t.owner+"/"+t.repo+(dir?"/"+dir:"");
          skipWhy=tree.mirror?"GitHub's lookup limit is used up on this network":tree.truncated?"this repo is too large to list in one request":"";
          render(window.SkillCheck.check(body,opts),label,"https://github.com/"+t.owner+"/"+t.repo+(dir?"/tree/"+(t.ref||"HEAD")+"/"+dir:""));
          say("");
        }).catch(function(e){say(e.message,true);});
      }
      if(!skills.length&&tree.mirror){
        /* The mirror listed no skill. Ask for the file itself at the places a skill usually sits. */
        var guesses=want?(/(^|\/)SKILL\.md$/.test(want)?[want]:[want+"/SKILL.md",want+"/skills/"+want.split("/").pop()+"/SKILL.md"]):["SKILL.md",t.repo+"/SKILL.md","skills/"+t.repo+"/SKILL.md"];
        var repoPath=encodeURIComponent(t.owner)+"/"+encodeURIComponent(t.repo)+"/"+encodeURIComponent(t.ref||"HEAD")+"/";
        return guesses.reduce(function(prev,g){
          return prev.catch(function(){return plain("https://raw.githubusercontent.com/"+repoPath+enc(g),true).then(function(body){return run(g,body);});});
        },Promise.reject()).catch(function(){say("No SKILL.md found there. Check the link, or paste the file below.",true);});
      }
      if(!skills.length){say("No SKILL.md found there. Check the link, or paste the file below.",true);return;}
      if(skills.length===1)return run(skills[0]);
      say(skills.length+" skills found. Pick one to check."+(skills.length>300?" Showing the first 300.":""));
      picker.textContent="";
      skills.sort().slice(0,300).forEach(function(p){
        var li=el("li"),b=el("button",null,p==="SKILL.md"?"SKILL.md (repo root)":p.slice(0,-"/SKILL.md".length));
        b.type="button";b.addEventListener("click",function(){run(p);});
        li.appendChild(b);picker.appendChild(li);
      });
      picker.hidden=false;
    }).catch(function(e){say(e.message,true);});
  }

  function render(r,label,link){
    result.textContent="";
    var fails=r.fatal?[r.fatal]:r.fails,warns=r.fatal?[]:r.warns;
    var verdict=r.fatal?"This file will not load as a skill."
      :fails.length?fails.length+(fails.length===1?" thing":" things")+" must be fixed"+(warns.length?", and "+warns.length+" to look at.":".")
      :warns.length?"No failures. "+warns.length+(warns.length===1?" thing":" things")+" to look at."
      :"Nothing found. The file's shape is sound.";
    result.appendChild(el("p","verdict",verdict));

    var facts=el("div","facts");
    function fact(k,v){var s=el("span");s.appendChild(el("b",null,v));s.appendChild(document.createTextNode(" "+k));facts.appendChild(s);}
    if(label)fact("",label);
    if(!r.fatal){fact("of 1,024 description characters",String(r.descChars));fact("body lines (500 is the soft limit)",String(r.bodyLines));}
    result.appendChild(facts);

    var list=el("ul","findings");
    function add(f,lvl){
      var li=el("li","finding "+lvl.toLowerCase());
      li.appendChild(el("span","lvl",lvl));li.appendChild(el("span","msg",f.msg));
      var ex=EXPLAIN[f.id];
      if(ex){
        var why=el("p");why.appendChild(el("b",null,"Why it matters. "));why.appendChild(document.createTextNode(ex[0]));li.appendChild(why);
        var fix=el("p");fix.appendChild(el("b",null,"Fix. "));fix.appendChild(document.createTextNode(ex[1]));li.appendChild(fix);
      }
      list.appendChild(li);
    }
    fails.forEach(function(f){add(f,"FAIL");});
    warns.forEach(function(w){add(w,"WARN");});
    if(!r.fatal&&r.note)add(r.note,"NOTE");
    if(list.children.length)result.appendChild(list);

    if(r.skipped.length)result.appendChild(el("p","skipped",label&&skipWhy
      ?"Not checked, because "+skipWhy+": "+r.skipped.join("; ")+"."+(/limit/.test(skipWhy)?" Try again in an hour to check "+(r.skipped.length===1?"it":"them")+".":"")
      :"Not checked, because pasted text has no folder: "+r.skipped.join("; ")+". Use a GitHub link to check "+(r.skipped.length===1?"it":"them")+"."));

    var actions=el("div","result-actions");
    var copy=el("button","btn btn-quiet","Copy the report");copy.type="button";
    copy.addEventListener("click",function(){
      var body=(label?label+"\n":"")+window.SkillCheck.report(r)+"\n\nChecked with https://skillsmith.tech/check/";
      var done=function(){copy.textContent="Copied";setTimeout(function(){copy.textContent="Copy the report";},1600);};
      if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(body).then(done,function(){window.prompt("Copy the report:",body);});
      else window.prompt("Copy the report:",body);
    });
    actions.appendChild(copy);
    if(link&&location.protocol.indexOf("http")===0){
      var share=el("button","btn btn-quiet","Copy a link to this check");share.type="button";
      share.addEventListener("click",function(){
        var u=location.origin+location.pathname+"?src="+encodeURIComponent(link.replace(/^https:\/\//,""));
        var done=function(){share.textContent="Copied";setTimeout(function(){share.textContent="Copy a link to this check";},1600);};
        if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(done,function(){window.prompt("Copy the link:",u);});
        else window.prompt("Copy the link:",u);
      });
      actions.appendChild(share);
    }
    result.appendChild(actions);

    var up=el("div","upsell"),p=el("p");
    var clean=!r.fatal&&!fails.length&&!warns.length;
    p.appendChild(el("b",null,clean?"A script can only check the shape.":"Want it sent back fixed?"));
    p.appendChild(document.createTextNode(clean
      ?"Whether the description wins the right requests takes a reader. A tune-up is $19 for one skill at the launch price, refunded if we find nothing worth changing."
      :"A tune-up is $19 for one skill at the launch price: a replacement SKILL.md, each finding with its fix, and test requests. Back in two working days, refunded if we find nothing worth changing."));
    up.appendChild(p);
    var a=el("a","btn btn-accent","Order a tune-up");
    a.href=orderHref("single",link||"");
    up.appendChild(a);result.appendChild(up);

    result.hidden=false;
    result.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
  }

  function orderHref(kind,link){
    if(PAY[kind])return PAY[kind];
    var subject=kind==="family"?"Family tune-up ($99)":"Skill tune-up ($19 launch price)";
    return "mailto:hello@skillsmith.tech?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent("Skill repo or SKILL.md link: "+link+"\n\nAnything we should know (what it fails to do, which agent you use): \n");
  }
  [].forEach.call(document.querySelectorAll("[data-order]"),function(a){
    var kind=a.getAttribute("data-order");
    if(PAY[kind])a.href=PAY[kind];
  });
  if(PAY.single&&PAY.family){
    var note=$("order-note");
    if(note)note.firstChild.textContent="Prices in USD, before any local taxes. After you pay, reply to the receipt with your skill link or file; the clock starts then. More than five skills, or private ones? See ";
  }

  form.addEventListener("submit",function(e){
    e.preventDefault();
    if(!src.value.trim()){if(text.value.trim())return checkText();say("Paste a GitHub link, or paste the file below.",true);src.focus();return;}
    var t=parseTarget(src.value);
    if(!t){say("That does not look like a GitHub link. Try owner/repo, or paste the file below.",true);return;}
    fromGitHub(t);
  });
  function checkText(){
    clear();
    if(!text.value.trim()){say("Paste the contents of a SKILL.md first.",true);text.focus();return;}
    say("");render(window.SkillCheck.check(text.value,{}),"","");
  }
  $("go-text").addEventListener("click",checkText);
  $("sample").addEventListener("click",function(){text.value=SAMPLE;src.value="";checkText();});

  var q=/[?&]src=([^&]+)/.exec(location.search);
  if(q){try{src.value=decodeURIComponent(q[1]);var t0=parseTarget(src.value);if(t0)fromGitHub(t0);}catch(e){}}
})();

/* Workflow Map page: reads the site's own workflow list and draws the route that matches what
   you typed. Nothing you type is sent anywhere. */
(function(){
  var T=window.Tool,M=window.WorkflowMap,$=function(id){return document.getElementById(id);};
  var form=$("form"),goal=$("goal"),statusEl=$("status"),result=$("result"),chips=$("chips");
  if(!form||!T||!M)return;
  var el=T.el,manifest=null;
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}
  function load(){
    if(manifest)return Promise.resolve(manifest);
    function get(u){return fetch(u).then(function(r){if(!r.ok)throw new Error(r.status);return r.json();});}
    /* the build copies site/skills.json beside this page; a local checkout serves it from /site/ */
    return get("/map/skills.json").catch(function(){return get("/site/skills.json");}).then(function(d){manifest=d;return d;});
  }
  var ARROW='M5 12h14M13 6l6 6-6 6';
  function arrow(){
    var ns="http://www.w3.org/2000/svg",s=document.createElementNS(ns,"svg"),p=document.createElementNS(ns,"path");
    s.setAttribute("aria-hidden","true");s.setAttribute("width","22");s.setAttribute("height","22");s.setAttribute("viewBox","0 0 24 24");
    s.setAttribute("fill","none");s.setAttribute("stroke","currentColor");s.setAttribute("stroke-width","2");s.setAttribute("stroke-linecap","round");s.setAttribute("stroke-linejoin","round");
    p.setAttribute("d",ARROW);s.appendChild(p);return s;
  }
  function skillLink(name,page,cls){var a=el(page?"a":"span",cls,name);if(page)a.href=page;return a;}

  function draw(d,ranked,pick,typed){
    var hit=ranked[pick],flow=hit.flow,g=M.graph(flow,d);
    result.textContent="";
    var second=ranked.filter(function(r,i){return i!==pick&&r.score>0;})[0];
    var unsure=typed&&(hit.score<4||(second&&hit.score-second.score<2));
    if(typed)result.appendChild(el("p","verdict",unsure?"The closest route we have:":"Here is the route."));

    var box=el("section","route");box.setAttribute("aria-label","The route");
    box.appendChild(el("p","brew","BREW "+flow.number+" · "+String(flow.name).toUpperCase()));
    box.appendChild(el("h3",null,flow.title+"."));
    box.appendChild(el("p","sum",flow.summary));
    var graph=el("div","graph");graph.setAttribute("role","list");
    g.nodes.forEach(function(n,i){
      if(i)graph.appendChild(arrow());
      var node=el("div","node"+(i===g.nodes.length-1?" last":""));node.setAttribute("role","listitem");
      node.appendChild(el("span","n",(n.n<10?"0":"")+n.n+(n.optional?" · optional":"")));
      node.appendChild(skillLink(n.name,n.page,"name"));
      node.appendChild(el("span","what",n.what));
      if(n.alternatives.length){
        var alt=el("span","alt","or ");
        n.alternatives.forEach(function(a,k){if(k)alt.appendChild(document.createTextNode(", "));alt.appendChild(skillLink(a.name,a.page));});
        node.appendChild(alt);
      }
      graph.appendChild(node);
    });
    box.appendChild(graph);
    if(g.install.length){
      var ins=el("div","install"),pre=el("pre",null,g.install.join("\n"));
      var copy=el("button","btn btn-light","Copy the install lines");copy.type="button";
      copy.addEventListener("click",function(){T.copyText(copy,g.install.join("\n"));});
      ins.appendChild(pre);ins.appendChild(copy);box.appendChild(ins);
    }
    var note=el("p","note",flow.note?flow.note+" ":"");
    var full=el("a",null,"Open the full workflow page");full.href="/workflows/"+flow.slug+"/";note.appendChild(full);
    box.appendChild(note);
    result.appendChild(box);

    var after=el("div","after");
    if(typed){
      var why=el("div");why.appendChild(el("b",null,"Why this route"));
      why.appendChild(el("p",null,hit.matched.length?"Your words matched: "+hit.matched.join(", ")+". The match is by word, with no model behind it, so check that the goal above is the one you meant.":"None of your words matched a workflow, so this is the first one on the list."));
      after.appendChild(why);
      if(second){
        var other=el("div");other.appendChild(el("b",null,"Or did you mean this?"));
        var p=el("p"),b=el("button","link","Brew "+second.flow.number+" · "+second.flow.name+": "+second.flow.title);b.type="button";
        b.addEventListener("click",function(){draw(d,ranked,ranked.indexOf(second),true);});
        p.appendChild(b);other.appendChild(p);after.appendChild(other);
      }
    }
    var none=el("div");none.appendChild(el("b",null,"Nothing fits?"));
    var np=el("p",null,"We build the missing skill for your team at a fixed price. ");var wl=el("a",null,"See custom work");wl.href="/work/";np.appendChild(wl);
    none.appendChild(np);after.appendChild(none);
    result.appendChild(after);
    result.hidden=false;T.reveal(result);
  }

  function run(){
    var q=goal.value.trim();
    if(!q){say("Say what you are trying to get done, or pick a goal below.",true);goal.focus();return;}
    say("");
    load().then(function(d){
      var ranked=M.rank(q,d);
      if(!ranked.length){say("The workflow list is empty.",true);return;}
      if(ranked[0].score===0){
        result.textContent="";
        result.appendChild(el("p","verdict","No workflow matches those words."));
        result.appendChild(el("p","passed","Try the words you would use with a colleague, such as \"launch\", \"job\", \"traffic\" or \"cold email\", or pick a goal from the list above."));
        result.appendChild(T.upsell("It may be a skill nobody has written yet.","We scope it on a short call, test it on your real tasks and hand it over as a repo you own.","See custom work","/work/"));
        result.hidden=false;T.reveal(result);return;
      }
      draw(d,ranked,0,true);
    }).catch(function(){say("Could not load the workflow list. Reload the page and try again.",true);});
  }
  form.addEventListener("submit",function(e){e.preventDefault();run();});

  /* one chip per workflow, from the same list, so the page never names a route that is gone */
  load().then(function(d){
    (d.workflows||[]).forEach(function(flow,i){
      var b=el("button",null,flow.title);b.type="button";
      b.addEventListener("click",function(){
        goal.value="";say("");
        var ranked=(d.workflows||[]).map(function(f){return {flow:f,score:0,matched:[]};});
        draw(d,ranked,i,false);
      });
      chips.appendChild(b);
    });
  }).catch(function(){});
})();

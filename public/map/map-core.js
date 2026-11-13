/* Workflow Map core: matches a plain-language goal to one of the workflows in site/skills.json.
   No model and no network: it scores the words you typed against each workflow's title, summary,
   skills and a short list of everyday words for the same job. Runs in the browser and in Node. */
(function(root){
  var STOP={};"a an and are as at be but by can do does for from get have how i i'm if in into is it its me my need of on or our so that the their them this to up us want we what when which who why will with would you your please help make made using use".split(" ").forEach(function(w){STOP[w]=1;});
  /* Everyday words people use for each workflow, keyed by its id in the manifest. A workflow
     without an entry here still matches on its own title, summary and skills. */
  var WORDS={
    "pour-over":"skill skills prompt prompts create write author draft package release publish installable template agent-skill skill.md",
    "bloom":"found find discover discovery discoverable findable visibility visible github repo repository stars readme listing directory directories nobody indexed plugin mcp",
    "espresso":"launch launching safe safely ship shipping deploy deployment security secure hack hacked vulnerability vulnerabilities exposed leak performance slow speed fast production ready live preflight release pentest",
    "cold-brew":"seo search traffic google rank ranking rankings keyword keywords organic content blog visitors serp cannibalization impressions clicks",
    "french-press":"job jobs resume cv recruiter recruiters interview interviews hire hired hiring linkedin application applications apply applying career cover letter offer",
    "cupping":"should buy vendor versus vs pick decide decision decisions choose choice option options research compare comparison strategy whether memo analysis analyse analyze data numbers tradeoff pros cons",
    "slow-drip":"learn learning study studying teach teaching course curriculum understand topic lesson lessons exam practice tutor beginner",
    "nitro":"cold email emails outbound lead leads list prospect prospects prospecting sales outreach send sending deliverability inbox campaign sequence b2b",
    "moka-pot":"product business startup solo income money side project saas landing page website site idea sell online indie founder customers revenue mvp",
    "descale":"maintain maintenance update updates regress regression health broken stale upkeep drift nightly",
    "estate-roast":"audit estate collection inventory portfolio marketplace catalogue catalog dozens many whole all",
    "dial-in":"claude code codex cursor coding agent agents setup set configure configuration claude.md agents.md harness rules usage limit limits quota tokens effort model hooks"
  };
  function stem(w){
    if(w.length>5&&/ing$/.test(w))return w.slice(0,-3);
    if(w.length>4&&/ies$/.test(w))return w.slice(0,-3)+"y";
    if(w.length>4&&/ed$/.test(w))return w.slice(0,-2);
    if(w.length>3&&/s$/.test(w)&&!/ss$/.test(w))return w.slice(0,-1);
    return w;
  }
  function tokens(text){
    return (String(text).toLowerCase().match(/[a-z0-9][a-z0-9.+#-]*/g)||[]).map(function(w){return w.replace(/[.-]+$/,"");})
      .filter(function(w){return w&&!STOP[w];}).map(stem);
  }
  function firstSentence(text){
    var m=/^(.*?[.!?])(\s|$)/.exec(String(text||"").trim());
    return (m?m[1]:String(text||"").trim());
  }

  /* manifest: the parsed site/skills.json. Returns the workflows ranked best first, each as
     {flow, score, matched[]}; a score of 0 means none of your words matched it. */
  function rank(query,manifest){
    var skills={};
    (manifest.skills||[]).forEach(function(s){skills[s.name]=s;});
    var q=tokens(query),uniq={};
    q.forEach(function(t){uniq[t]=1;});
    return (manifest.workflows||[]).map(function(flow,i){
      var bag={};
      function add(text,weight){tokens(text).forEach(function(t){if(!bag[t]||bag[t]<weight)bag[t]=weight;});}
      add(flow.title,4);add(String(flow.slug||"").replace(/-/g," "),4);add(WORDS[flow.id]||"",3);add(flow.summary,2);
      (flow.steps||[]).forEach(function(step){
        (step.skills||[]).forEach(function(name){
          add(name.replace(/-/g," "),2);
          if(skills[name])add(skills[name].blurb,1);
        });
      });
      var score=0,matched=[];
      Object.keys(uniq).forEach(function(t){if(bag[t]){score+=bag[t];matched.push(t);}});
      return {flow:flow,score:score,matched:matched,i:i};
    }).sort(function(a,b){return b.score-a.score||a.i-b.i;});
  }

  /* One workflow as a graph: an ordered list of nodes, each with its main skill, the
     alternatives for that step, what the skill does, and the install lines for the route. */
  function graph(flow,manifest){
    var skills={};
    (manifest.skills||[]).forEach(function(s){skills[s.name]=s;});
    var nodes=(flow.steps||[]).map(function(step,i){
      var names=step.skills||[],main=skills[names[0]]||{name:names[0]};
      return {
        n:i+1,name:names[0],optional:!!step.optional,
        what:firstSentence(main.blurb),
        page:main.page&&main.page!=="none"?"/"+main.name+"/":"",
        install:main.install||"",
        alternatives:names.slice(1).map(function(n){var s=skills[n]||{};return {name:n,page:s.page&&s.page!=="none"?"/"+n+"/":""};})
      };
    });
    return {nodes:nodes,install:nodes.filter(function(n){return !n.optional&&n.install;}).map(function(n){return n.install;})};
  }

  var api={rank:rank,graph:graph,tokens:tokens};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.WorkflowMap=api;
})(typeof self!=="undefined"?self:this);

/* Star prompt for the free tools. Once a tool has drawn a result into #result, add one line under it
   that points at the single repo to star (arm-pz/caffeinity-skills) and at the open skill that does
   the next step. Tools rebuild #result from scratch on every run, so watch it and add the line back.
   Built with textContent only, like the rest of the tools. */
(function(){
  var REPO="https://github.com/arm-pz/caffeinity-skills";
  var result=document.getElementById("result");
  if(!result)return;
  var skill=document.body.getAttribute("data-skill")||"";
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
  function build(){
    var box=el("aside","star-cta");box.setAttribute("aria-label","Star the open-source repo");
    var p=el("p");
    p.appendChild(el("b",null,"Was that useful? Star the repo behind it."));
    p.appendChild(document.createTextNode(
      "This check is a small part of an MIT-licensed set of agent skills for Claude Code, Codex and Cursor"+
      (skill?". The full version of this check is "+skill+", which your own agent can run.":".")+
      " A star is how other developers find it."));
    box.appendChild(p);
    var a=el("a","btn btn-accent star-btn","★ Star on GitHub");
    a.href=REPO;a.rel="noopener";a.target="_blank";
    box.appendChild(a);
    return box;
  }
  function sync(){
    if(result.hidden||!result.firstChild)return;
    if(result.querySelector(".star-cta"))return;
    result.appendChild(build());
  }
  new MutationObserver(sync).observe(result,{childList:true,attributes:true,attributeFilter:["hidden"]});
  sync();
})();

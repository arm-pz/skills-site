/* Shared helpers for the free tools. Every page builds its result with textContent only, so
   pasted text is always shown as text and never run. */
(function(root){
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
  function plural(n,one,many){return n.toLocaleString("en")+" "+(n===1?one:many);}
  function copyText(btn,body){
    var label=btn.textContent;
    var done=function(){btn.textContent="Copied";setTimeout(function(){btn.textContent=label;},1600);};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(body).then(done,function(){window.prompt("Copy:",body);});
    else window.prompt("Copy:",body);
  }
  function reveal(node){node.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});}
  /* One finding card: level chip, message, then optional evidence, why and fix. */
  function finding(level,msg,o){
    o=o||{};
    var cls={FAIL:"fail","NOT CHECKED":"skip"}[level]||"";
    var li=el("li","finding "+cls);
    li.appendChild(el("span","lvl",level));li.appendChild(el("span","msg",msg));
    if(o.evidence)li.appendChild(el("p","ev",o.evidence));
    if(o.terms&&o.terms.length){var t=el("p","terms");o.terms.forEach(function(x){t.appendChild(el("span",null,x));});li.appendChild(t);}
    if(o.why)li.appendChild(el("p",null,o.why));
    if(o.fix){var f=el("p");f.appendChild(el("b",null,"Fix. "));f.appendChild(document.createTextNode(o.fix));li.appendChild(f);}
    return li;
  }
  /* The pasted text as numbered lines, with spans [{line, col, len, title}] marked in place. */
  function markedDraft(lines,spans,label){
    var by={};
    spans.forEach(function(s){(by[s.line]=by[s.line]||[]).push(s);});
    var draft=el("div","draft");draft.setAttribute("role","group");draft.setAttribute("aria-label",label);
    lines.forEach(function(raw,i){
      var row=el("div","ln"),tx=el("span","tx"),at=0;
      row.appendChild(el("span","no",String(i+1)));
      (by[i+1]||[]).sort(function(a,b){return a.col-b.col;}).forEach(function(s){
        if(s.col<at)return;
        if(s.col>at)tx.appendChild(document.createTextNode(raw.slice(at,s.col)));
        var m=el("mark",null,raw.slice(s.col,s.col+s.len));if(s.title)m.title=s.title;
        tx.appendChild(m);at=s.col+s.len;
      });
      tx.appendChild(document.createTextNode(raw.slice(at)||(at?"":" ")));
      row.appendChild(tx);draft.appendChild(row);
    });
    return draft;
  }
  function upsell(title,body,label,href){
    var up=el("div","upsell"),p=el("p");
    p.appendChild(el("b",null,title));p.appendChild(document.createTextNode(body));up.appendChild(p);
    var a=el("a","btn btn-accent",label);a.href=href;up.appendChild(a);
    return up;
  }
  root.Tool={el:el,plural:plural,copyText:copyText,reveal:reveal,finding:finding,markedDraft:markedDraft,upsell:upsell};
})(window);

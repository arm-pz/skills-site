/* Prose Check page: runs /prose/prose-core.js on the pasted draft in the browser and renders the
   hits in place. The draft is never sent anywhere; this file makes no network request. */
(function(){
  /* Payment link. Leave it empty and the order buttons open an email instead.
     Paste a hosted checkout URL (for example a Stripe Payment Link) to take payment directly. */
  var PAY={edit:""};
  var MAX_CHARS=400000;

  /* rule id: [label, why it reads as machine-written, how to fix it] */
  var RULES={
    "em-dash":["Em dashes","Language models reach for the em dash far more often than most people do, and readers now treat a page full of them as a sign nobody edited it.","Use a comma, a full stop, a colon or brackets. Often the sentence is really two sentences."],
    "vocabulary":["Stock vocabulary","These words were ordinary until models started using them in every answer. One is fine when it is the clearest word. Several close together is the pattern.","Say the plain thing: \"is\" for \"serves as\", \"uses\" for \"utilises\", \"important\" or nothing at all for \"crucial\". Rewrite the sentence if swapping the word leaves it empty."],
    "promotional":["Promotional wording","Praise words tell the reader how to feel instead of giving them something to judge. Outside an advert, they read as a press release.","Replace the adjective with the fact behind it: the number, the date, what the thing does."],
    "significance":["Inflated significance","Ordinary facts get dressed up as turning points and broader trends. Readers discount the whole page once they notice.","State the fact and stop. Keep the claim only if you can say what changed and who says so."],
    "vague-attribution":["Vague attribution","\"Experts say\" names nobody, so the reader cannot check it. It is how a model sounds sure without a source.","Name the person, study or report, or make the claim in your own voice."],
    "chatbot-phrase":["Chatbot phrases","These are the opening and closing lines of a chat reply. Left in a document, they show it was pasted from one.","Delete them. Start with the answer and end when you have finished."],
    "negative-parallelism":["Contrast formulas","\"Not just X, but Y\" and \"it's not X, it's Y\" invent something to correct so the real point sounds bigger. The scanner also marks every \"rather than\", which is often fine.","Say the point directly. If nobody claimed X, leave X out."],
    "ing-tail":["Trailing \"-ing\" analysis","A fact followed by \", highlighting…\" or \", underscoring…\" tacks on an interpretation nobody asked for.","End the sentence at the fact. If the interpretation matters, give it its own sentence and say whose it is."],
    "canned-opener":["Canned openers","\"In conclusion\", \"Overall\" and \"Additionally\" announce a structure instead of adding to it.","Drop the opener. If the paragraph only repeats what came before, drop the paragraph."],
    "vague-relationship":["Vague relationships","\"Associated with\" hides what the relationship is. It can be the right phrase when the link really is loose.","Say what the link is: founded, funded, worked at, caused."],
    "placeholder":["Template placeholders","Text such as [Your Name] was meant to be filled in. Sending it is the surest sign a draft was not read.","Fill it in or delete it."],
    "tool-markup":["Tool markup and tracking","Citation tokens and utm_ parameters are left behind by chat tools when text is copied out of them.","Delete the tokens. Strip tracking parameters from links."],
    "title-case-heading":["Title-case headings","Capitalising Every Word Of A Heading is a model default. Many house styles do ask for it, so this is a style call.","Use sentence case unless your style guide says otherwise."],
    "emoji-decoration":["Emoji decoration","Emoji used as bullets or in front of headings is a chat-reply habit.","Remove them, unless the place you are publishing really uses them."],
    "horizontal-rule":["Section-break rules","A rule between every section is chat formatting. Headings already separate the sections.","Delete the rule."],
    "bold-label-list":["Bold-label bullet lists","A list where every bullet is a bold label and an explanation is the stock shape of a model answer.","Write it as a paragraph, or keep the list and drop the bold labels."],
    "curly-quote":["Curly quotes","In a plain-text destination such as code, a terminal or some forms, curly quotes can break or show as odd characters.","Use straight quotes there. In ordinary prose, curly quotes are correct."]
  };
  var ORDER=["chatbot-phrase","placeholder","tool-markup","em-dash","vocabulary","promotional","significance","vague-attribution","negative-parallelism","ing-tail","canned-opener","vague-relationship","bold-label-list","title-case-heading","emoji-decoration","horizontal-rule","curly-quote"];

  var SAMPLE="Great question! Here's a comprehensive overview of our new office.\n\n## A New Chapter For The Team\n\nNestled in the heart of the city, the new office is not just a workspace — it's a testament to our commitment to excellence. The move marks a significant shift for the company, underscoring our focus on collaboration, creativity, and growth.\n\n- **Location:** a vibrant neighbourhood with a rich tapestry of cafes\n- **Design:** a stunning open plan that fosters teamwork\n- **Technology:** robust tools that serve as the backbone of our work\n\nExperts say that offices like this play a pivotal role in retention. Additionally, staff associated with the pilot were happier, highlighting the value of the investment.\n\nIn conclusion, we moved on 3 March and the lease runs for five years. I hope this helps!\n\nRegards,\n[Your Name]\n";

  var $=function(id){return document.getElementById(id);};
  var form=$("form"),text=$("text"),plain=$("plain"),statusEl=$("status"),result=$("result");
  if(!form||!window.ProseCheck)return;
  var live=false,timer=0,focusRule="";

  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}
  function plural(n,one,many){return n.toLocaleString("en")+" "+(n===1?one:many);}
  function copyText(btn,body,label){
    var done=function(){btn.textContent="Copied";setTimeout(function(){btn.textContent=label;},1600);};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(body).then(done,function(){window.prompt("Copy:",body);});
    else window.prompt("Copy:",body);
  }

  /* Lists of exactly three short items ("fast, cheap and good"). The scanner cannot judge these,
     so they are shown as a softer mark and never counted as hits. */
  var ITEM="[\\p{L}\\p{N}'’-]+(?: [\\p{L}\\p{N}'’-]+){0,2}";
  var THREE=new RegExp("(?<![,;:] )(?<![\\p{L}\\p{N}'’-])"+ITEM+", "+ITEM+",? (?:and|or) "+ITEM,"gu");
  function threes(lines){
    var out=[],fence=false;
    lines.forEach(function(raw,i){
      var t=raw.replace(/^\s+/,"");
      if(t.indexOf("```")===0||t.indexOf("~~~")===0){fence=!fence;return;}
      if(fence)return;
      var m;THREE.lastIndex=0;
      while((m=THREE.exec(raw)))out.push({line:i+1,col:m.index,len:m[0].length,text:m[0]});
    });
    return out;
  }

  function lineRanges(nums){
    var uniq=[],seen={};
    nums.forEach(function(n){if(!seen[n]){seen[n]=1;uniq.push(n);}});
    var parts=[],i=0;
    while(i<uniq.length){
      var j=i;while(j+1<uniq.length&&uniq[j+1]===uniq[j]+1)j++;
      parts.push(j>i?uniq[i]+" to "+uniq[j]:String(uniq[i]));i=j+1;
    }
    var shown=parts.slice(0,12).join(", ");
    return (uniq.length===1&&parts[0].indexOf(" ")<0?"line ":"lines ")+shown+(parts.length>12?" and more":"");
  }

  function fixPrompt(src,hits){
    var L=["Edit the draft below. Change only the sentences that carry one of the patterns listed, and keep everything else word for word, in the author's own voice, spelling and level of formality.","",
      "For each flagged sentence, rewrite it so it states its actual point. Do not just delete or swap the flagged word, because that leaves the same empty sentence behind. Do not add em dashes. Do not add praise, summaries or offers of more help. If a claim has nothing to support it, cut it and say so in one line after the text.","",
      "Return the finished text and nothing else.","","Patterns found (line, rule, matched text):"];
    hits.slice(0,300).forEach(function(h){L.push("- line "+h.line+", "+h.rule+": "+h.text);});
    if(hits.length>300)L.push("- and "+(hits.length-300)+" more of the same kinds");
    L.push("","Draft:","<<<",src.replace(/\s+$/,""),">>>");
    return L.join("\n");
  }

  function setFocus(rule){
    focusRule=focusRule===rule?"":rule;
    [].forEach.call(result.querySelectorAll("mark[data-rule],.ln[data-rules]"),function(m){
      var rules=(m.getAttribute("data-rule")||m.getAttribute("data-rules")||"").split(" ");
      m.classList.toggle("on",!!focusRule&&rules.indexOf(focusRule)>=0);
    });
    [].forEach.call(result.querySelectorAll("[data-show]"),function(b){
      var on=b.getAttribute("data-show")===focusRule;
      b.setAttribute("aria-pressed",on?"true":"false");
    });
    var draft=result.querySelector(".draft");
    if(draft)draft.classList.toggle("focused",!!focusRule);
  }

  function render(src,scroll){
    var hits=window.ProseCheck.scan(src,{plainText:plain.checked});
    var lines=src.replace(/^﻿/,"").replace(/\r\n/g,"\n").split("\n");
    var notes=threes(lines);
    var words=(src.match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu)||[]).length;
    var byRule={};
    hits.forEach(function(h){(byRule[h.rule]=byRule[h.rule]||[]).push(h);});
    var ruleIds=ORDER.filter(function(r){return byRule[r];}).concat(Object.keys(byRule).filter(function(r){return ORDER.indexOf(r)<0;}));

    result.textContent="";
    result.appendChild(el("p","verdict",hits.length
      ?plural(hits.length,"stock pattern","stock patterns")+" in "+plural(words,"word","words")+"."
      :"None of the listed patterns found."));
    if(!hits.length)result.appendChild(el("p","clean","That proves less than it sounds. A script cannot see a forced group of three, an inflated claim in fresh words, or a sentence that sounds good and says nothing. Read it once more for those."));

    var facts=el("div","facts");
    function fact(v,k){var s=el("span");s.appendChild(el("b",null,v));s.appendChild(document.createTextNode(" "+k));facts.appendChild(s);}
    if(hits.length){
      fact(String(ruleIds.length),ruleIds.length===1?"kind of pattern":"kinds of pattern");
      if(words>=50)fact((hits.length*1000/words).toFixed(1),"per 1,000 words");
    }
    if(notes.length)fact(String(notes.length),notes.length===1?"list of three to look at":"lists of three to look at");
    if(facts.children.length)result.appendChild(facts);

    /* the draft, with every hit marked where it sits */
    if(hits.length||notes.length){
      var spans={},lineRules={};
      hits.forEach(function(h){
        if(h.col>=0)(spans[h.line]=spans[h.line]||[]).push({s:h.col,e:h.col+h.len,rule:h.rule});
        else for(var k=0;k<(h.span||1);k++){var ln=h.line+k;(lineRules[ln]=lineRules[ln]||[]).push(h.rule);}
      });
      notes.forEach(function(t){(spans[t.line]=spans[t.line]||[]).push({s:t.col,e:t.col+t.len,rule:"",soft:true});});
      var first=Infinity,last=0;
      Object.keys(spans).concat(Object.keys(lineRules)).forEach(function(k){first=Math.min(first,+k);last=Math.max(last,+k);});
      var draft=el("div","draft");draft.setAttribute("role","group");draft.setAttribute("aria-label","Your draft with each pattern marked");
      lines.forEach(function(raw,i){
        var n=i+1,row=el("div","ln"),tx=el("span","tx");
        row.appendChild(el("span","no",String(n)));
        var list=(spans[n]||[]).slice().sort(function(a,b){return a.s-b.s||(a.soft?1:0)-(b.soft?1:0)||b.e-a.e;});
        /* a hit inside or across another: merge into one mark that carries both rules */
        var merged=[];
        list.forEach(function(sp){
          var prev=merged[merged.length-1];
          if(prev&&sp.s<prev.e){
            if(sp.soft&&!prev.soft)return;
            if(prev.soft&&!sp.soft){
              /* a real hit inside a list of three: the hit wins, the soft mark is cut around it */
              var tail={s:sp.e,e:prev.e,rule:"",soft:true};prev.e=sp.s;
              if(prev.e<=prev.s)merged.pop();
              merged.push(sp);if(tail.e>tail.s)merged.push(tail);return;
            }
            prev.e=Math.max(prev.e,sp.e);
            if(sp.rule&&prev.rule.split(" ").indexOf(sp.rule)<0)prev.rule+=" "+sp.rule;
            return;
          }
          merged.push({s:sp.s,e:sp.e,rule:sp.rule,soft:sp.soft});
        });
        merged.sort(function(a,b){return a.s-b.s;});
        var at=0;
        merged.forEach(function(sp){
          if(sp.s<at)return;
          if(sp.s>at)tx.appendChild(document.createTextNode(raw.slice(at,sp.s)));
          var m=el("mark",sp.soft?"soft":null,raw.slice(sp.s,sp.e));
          if(sp.soft)m.title="A list of exactly three. Is three the real count?";
          else{
            m.setAttribute("data-rule",sp.rule);
            m.title=sp.rule.split(" ").map(function(r){return RULES[r]?RULES[r][0]:r;}).join(" and ");
          }
          tx.appendChild(m);at=sp.e;
        });
        tx.appendChild(document.createTextNode(raw.slice(at)||(at?"":" ")));
        if(lineRules[n]){
          row.setAttribute("data-rules",lineRules[n].join(" "));row.classList.add("whole");
          row.title=lineRules[n].map(function(r){return RULES[r]?RULES[r][0]:r;}).join(" and ");
        }
        row.appendChild(tx);draft.appendChild(row);
      });
      result.appendChild(draft);
      var legend=el("p","legend");
      if(hits.length){legend.appendChild(el("mark",null,"marked"));legend.appendChild(document.createTextNode(" a listed pattern. "));}
      if(notes.length){legend.appendChild(el("mark","soft","dotted"));legend.appendChild(document.createTextNode(" a list of exactly three, which only you can judge. "));}
      legend.appendChild(document.createTextNode("Edit the box above and the marks update as you type."));
      result.appendChild(legend);
    }

    /* one card per kind of pattern */
    if(hits.length){
      var list=el("ul","findings");
      ruleIds.forEach(function(rule){
        var hs=byRule[rule],meta=RULES[rule]||[rule,"",""];
        var li=el("li","finding");
        var head=el("div","head");
        head.appendChild(el("span","lvl","×"+hs.length));
        head.appendChild(el("span","msg",meta[0]));
        var show=el("button","link","Show in the draft");show.type="button";
        show.setAttribute("data-show",rule);show.setAttribute("aria-pressed","false");
        show.addEventListener("click",function(){
          setFocus(rule);
          if(focusRule){var first=result.querySelector(".draft .on");if(first)first.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"center"});}
        });
        head.appendChild(show);li.appendChild(head);
        var where=el("p","where",lineRanges(hs.map(function(h){return h.line;}))+": ");
        var seen={},quotes=[];
        hs.forEach(function(h){var q=h.text.trim();if(q&&!seen[q.toLowerCase()]){seen[q.toLowerCase()]=1;quotes.push(q);}});
        quotes.slice(0,8).forEach(function(q,i){
          if(i)where.appendChild(document.createTextNode(" "));
          where.appendChild(el("q",null,q.length>70?q.slice(0,67)+"…":q));
        });
        if(quotes.length>8)where.appendChild(document.createTextNode(" and "+(quotes.length-8)+" more"));
        li.appendChild(where);
        if(meta[1]){var why=el("p");why.appendChild(el("b",null,"Why it stands out. "));why.appendChild(document.createTextNode(meta[1]));li.appendChild(why);}
        if(meta[2]){var fix=el("p");fix.appendChild(el("b",null,"Fix. "));fix.appendChild(document.createTextNode(meta[2]));li.appendChild(fix);}
        list.appendChild(li);
      });
      result.appendChild(list);
      result.appendChild(el("p","skipped","A hit is a reason to look, since a listed word is sometimes the clearest one. These patterns are habits people have too, so the result says nothing about who or what wrote the text."));
    }

    var actions=el("div","result-actions");
    if(hits.length){
      var pr=el("button","btn btn-accent","Copy a fix prompt");pr.type="button";
      pr.addEventListener("click",function(){copyText(pr,fixPrompt(src,hits),"Copy a fix prompt");});
      actions.appendChild(pr);
    }
    var copy=el("button","btn btn-quiet","Copy the report");copy.type="button";
    copy.addEventListener("click",function(){copyText(copy,window.ProseCheck.report(hits)+"\n\nChecked with https://skillsmith.tech/prose/","Copy the report");});
    actions.appendChild(copy);
    result.appendChild(actions);
    if(hits.length)result.appendChild(el("p","small hint","The fix prompt holds your draft, the hits and the editing rules. Paste it into any chat model to get the flagged sentences rewritten and the rest left alone."));

    var up=el("div","upsell"),p=el("p");
    p.appendChild(el("b",null,hits.length?"Stop the patterns before they are written.":"Keep the next draft clean too."));
    p.appendChild(document.createTextNode("straight-prose is the free, open skill behind this page. Install it and your agent applies these rules while it drafts, then runs this same scan before it hands the text back."));
    up.appendChild(p);
    var a=el("a","btn btn-accent","Get the skill, free");a.href="#skill";
    up.appendChild(a);result.appendChild(up);

    result.hidden=false;
    if(focusRule){var keep=focusRule;focusRule="";if(byRule[keep])setFocus(keep);}
    if(scroll)result.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
  }

  function run(scroll){
    var src=text.value;
    if(!src.trim()){
      live=false;result.hidden=true;result.textContent="";
      if(scroll){say("Paste a draft first.",true);text.focus();}
      return;
    }
    if(src.length>MAX_CHARS){say("That is over "+MAX_CHARS.toLocaleString("en")+" characters. Check it a chapter at a time.",true);return;}
    say("");live=true;render(src,scroll);
  }

  form.addEventListener("submit",function(e){e.preventDefault();run(true);});
  text.addEventListener("keydown",function(e){if((e.ctrlKey||e.metaKey)&&e.key==="Enter"){e.preventDefault();run(true);}});
  text.addEventListener("input",function(){
    if(!live)return;
    clearTimeout(timer);timer=setTimeout(function(){run(false);},250);
  });
  plain.addEventListener("change",function(){if(live)run(false);});
  $("sample").addEventListener("click",function(){text.value=SAMPLE;focusRule="";run(true);});
  $("clear").addEventListener("click",function(){text.value="";focusRule="";say("");run(false);text.focus();});

  [].forEach.call(document.querySelectorAll("[data-order]"),function(a){
    var kind=a.getAttribute("data-order");
    if(PAY[kind])a.href=PAY[kind];
  });
})();

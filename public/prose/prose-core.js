/* Prose Check core: a line-for-line port of straight-prose's scripts/slop_scan.py (MIT,
   github.com/arm-pz/straight-prose). Runs in the browser and in Node
   (tools/agent-skills/tests/prose_parity.mjs compares it to the Python original).
   Python's \b, \w, \d and \s are Unicode-aware and JavaScript's are not, so the patterns below
   are built from the script's own strings with those four classes spelled out. */
(function(root){
  var W="\\p{L}\\p{N}_";
  var WS="\\t\\n\\v\\f\\r\\x1c-\\x1f \\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000";
  var B="(?:(?<=["+W+"])(?!["+W+"])|(?<!["+W+"])(?=["+W+"]))";
  function rx(src,flags){
    return new RegExp(src.replace(/\\b/g,B).replace(/\\w/g,"["+W+"]").replace(/\\d/g,"\\p{Nd}").replace(/\\s/g,"["+WS+"]"),"u"+(flags||""));
  }

  var VOCAB="delv(e|es|ed|ing)|deep dives?|crucial|pivotal|intricate|intricacies|tapestry|vibrant|"+
    "landscape|enduring|testament|underscor(e|es|ed|ing)|showcas(e|es|ed|ing)|foster(s|ed|ing)?|"+
    "garner(s|ed|ing)?|robust|interplay|meticulous(ly)?|aligns? with|resonates? with|"+
    "bolster(s|ed|ing)?|utili[sz](e|es|ed|ing)|serves? as|boasts?";
  var PROMO="renowned|groundbreaking|breathtaking|nestled|world-class|stunning|diverse array|"+
    "commitment to excellence|remarkable|profound|innovative|impressive";
  var SIGNIFICANCE="marks? a (major |significant )?(shift|turning point)|turning point|broader trend|"+
    "enduring legacy|plays? a (pivotal|crucial|key|vital) role|sets? the stage|"+
    "broader landscape|stands as a";
  var ATTRIBUTION="experts (say|believe|agree)|observers have noted|critics argue|"+
    "industry reports suggest|sources indicate|many believe|studies show";
  var CHATBOT="of course!|certainly!|absolutely!|you're absolutely right|great question|"+
    "i hope this helps|here is a detailed breakdown|here's a comprehensive overview|"+
    "would you like me to|let me know if you'd like|is there anything else|"+
    "i'm happy to|feel free to";
  var PARALLEL="not only\\b[^.\\n]{0,80}\\bbut|not just\\b[^.\\n]{0,80}\\bbut|"+
    "\\bnot (just|only|merely)\\b[^.\\n]{0,60}[,;\\u2014] ?(it|this|that|they)(['’]s|['’]re| is| are)\\b|"+
    "\\b(it|this|that)(['’]s| is) not\\b[^.\\n]{0,60}[,;.] (it|this|that)(['’]s| is)\\b|"+
    "\\b(is|are|was)n['’]t\\b[^.\\n]{0,60}\\. (It|They|This)(['’]s|['’]re| is| are)\\b|"+
    "\\bnot\\b[^.\\n]{0,40}, but rather\\b|\\bno \\w+, no \\w+, just\\b|\\brather than\\b";
  var ING_TAIL=", (highlighting|underscoring|reflecting|ensuring|fostering|enhancing|symboli[sz]ing|"+
    "demonstrating|showcasing|contributing to)\\b";
  var CANNED="^(in conclusion|in summary|overall|additionally)\\b,?";
  var PLACEHOLDER="\\[(your|insert|specific|add|name|company|date)\\b[^\\]\\n]*\\]|XX/XX/XXXX|INSERT_URL|"+
    "SOURCE_PUBLISHER|lorem ipsum";
  var MARKUP="【[^】]*】|oaicite|contentReference|turn\\d+(search|view|news)\\d+|\\butm_[a-z]+=";
  var RELATION="associated with|connected to|linked with|in connection with";

  var LINE_RULES=[
    ["em-dash",rx("\\u2014","g")],
    ["vocabulary",rx("\\b("+VOCAB+")\\b","gi")],
    ["promotional",rx("\\b("+PROMO+")\\b","gi")],
    ["significance",rx("\\b("+SIGNIFICANCE+")\\b","gi")],
    ["vague-attribution",rx("\\b("+ATTRIBUTION+")\\b","gi")],
    ["chatbot-phrase",rx("("+CHATBOT+")","gi")],
    ["negative-parallelism",rx(PARALLEL,"gi")],
    ["ing-tail",rx(ING_TAIL,"gi")],
    ["canned-opener",rx(CANNED,"gi")],
    ["vague-relationship",rx("\\b("+RELATION+")\\b","gi")],
    ["placeholder",rx(PLACEHOLDER,"gi")],
    ["tool-markup",rx(MARKUP,"g")]
  ];
  var CURLY=/[‘’“”]/g;
  var EMOJI_SRC="[\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF\\u2B50\\u2B06\\u2705\\u274C]";
  var EMOJI=new RegExp(EMOJI_SRC,"u"),EMOJI_START=new RegExp("^"+EMOJI_SRC,"u");
  var HEADING=rx("^(#{1,6})\\s+([^\\n]+?)\\s*#*$");
  var BOLD_LABEL=rx("^\\s*([-*+]|\\d+[.)])\\s+\\*\\*[^*\\n]+\\*\\*\\s*[:–-]|^\\s*([-*+]|\\d+[.)])\\s+\\*\\*[^*\\n]+:\\*\\*");
  var RULE_LINE=rx("^\\s*([-*_])(\\s*\\1){2,}\\s*$");
  var BULLET=rx("^\\s*([-*+]|\\d+[.)])\\s+");
  var LEAD=new RegExp("^["+WS+"]+","u"),TRAIL=new RegExp("["+WS+"]+$","u");
  var SMALL={};"a an and as at but by for in of on or the to vs with".split(" ").forEach(function(w){SMALL[w]=1;});

  function strip(s){return s.replace(LEAD,"").replace(TRAIL,"");}
  function lstrip(s){return s.replace(LEAD,"");}

  /* True when a heading of three or more words capitalises every word that is not a small one. */
  function titleCase(heading){
    var words=heading.match(/[A-Za-z][A-Za-z'-]*/g)||[];
    if(words.length<3)return false;
    var rest=words.slice(1).filter(function(w){return !SMALL[w.toLowerCase()];})
      /* All-caps words are acronyms and say nothing about the casing style. */
      .filter(function(w){return !(w===w.toUpperCase()&&/[A-Z]/.test(w));});
    return rest.length>=2&&rest.every(function(w){return /[A-Z]/.test(w.charAt(0));});
  }

  /* Python sorts the hit tuples by code point; JavaScript compares UTF-16 units by default. */
  function cmpStr(a,b){
    var x=Array.from(a),y=Array.from(b),n=Math.min(x.length,y.length);
    for(var i=0;i<n;i++){var d=x[i].codePointAt(0)-y[i].codePointAt(0);if(d)return d;}
    return x.length-y.length;
  }

  /* text: the draft. opts.plainText: also flag curly quotes.
     Returns hits sorted as slop_scan.py sorts them. Each hit is {line, rule, text} as the script
     prints it, plus col and len: where the match sits in the original line (UTF-16 units), or
     col -1 for a hit that belongs to the whole line. */
  function scan(text,opts){
    opts=opts||{};
    var hits=[];
    var lines=String(text).replace(/^﻿/,"").replace(/\r\n/g,"\n").split("\n");
    var inFence=false,inFront=lines.length>0&&strip(lines[0])==="---",boldRun=[];
    lines.forEach(function(raw,i){
      var n=i+1;
      if(inFront){if(n>1&&strip(raw)==="---")inFront=false;return;}
      var ls=lstrip(raw);
      if(ls.indexOf("```")===0||ls.indexOf("~~~")===0){inFence=!inFence;return;}
      if(inFence)return;

      /* Inline code is removed before matching, as in the script; map[] turns a position in the
         stripped line back into one in the original, so the page can highlight the match. */
      var line="",map=[],last=0,cm,codeRe=/`[^`\n]*`/g,k;
      while((cm=codeRe.exec(raw))){
        for(k=last;k<cm.index;k++)map.push(k);
        line+=raw.slice(last,cm.index);last=cm.index+cm[0].length;
      }
      for(k=last;k<raw.length;k++)map.push(k);
      line+=raw.slice(last);
      function add(rule,found,start,length){
        var col=-1,len=0;
        if(start>=0&&length>0){col=map[start];len=map[start+length-1]+1-col;}
        hits.push({line:n,rule:rule,text:found,col:col,len:len});
      }

      LINE_RULES.forEach(function(pair){
        var rule=pair[0],re=pair[1],target=line,offset=0,m;
        if(rule==="canned-opener"){target=strip(line);offset=line.length-lstrip(line).length;}
        re.lastIndex=0;
        while((m=re.exec(target))){
          add(rule,m[0],m.index+offset,m[0].length);
          if(!m[0].length)re.lastIndex++;
        }
      });
      if(opts.plainText){
        var q;CURLY.lastIndex=0;
        while((q=CURLY.exec(line)))add("curly-quote",q[0],q.index,1);
      }

      var h=HEADING.exec(line);
      if(h){
        var at=h[1].length+h[0].slice(h[1].length).indexOf(h[2]);
        if(titleCase(h[2]))add("title-case-heading",h[2],at,h[2].length);
        if(EMOJI.test(h[2]))add("emoji-decoration",h[2],at,h[2].length);
      }else if(BULLET.test(line)&&EMOJI_START.test(line.replace(BULLET,""))){
        var s=strip(line);
        add("emoji-decoration",Array.from(s).slice(0,40).join(""),line.length-lstrip(line).length,s.length);
      }
      if(RULE_LINE.test(line))add("horizontal-rule",strip(line),-1,0);

      /* One bold-label bullet is ordinary; three in a row is the stock list format. */
      if(BOLD_LABEL.test(line))boldRun.push(n);
      else if(strip(line)&&line.charAt(0)!==" "&&line.charAt(0)!=="\t"){
        if(boldRun.length>=3)hits.push({line:boldRun[0],rule:"bold-label-list",text:boldRun.length+" bullets",col:-1,len:0,span:boldRun.length});
        boldRun=[];
      }
    });
    if(boldRun.length>=3)hits.push({line:boldRun[0],rule:"bold-label-list",text:boldRun.length+" bullets",col:-1,len:0,span:boldRun.length});
    return hits.sort(function(a,b){return a.line-b.line||cmpStr(a.rule,b.rule)||cmpStr(a.text,b.text);});
  }

  function pad(s,n,left){s=String(s);var gap=Math.max(0,n-Array.from(s).length),fill=new Array(gap+1).join(" ");return left?fill+s:s+fill;}

  /* The same lines slop_scan.py prints, for the copy button and the parity test. */
  function report(hits){
    var L=[],counts={};
    hits.forEach(function(h){
      counts[h.rule]=(counts[h.rule]||0)+1;
      L.push(pad(h.line,5,true)+"  "+pad(h.rule,22)+h.text);
    });
    var summary=Object.keys(counts).sort(cmpStr).map(function(r){return r+" "+counts[r];}).join(", ")||"none";
    L.push("");
    L.push(hits.length+" hits: "+summary);
    L.push("Not checked: groups of three, unlisted inflated wording, voice changes, empty sentences.");
    return L.join("\n");
  }

  var api={scan:scan,report:report};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.ProseCheck=api;
})(typeof self!=="undefined"?self:this);

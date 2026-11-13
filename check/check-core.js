/* Skill Check core: a line-for-line port of tune-skill's scripts/check_skill.py (MIT,
   github.com/arm-pz/tune-skill), using its no-PyYAML frontmatter parser. Runs in the browser
   and in Node (tools/agent-skills/tests/check_parity.mjs compares it to the Python original). */
(function(root){
  var MAX_DESC=1024,SOFT_DESC=950,MAX_BODY_LINES=500;
  var MOMENT_RE=/\b(before|prior to)\b[^.\n]{0,50}\b(push(ing)?|deploy(ing)?|ship(ping)?|releas(e|ing)|publish(ing)?|merg(e|ing)|going live)\b/gi;
  var NUMBERS={};"zero one two three four five six seven eight nine ten".split(" ").forEach(function(w,i){NUMBERS[w]=i;});

  function listSizes(body){
    var sizes={},rows=0,items=0;
    body.split("\n").concat([""]).forEach(function(line){
      var s=line.trim();
      if(s.charAt(0)==="|"){
        if(!/^\|[\s:|-]+\|?$/.test(s))rows++;
        return;
      }
      if(rows){sizes[rows-1]=true;rows=0;}
      if(/^(\d+[.)]|[-*])\s/.test(line)){items++;return;}
      if(items&&(!s||line.charAt(0)===" "||line.charAt(0)==="\t"))return;
      if(items){sizes[items]=true;items=0;}
    });
    if(items)sizes[items]=true;
    return sizes;
  }

  function parseSimple(block){
    var meta={},key=null,folded=false,lines=[];
    function flush(){if(key!==null&&lines.length)meta[key]=lines.join(folded?" ":"\n");}
    block.split("\n").forEach(function(raw){
      var m=/^([A-Za-z0-9_-]+):\s*(.*)$/.exec(raw);
      if(m){
        flush();
        key=m[1];var value=m[2].trim();lines=[];
        folded=value.charAt(0)===">";
        if(value.charAt(0)===">"||value.charAt(0)==="|")return;
        if(value.length>1&&value.charAt(0)===value.charAt(value.length-1)&&(value.charAt(0)==="'"||value.charAt(0)==='"')){
          value=value.slice(1,-1);
        }else if(/:\s|\s#/.test(value)){
          throw new Error("unquoted '"+key+"' value contains ': ' or ' #'; quote it or use a >- block");
        }
        meta[key]=value;key=null;
      }else if(key!==null&&raw.trim()){
        lines.push(raw.trim());
      }
    });
    flush();
    return meta;
  }

  function splitLines(s){
    if(!s)return [];
    var parts=s.split(/\r\n|[\n\r\v\f\x1c-\x1e\x85\u2028\u2029]/);
    if(parts[parts.length-1]==="")parts.pop();
    return parts;
  }

  /* text: the SKILL.md source. opts.folder: the folder name (omit when unknown).
     opts.exists(path): true/false for a path beside SKILL.md (omit when the folder can't be seen).
     Returns {fatal, fails[], warns[], note, descChars, bodyLines, skipped[]}; every finding is
     {id, msg} where msg is the exact check_skill.py wording. */
  function check(text,opts){
    opts=opts||{};
    var out={fatal:null,fails:[],warns:[],note:null,descChars:0,bodyLines:0,skipped:[],name:null};
    text=String(text).replace(/^\uFEFF/,"").replace(/\r\n/g,"\n");
    var match=/^---\n([\s\S]*?)\n---\n([\s\S]*)$/.exec(text);
    if(!match){out.fatal={id:"no-frontmatter",msg:"SKILL.md has no YAML frontmatter between --- lines"};return out;}
    var meta;
    try{meta=parseSimple(match[1]);}
    catch(e){out.fatal={id:"bad-yaml",msg:"frontmatter is not valid YAML: "+e.message};return out;}
    var body=match[2];
    function fail(id,msg){out.fails.push({id:id,msg:msg});}
    function warn(id,msg){out.warns.push({id:id,msg:msg});}

    var name=Object.prototype.hasOwnProperty.call(meta,"name")?meta.name:"";
    out.name=name||null;
    if(!name){fail("no-name","frontmatter has no name");}
    else{
      if(opts.folder==null)out.skipped.push("the name matches its folder");
      else if(name!==opts.folder)warn("name-folder","name '"+name+"' differs from folder '"+opts.folder+"'");
      if(!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name))fail("name-shape","name '"+name+"' should be lowercase words joined by hyphens");
      if(Array.from(name).length>64)fail("name-long","name is longer than 64 characters");
    }

    var rawDesc=Object.prototype.hasOwnProperty.call(meta,"description")?meta.description:"";
    var desc=rawDesc.trim().split(/\s+/).filter(Boolean).join(" ");
    if(!desc){fail("no-desc","frontmatter has no description");}
    else{
      var n=Array.from(desc).length;
      if(n>MAX_DESC)fail("desc-over","description is "+n+" characters, over the "+MAX_DESC+" limit");
      else if(n>SOFT_DESC)warn("desc-close","description is "+n+" characters, close to the "+MAX_DESC+" limit");
      var low=desc.toLowerCase();
      if(low.indexOf("use when")<0&&low.indexOf("use whenever")<0&&low.indexOf("use this")<0)
        warn("no-trigger","description has no 'Use when/whenever' trigger wording");
      if(low.indexOf("not for")<0&&low.indexOf("do not use")<0)
        warn("no-boundary","description has no 'Not for' boundary (fine for a skill with no siblings)");
    }
    out.descChars=Array.from(desc).length;

    var h1=/^#\s+(.+)$/m.exec(body);
    if(h1&&name){
      var slug=h1[1].toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");
      if(slug!==name)warn("h1-name","H1 '"+h1[1]+"' does not match name '"+name+"' (stale name?)");
    }

    var lines=splitLines(body).length;
    out.bodyLines=lines;
    if(lines>MAX_BODY_LINES)warn("body-long","body is "+lines+" lines; move detail into references/");

    var refs={},rm,refRe=/`((?:references|scripts|examples|assets)\/[^`\s]+)`/g;
    while((rm=refRe.exec(body)))refs[rm[1]]=true;
    var refList=Object.keys(refs).sort();
    if(refList.length){
      if(!opts.exists)out.skipped.push("the "+refList.length+" file"+(refList.length===1?"":"s")+" the body points to "+(refList.length===1?"exists":"exist"));
      else refList.forEach(function(ref){
        if(!opts.exists(ref))warn("missing-ref","body points to "+ref+", which is not in this folder");
      });
    }

    var cm,countRe=/\b(two|three|four|five|six|seven|eight|nine|ten)\s+(workflows|modes|commands|steps)\b/gi,sizes=null;
    while((cm=countRe.exec(body))){
      var claimed=NUMBERS[cm[1].toLowerCase()];
      sizes=sizes||listSizes(body);
      if(!sizes[claimed])warn("count-claim","body says '"+cm[0]+"' but no table or list in it has "+claimed+" entries");
    }

    var moments=body.match(MOMENT_RE)||[];
    if(moments.length>=2)out.note={id:"moment",msg:"body ties the skill to "+moments.length+" moments like 'before pushing or deploying'; if a skipped run is costly, skill-to-mod can add a trigger"};
    return out;
  }

  /* The same lines check_skill.py prints, for the copy button and the parity test. */
  function report(r){
    if(r.fatal)return "FAIL  "+r.fatal.msg;
    var L=[];
    r.fails.forEach(function(f){L.push("FAIL  "+f.msg);});
    r.warns.forEach(function(w){L.push("WARN  "+w.msg);});
    if(r.note)L.push("NOTE  "+r.note.msg);
    if(!r.fails.length&&!r.warns.length)L.push("OK    no findings");
    L.push("");
    L.push(r.fails.length+" fail, "+r.warns.length+" warn ("+r.descChars+" description chars, "+r.bodyLines+" body lines)");
    return L.join("\n");
  }

  var api={check:check,report:report};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.SkillCheck=api;
})(typeof self!=="undefined"?self:this);

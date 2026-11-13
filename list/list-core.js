/* List Gate core: the mailbox half of cold-email-list-gate, run on every row, plus the
   ten-row sample the skill asks a person to read. Runs in the browser and in Node. */
(function(root){
  var ROLE={};"info sales support admin contact hello office team marketing hr jobs careers billing accounts accounting enquiries inquiries enquiry inquiry help service services noreply no-reply donotreply webmaster postmaster abuse mail press media legal privacy security orders booking bookings reception finance".split(" ").forEach(function(w){ROLE[w]=1;});
  var TYPO={"gmial.com":"gmail.com","gmai.com":"gmail.com","gmail.co":"gmail.com","gamil.com":"gmail.com","gnail.com":"gmail.com","gmail.con":"gmail.com","gmaill.com":"gmail.com","gmail.cm":"gmail.com","hotmial.com":"hotmail.com","hotmal.com":"hotmail.com","hotmail.co":"hotmail.com","hotmail.con":"hotmail.com","yahooo.com":"yahoo.com","yaho.com":"yahoo.com","yahoo.co":"yahoo.com","yahoo.con":"yahoo.com","outlok.com":"outlook.com","outloo.com":"outlook.com","outlook.co":"outlook.com","outlook.con":"outlook.com","icloud.co":"icloud.com","iclod.com":"icloud.com"};
  var FREE={};"gmail.com yahoo.com hotmail.com outlook.com icloud.com aol.com proton.me protonmail.com live.com msn.com gmx.com mail.com yandex.com zoho.com".split(" ").forEach(function(d){FREE[d]=1;});
  var EMAIL=/^[a-z0-9._%+'-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i;

  /* RFC 4180 style: quoted fields, doubled quotes, line breaks inside quotes. The delimiter is
     whichever of comma, semicolon or tab the first line uses most. */
  function parse(text){
    text=String(text).replace(/^﻿/,"").replace(/\r\n?/g,"\n");
    var first=text.split("\n")[0]||"",delim=",",best=-1;
    [",",";","\t"].forEach(function(d){var n=first.split(d).length;if(n>best){best=n;delim=d;}});
    var rows=[],row=[],cell="",q=false;
    for(var i=0;i<text.length;i++){
      var c=text.charAt(i);
      if(q){
        if(c==='"'){if(text.charAt(i+1)==='"'){cell+='"';i++;}else q=false;}
        else cell+=c;
      }else if(c==='"'&&cell==="")q=true;
      else if(c===delim){row.push(cell);cell="";}
      else if(c==="\n"){row.push(cell);rows.push(row);row=[];cell="";}
      else cell+=c;
    }
    if(cell!==""||row.length){row.push(cell);rows.push(row);}
    return {rows:rows.filter(function(r){return r.some(function(x){return x.trim();});}),delim:delim};
  }
  function toCsv(rows,delim){
    return rows.map(function(r){
      return r.map(function(x){x=String(x==null?"":x);return /["\n\r]/.test(x)||x.indexOf(delim)>=0?'"'+x.replace(/"/g,'""')+'"':x;}).join(delim);
    }).join("\n")+"\n";
  }

  /* text: the CSV. opts.titles: the job titles you are targeting, comma separated (optional).
     Returns the verdict and every row's findings. A row is "wrong" when its address would
     bounce, hit a shared inbox or repeat, or (with titles given) when its title is off target. */
  function gate(text,opts){
    opts=opts||{};
    var parsed=parse(text),rows=parsed.rows,out={delim:parsed.delim,header:null,rows:[],total:0,wrong:0,counts:{},notes:[],cols:{}};
    if(!rows.length)return Object.assign(out,{verdict:"EMPTY"});
    var hasHeader=!rows[0].some(function(x){return x.indexOf("@")>=0;});
    var header=hasHeader?rows[0]:null,data=hasHeader?rows.slice(1):rows;
    out.header=header;out.total=data.length;
    var width=Math.max.apply(null,rows.map(function(r){return r.length;})),emailCol=-1,top=0;
    for(var c=0;c<width;c++){
      var n=data.filter(function(r){return (r[c]||"").indexOf("@")>=0;}).length;
      if(n>top){top=n;emailCol=c;}
    }
    function find(re){if(!header)return -1;for(var i=0;i<header.length;i++)if(re.test(header[i].trim()))return i;return -1;}
    if(emailCol<0)emailCol=find(/e-?mail/i);
    var nameCol=find(/^(first[ _-]?name|given[ _-]?name|first|name|full[ _-]?name|contact([ _-]?name)?)$/i);
    var titleCol=find(/title|role|position|designation/i),companyCol=find(/company|organi[sz]ation|account|employer/i);
    out.cols={email:emailCol,name:nameCol,title:titleCol,company:companyCol};
    if(emailCol<0)return Object.assign(out,{verdict:"NO_EMAIL_COLUMN"});

    var targets=String(opts.titles||"").split(",").map(function(t){return t.trim().toLowerCase();}).filter(Boolean);
    out.fit=targets.length?(titleCol>=0?"checked":"no-title-column"):"not-given";
    var seen={},domains={},free=0;
    function bump(k){out.counts[k]=(out.counts[k]||0)+1;}
    data.forEach(function(r,i){
      var raw=(r[emailCol]||"").trim(),email=raw.toLowerCase(),problems=[];
      var at=email.lastIndexOf("@"),local=at>0?email.slice(0,at):"",domain=at>0?email.slice(at+1):"";
      if(!email){problems.push("No email address");bump("empty");}
      else if(!EMAIL.test(email)||/\.\./.test(email)){problems.push("Malformed address");bump("malformed");}
      else{
        if(TYPO[domain]||/\.(con|cmo|vom|comm|ocm)$/.test(domain)){problems.push("Typo domain"+(TYPO[domain]?" (did you mean "+TYPO[domain]+"?)":""));bump("typo");}
        if(ROLE[local.replace(/[0-9]+$/,"")]){problems.push("Role address");bump("role");}
        if(seen[email]){problems.push("Duplicate of row "+seen[email]);bump("duplicate");}
        else seen[email]=i+1;
        if(FREE[domain])free++;
        domains[domain]=(domains[domain]||0)+1;
      }
      if(out.fit==="checked"){
        var title=(r[titleCol]||"").toLowerCase();
        if(!targets.some(function(t){return title.indexOf(t)>=0;})){problems.push(title?"Title is outside your target":"No title");bump("title");}
      }
      var noName=nameCol>=0&&!(r[nameCol]||"").trim();
      if(noName)bump("noname");
      if(problems.length)out.wrong++;
      out.rows.push({n:i+1,cells:r,email:raw,title:titleCol>=0?(r[titleCol]||""):"",company:companyCol>=0?(r[companyCol]||""):"",problems:problems,noName:noName});
    });
    var valid=out.total-(out.counts.empty||0)-(out.counts.malformed||0);
    if(valid>=10&&free/valid>0.3)out.notes.push(Math.round(free*100/valid)+"% of the addresses are at free mail providers such as gmail.com. For a business list, that usually means personal addresses were scraped.");
    var crowded=Object.keys(domains).filter(function(d){return !FREE[d]&&domains[d]>=5;});
    if(crowded.length)out.notes.push(crowded.length+(crowded.length===1?" company has":" companies have")+" five or more contacts on the list ("+crowded.slice(0,3).join(", ")+(crowded.length>3?", …":"")+"). Sending to all of them at once looks like a blast from inside their mail system.");
    if(out.counts.noname)out.notes.push(out.counts.noname+(out.counts.noname===1?" row has":" rows have")+" no first name, so a \"Hi {first name}\" template would send \"Hi ,\".");

    /* The skill's rule: two or more wrong in ten is a pattern, so HOLD and fix the source. */
    var share=out.total?out.wrong/out.total:0;
    out.share=share;
    out.verdict=out.total<10?"INCONCLUSIVE":share>=0.2?"HOLD":"GO";
    var names={role:"shared role addresses",duplicate:"duplicates",malformed:"malformed addresses",typo:"typo domains",empty:"rows with no address",title:"titles outside your target"};
    var worst=Object.keys(names).filter(function(k){return out.counts[k];}).sort(function(a,b){return out.counts[b]-out.counts[a];})[0];
    out.pattern=worst?names[worst]:"";
    return out;
  }

  /* Ten rows picked at random for a person to read, as the skill asks. rand: () => 0..1. */
  function sample(result,rand){
    var idx=result.rows.map(function(_,i){return i;});
    for(var i=idx.length-1;i>0;i--){var j=Math.floor((rand||Math.random)()*(i+1)),t=idx[i];idx[i]=idx[j];idx[j]=t;}
    return idx.slice(0,10).sort(function(a,b){return a-b;}).map(function(i){return result.rows[i];});
  }
  function exportCsv(result,keepWrong){
    var rows=result.rows.filter(function(r){return keepWrong?r.problems.length:!r.problems.length;}).map(function(r){return keepWrong?r.cells.concat([r.problems.join("; ")]):r.cells;});
    if(result.header)rows.unshift(keepWrong?result.header.concat(["Finding"]):result.header);
    return toCsv(rows,result.delim);
  }

  var api={parse:parse,gate:gate,sample:sample,exportCsv:exportCsv};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.ListGate=api;
})(typeof self!=="undefined"?self:this);

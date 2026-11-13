/* Resume Check core: the part of recruiter-lens a script can do on pasted text. It counts and
   quotes; it does not judge a career. Runs in the browser and in Node. */
(function(root){
  var DUTY=/\b(responsible for|duties included?|tasked with|worked on|helped (?:to )?|assisted (?:with|in)|involved in|participated in|in charge of)/gi;
  var CLICHE=/\b(results?[- ](?:driven|oriented)|proven track record|passion(?:ate)? (?:for|about)|team player|detail[- ]oriented|hard[- ]working|self[- ]starter|go[- ]getter|think(?:ing)? outside the box|dynamic professional|highly motivated|motivated professional|excellent communication skills|strong work ethic|synergy)\b/gi;
  var BULLET=/^\s*(?:[-*•·▪◦‣–]|\d+[.)])\s+/;
  var STOP={};("a about above across after all also an and any are as at be been being both but by can could do does each for from has have having he her his how i if in into is it its just may might more most must my no not of on or other our out over own she should so some such than that the their them then there these they this those through to too under up us very was we were what when where which while who will with within would you your years year experience work working role team teams ability able strong including etc new using use used well plus per day days week based looking join company business people person candidate candidates ideal required requirements preferred responsibilities qualifications skills skill knowledge understanding excellent good great proven minimum least").split(" ").forEach(function(w){STOP[w]=1;});

  function words(text){return String(text).match(/[\p{L}\p{N}][\p{L}\p{N}'’+#./-]*/gu)||[];}
  function norm(w){return w.toLowerCase().replace(/[.,;:]+$/,"");}
  function stem(w){
    if(w.length>5&&/ing$/.test(w))return w.slice(0,-3);
    if(w.length>4&&/ies$/.test(w))return w.slice(0,-3)+"y";
    if(w.length>4&&/ed$/.test(w))return w.slice(0,-2);
    if(w.length>3&&/s$/.test(w)&&!/ss$/.test(w))return w.slice(0,-1);
    return w;
  }

  /* The terms a job ad leans on: words and two-word phrases it repeats, plus anything that
     looks like a tool or a qualification (capitals, digits or symbols mid-sentence). */
  function adTerms(ad,limit){
    var count={},shown={},order=[];
    function add(key,display,weight){
      if(!count[key]){count[key]=0;shown[key]=display;order.push(key);}
      count[key]+=weight;
    }
    String(ad).split(/[\n.;:!?()]+/).forEach(function(chunk){
      var ws=words(chunk).map(function(w){return w.replace(/[.,/]+$/,"");}).filter(Boolean),prev=null;
      ws.forEach(function(w,i){
        var low=norm(w),plain=/^[a-z][a-z'’-]*$/.test(low);
        var isStop=STOP[low]||low.length<2||!/[a-z]/.test(low);
        var tooly=!isStop&&(/[A-Z].*[A-Z]|[0-9+#/]/.test(w)||(i>0&&/^[A-Z]/.test(w)&&w.length>2));
        if(!isStop){
          if(tooly)add(low,w,2);
          else if(plain&&low.length>3)add(stem(low),low,1);
        }
        if(prev&&!isStop&&plain&&low.length>2)add(prev.low+" "+low,prev.low+" "+low,1.5);
        prev=(!isStop&&plain&&low.length>2)?{low:low}:null;
      });
    });
    return order.filter(function(k){return count[k]>=2;})
      .sort(function(a,b){return count[b]-count[a]||order.indexOf(a)-order.indexOf(b);})
      .slice(0,limit||16).map(function(k){return {key:k,term:shown[k]};});
  }
  function has(resumeLow,resumeStems,t){
    if(t.key.indexOf(" ")>=0)return resumeLow.indexOf(t.key)>=0||resumeLow.indexOf(t.term.toLowerCase())>=0;
    return !!resumeStems[t.key]||!!resumeStems[stem(t.term.toLowerCase())]||resumeLow.indexOf(t.term.toLowerCase())>=0&&/[^a-z]/.test(t.term.toLowerCase());
  }

  /* resume, ad: pasted text (ad may be empty). Returns
     {words, bullets, withNumber, findings[], passed[], skipped[], spans[], terms} where each
     finding is {level: FAIL|WARN, id, msg, why, fix, terms?}. */
  function check(resume,ad){
    var text=String(resume).replace(/^﻿/,"").replace(/\r\n?/g,"\n"),lines=text.split("\n");
    var out={words:words(text).length,bullets:0,withNumber:0,findings:[],passed:[],skipped:[],spans:[],terms:null,lines:lines};
    function fail(id,msg,why,fix,extra){out.findings.push(Object.assign({level:"FAIL",id:id,msg:msg,why:why,fix:fix},extra||{}));}
    function warn(id,msg,why,fix,extra){out.findings.push(Object.assign({level:"WARN",id:id,msg:msg,why:why,fix:fix},extra||{}));}

    /* contact details */
    var email=/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i.test(text),phone=/(?:\+?\d[\d\s().-]{7,}\d)/.test(text);
    if(!email)fail("no-email","No email address in the text","A screener who likes the resume has no way to reply. If your email sits in the page header or footer of the file, many applicant tracking systems skip it too.","Put your email and phone in the first lines of the body, not in a header or footer.");
    else if(!phone)warn("no-phone","No phone number in the text","Many recruiters call before they email.","Add a phone number beside your email, if you are happy to be called.");
    else out.passed.push("Email and phone are in the body");

    /* bullets, and how many carry a number */
    var bullets=[];
    lines.forEach(function(l,i){if(BULLET.test(l))bullets.push({line:i+1,text:l.replace(BULLET,"")});});
    if(bullets.length<3){
      bullets=[];
      lines.forEach(function(l,i){var n=words(l).length;if(n>=6&&n<=45&&!/:\s*$/.test(l)&&!/@/.test(l))bullets.push({line:i+1,text:l});});
    }
    var numbered=bullets.filter(function(b){return /\d/.test(b.text.replace(/\b(?:19|20)\d{2}\b/g,""))||/[%$€£₹]/.test(b.text);});
    out.bullets=bullets.length;out.withNumber=numbered.length;
    if(bullets.length>=3){
      var share=numbered.length/bullets.length;
      var why="Recruiters look for what changed because of you. \"Increased X by Y\" is read; \"responsible for X\" is skipped.";
      var fix="For each bullet ask: how many, how much, how fast, compared with what? Use only figures you can stand behind.";
      if(share<0.3)fail("few-numbers",numbered.length+" of "+bullets.length+" bullets carry a number",why,fix);
      else if(share<0.5)warn("some-numbers",numbered.length+" of "+bullets.length+" bullets carry a number",why,fix);
      else out.passed.push(numbered.length+" of "+bullets.length+" bullets carry a number");
    }else out.skipped.push({msg:"Numbers in bullets",why:"Fewer than three bullet lines were found, so there is nothing to count. Paste the experience section as well."});

    /* duty wording and stock phrases, marked in place */
    var duty=[],stock=[];
    lines.forEach(function(l,i){
      var m;DUTY.lastIndex=0;
      while((m=DUTY.exec(l))){var t=m[0].replace(/\s+$/,"");duty.push(t);out.spans.push({line:i+1,col:m.index,len:t.length,title:"Says a duty, not a result"});}
      CLICHE.lastIndex=0;
      while((m=CLICHE.exec(l))){stock.push(m[0]);out.spans.push({line:i+1,col:m.index,len:m[0].length,title:"A phrase most resumes use"});}
    });
    function uniq(a){var s={},o=[];a.forEach(function(x){var k=x.toLowerCase();if(!s[k]){s[k]=1;o.push(x);}});return o;}
    if(duty.length>=3)fail("duties",duty.length+" phrases describe a duty instead of a result","A duty says what the job was. A screener is looking for what you did with it.","Start the bullet with what you did and end it with what changed.",{terms:uniq(duty)});
    else if(duty.length)warn("duties",duty.length+(duty.length===1?" phrase describes":" phrases describe")+" a duty instead of a result","A duty says what the job was. A screener is looking for what you did with it.","Start the bullet with what you did and end it with what changed.",{terms:uniq(duty)});
    else out.passed.push("No duty wording such as \"responsible for\"");
    if(stock.length>=2)fail("stock",stock.length+" phrases could be on anyone's resume","These phrases appear on most resumes, so they tell the reader nothing about you and use up the lines that get read first.","Replace each with one fact only you can claim: a product, a market, a result.",{terms:uniq(stock)});
    else if(stock.length)warn("stock","1 phrase could be on anyone's resume","It appears on most resumes, so it tells the reader nothing about you.","Replace it with one fact only you can claim.",{terms:uniq(stock)});
    else out.passed.push("No stock phrases such as \"results-driven\"");

    /* first person */
    var me=(text.match(/\b(I|I'm|I've|my|me)\b/g)||[]).length;
    if(me>=3)warn("first-person","\"I\" or \"my\" appears "+me+" times","Resume bullets are usually written without a subject, and the pronouns take up the start of the line, where the verb should be.","Start bullets with the verb: \"Cut\", \"Built\", \"Led\".");

    /* sections an applicant tracking system looks for */
    var missing=[];
    if(!/^\s*(?:work |professional |relevant )?(?:experience|employment(?: history)?|work history)\s*:?\s*$/im.test(text))missing.push("Experience");
    if(!/^\s*education(?: (?:and|&) \w+)?\s*:?\s*$/im.test(text))missing.push("Education");
    if(!/^\s*(?:technical |core |key )?skills(?: (?:and|&) \w+)?\s*:?\s*$/im.test(text))missing.push("Skills");
    if(missing.length)warn("sections","No plain heading for: "+missing.join(", "),"Applicant tracking systems sort a resume into fields by its headings. A heading they do not recognise, or none, can mean the section is filed wrongly or dropped.","Use the plain words as headings on their own line: Experience, Education, Skills.");
    else out.passed.push("Experience, Education and Skills each have a plain heading");

    /* length */
    if(out.words>1000)warn("long",out.words.toLocaleString("en")+" words, which is likely more than two pages","Past two pages, the second half is rarely read on a first pass.","Cut older roles to a line each and keep the detail for the last ten years.");
    else if(out.words<150)out.skipped.push({msg:"Length",why:"Only "+out.words+" words were pasted, which is too little to judge. Paste the whole resume."});
    else out.passed.push(out.words.toLocaleString("en")+" words, within two pages");

    /* the job ad */
    if(ad&&String(ad).trim()){
      var terms=adTerms(ad,16),low=text.toLowerCase(),stems={};
      words(low).forEach(function(w){stems[stem(norm(w))]=1;stems[norm(w)]=1;});
      var found=[],lost=[];
      terms.forEach(function(t){(has(low,stems,t)?found:lost).push(t.term);});
      out.terms={total:terms.length,found:found,missing:lost};
      if(terms.length<4)out.skipped.push({msg:"Terms from the job ad",why:"The ad text is too short to find its repeated terms. Paste the whole ad."});
      else{
        var why2="Many applicant tracking systems rank resumes by how many of the ad's own terms appear. A person screening does the same thing by eye.";
        var fix2="Use the ad's wording for the things you have really done. Leave out the ones you have not; an interview finds them.";
        if(lost.length>terms.length/2)fail("ad-terms",lost.length+" of the "+terms.length+" terms the ad repeats are missing",why2,fix2,{terms:lost});
        else if(lost.length>=3)warn("ad-terms",lost.length+" of the "+terms.length+" terms the ad repeats are missing",why2,fix2,{terms:lost});
        else out.passed.push(found.length+" of the "+terms.length+" terms the ad repeats appear");
      }
    }else out.skipped.push({msg:"Terms from the job ad",why:"No job ad was pasted. Add one to see which of its terms your resume is missing."});

    out.skipped.push({msg:"Layout, columns, tables and fonts",why:"Pasted text has no layout. Two-column designs, tables and text boxes are what scramble a resume inside an applicant tracking system, and only the file shows them."});
    out.skipped.push({msg:"Gaps, short stints and career story",why:"Whether a gap or a move needs a line of explanation takes a reader. The recruiter-lens skill does that review."});
    return out;
  }

  var api={check:check,adTerms:adTerms};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.ResumeCheck=api;
})(typeof self!=="undefined"?self:this);

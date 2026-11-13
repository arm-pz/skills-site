/* Resume Check page: runs /resume/resume-core.js on the pasted text in the browser. The resume
   and the job ad are never sent anywhere; this file makes no network request. */
(function(){
  var T=window.Tool,R=window.ResumeCheck,$=function(id){return document.getElementById(id);};
  var form=$("form"),resume=$("resume"),ad=$("ad"),statusEl=$("status"),result=$("result");
  if(!form||!T||!R)return;
  var el=T.el;
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}

  function render(r){
    result.textContent="";
    var fails=r.findings.filter(function(f){return f.level==="FAIL";}),warns=r.findings.filter(function(f){return f.level==="WARN";});
    result.appendChild(el("p","verdict",fails.length
      ?T.plural(fails.length,"thing","things")+" would get this put down"+(warns.length?", and "+warns.length+" to look at.":".")
      :warns.length?"Nothing that sinks it. "+T.plural(warns.length,"thing","things")+" to look at."
      :"Nothing found by the script."));
    var facts=el("div","facts");
    function fact(v,k){var s=el("span");s.appendChild(el("b",null,v));s.appendChild(document.createTextNode(" "+k));facts.appendChild(s);}
    fact(r.words.toLocaleString("en"),"words");
    if(r.bullets>=3)fact(r.withNumber+" of "+r.bullets,"bullets carry a number");
    if(r.terms&&r.terms.total>=4)fact(r.terms.found.length+" of "+r.terms.total,"repeated terms from the ad appear");
    result.appendChild(facts);

    if(r.spans.length){
      result.appendChild(T.markedDraft(r.lines,r.spans,"Your resume with each phrase marked"));
      var legend=el("p","legend");legend.appendChild(el("mark",null,"marked"));
      legend.appendChild(document.createTextNode(" a phrase that states a duty, or one that most resumes use."));
      result.appendChild(legend);
    }
    var list=el("ul","findings");
    fails.concat(warns).forEach(function(f){list.appendChild(T.finding(f.level,f.msg,{terms:f.terms,why:f.why,fix:f.fix}));});
    r.skipped.forEach(function(s){list.appendChild(T.finding("NOT CHECKED",s.msg,{why:s.why}));});
    result.appendChild(list);
    if(r.passed.length){var p=el("p","passed");p.appendChild(el("b",null,"Passed: "));p.appendChild(document.createTextNode(r.passed.join(" · ")));result.appendChild(p);}
    result.appendChild(el("p","passed","These are counts and quotes, not a judgement of you or your career. A script cannot tell whether a number is impressive or whether a term from the ad is true of you."));
    result.appendChild(T.upsell("Want the full review, or the rewrite?","recruiter-lens reviews the whole resume the way a recruiter screens it, and applicant-kit rewrites each bullet for the job using only what is true. Both are free, open skills for your own agent.","See the job-search workflow","/workflows/land-a-job/"));
    result.hidden=false;T.reveal(result);
  }

  form.addEventListener("submit",function(e){
    e.preventDefault();
    if(!resume.value.trim()){say("Paste your resume as text first.",true);resume.focus();return;}
    if(resume.value.length+ad.value.length>400000){say("That is too much text. Paste one resume and one job ad.",true);return;}
    say("");render(R.check(resume.value,ad.value));
  });
  $("sample").addEventListener("click",function(){
    resume.value="[YOUR NAME]\nProduct Manager · [CITY] · name@example.com · +1 555 010 0199\n\nSummary\nResults-driven professional with a passion for building products that users love and a proven track record of cross-functional leadership.\n\nExperience\nProduct Manager, [COMPANY] · 2022 to now\n- Responsible for the checkout roadmap and working with engineering\n- Helped improve onboarding for new customers\n- Cut checkout drop-off from 31% to 22% in two quarters\n- Worked on pricing experiments with the growth team\n\nAssociate Product Manager, [COMPANY] · 2019 to 2022\n- Assisted with user research for the mobile app\n- Shipped saved carts, used by 40,000 customers in the first month\n\nEducation\nBSc Computer Science, [UNIVERSITY]\n";
    ad.value="Senior Product Manager, B2B SaaS\n\nWe are looking for a product manager to own retention for our B2B SaaS platform. You will run A/B testing on onboarding and pricing, write SQL to answer your own questions, and work with engineering and design.\n\nRequirements: 4+ years in B2B SaaS product management. Strong SQL. A record of improving retention. Experience with A/B testing and pricing experiments. Clear writing for stakeholders; you will present to stakeholders monthly.";
    form.requestSubmit?form.requestSubmit():form.dispatchEvent(new Event("submit",{cancelable:true}));
  });
})();

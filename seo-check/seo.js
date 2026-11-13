/* SEO Check page: reads the page source you paste with the browser's own HTML parser and runs
   the single-page checks from seo-crawl. The source is parsed as an inert document: its scripts
   do not run, nothing in it is loaded, and it is never sent anywhere. */
(function(){
  var T=window.Tool,$=function(id){return document.getElementById(id);};
  var form=$("form"),src=$("src"),url=$("url"),statusEl=$("status"),result=$("result");
  if(!form||!T)return;
  var el=T.el;
  function say(msg,isErr){statusEl.textContent=msg||"";statusEl.className=isErr?"err":"";}
  function len(s){return Array.from(s).length;}
  function clip(s,n){var a=Array.from(s);return a.length>n?a.slice(0,n-1).join("").replace(/\s+\S*$/,"")+"…":s;}
  function attr(node,name){return (node.getAttribute(name)||"").trim();}
  function tidy(s){return String(s||"").replace(/\s+/g," ").trim();}
  function normUrl(u){try{var x=new URL(u);return (x.origin+x.pathname).replace(/\/+$/,"").toLowerCase();}catch(e){return "";}}

  function check(html,pageUrl){
    var doc=new DOMParser().parseFromString(html,"text/html");
    var out={fails:[],warns:[],passed:[],skipped:[],title:"",desc:"",url:pageUrl};
    function fail(msg,o){out.fails.push([msg,o]);}
    function warn(msg,o){out.warns.push([msg,o]);}
    function q(sel){return [].slice.call(doc.querySelectorAll(sel));}

    /* indexability */
    var robots=q('meta[name="robots" i],meta[name="googlebot" i]').map(function(m){return attr(m,"content");}).join(", ");
    if(/noindex|none/i.test(robots))fail("The page tells search engines not to index it",{evidence:'<meta name="robots" content="'+robots+'">',why:"With noindex set, the page is dropped from search results however good the rest is.",fix:"Remove the tag, unless you mean to keep this page out of search. It is often left over from a staging build."});
    else out.passed.push("No noindex in the meta robots tag");

    /* title */
    var titles=q("head title"),title=tidy(titles[0]&&titles[0].textContent);out.title=title;
    if(!title)fail("No title",{why:"The title is the headline of your search result and the strongest on-page signal of what the page is about.",fix:"Add a <title> that names the page's subject first."});
    else{
      if(titles.length>1)warn("Two or more <title> tags",{why:"Search engines use the first and ignore the rest, which may not be the one you meant.",fix:"Keep one."});
      var n=len(title);
      if(n>60)warn("Title is "+n+" characters and will likely be cut off",{evidence:title,why:"Search results show about 60 characters.",fix:"Put the page's subject in the first half, and the brand last."});
      else if(n<15)warn("Title is only "+n+" characters",{evidence:title,why:"A very short title rarely says what the page is about or matches what people search for.",fix:"Name the subject and who it is for."});
      else out.passed.push("Title is "+n+" characters");
    }

    /* meta description */
    var descs=q('meta[name="description" i]'),desc=tidy(descs[0]&&attr(descs[0],"content"));out.desc=desc;
    if(!desc)warn("No meta description",{why:"Without one the search engine picks its own text from the page, which is often a menu or a cookie notice.",fix:"Add one or two sentences that say what the visitor gets."});
    else{
      var dn=len(desc);
      if(dn>160)warn("Meta description is "+dn+" characters and will be cut off",{why:"Search results show about 155 to 160 characters.",fix:"Say the main thing in the first 120."});
      else if(dn<50)warn("Meta description is only "+dn+" characters",{evidence:desc,why:"It leaves most of the space in your search result empty.",fix:"Use the room: what the page offers, and for whom."});
      else out.passed.push("Meta description is "+dn+" characters");
    }

    /* canonical */
    var canon=q('link[rel~="canonical" i]').map(function(l){return attr(l,"href");}).filter(Boolean);
    if(!canon.length)warn("No canonical tag",{why:"When the same page is reachable at more than one address (with and without www, with tracking parameters), the canonical tag says which one counts.",fix:'Add <link rel="canonical" href="…"> with the page\'s own full address.'});
    else if(canon.length>1&&canon.some(function(c){return c!==canon[0];}))fail("Two canonical tags that disagree",{evidence:canon.join("\n"),why:"Conflicting canonicals are ignored, so duplicates compete with each other.",fix:"Keep one."});
    else if(pageUrl&&normUrl(pageUrl)&&/^https?:/i.test(canon[0])&&normUrl(canon[0])!==normUrl(pageUrl))warn("The canonical tag points to a different address",{evidence:canon[0],why:"This tells search engines to index that address instead of this page. That is right for a duplicate and wrong for a page you want ranked.",fix:"If this page should rank, point the canonical at its own address."});
    else if(!/^https?:/i.test(canon[0]))warn("The canonical address is relative",{evidence:canon[0],why:"A relative canonical is easy to resolve wrongly.",fix:"Use the full address, starting with https://."});
    else out.passed.push("One canonical tag");

    /* headings */
    var h1=q("h1").map(function(h){return tidy(h.textContent);});
    if(!h1.length)fail("No H1 heading",{why:"The H1 tells a reader and a search engine what the page is about. A page built only from styled divs has none.",fix:"Mark the page's main heading up as <h1>."});
    else if(h1.length>1)warn(h1.length+" H1 headings",{evidence:h1.slice(0,5).join("\n"),why:"With several, none of them names the page.",fix:"Keep the one that names the page and make the others <h2>."});
    else out.passed.push("One H1");

    /* language and viewport */
    if(!attr(doc.documentElement,"lang"))warn("No language on the <html> tag",{why:"Search engines and screen readers use it to tell which language the page is in.",fix:'Add lang, for example <html lang="en">.'});
    else out.passed.push("Language is set ("+attr(doc.documentElement,"lang")+")");
    if(!q('meta[name="viewport" i]').length)warn("No viewport tag",{why:"Without it a phone shows the desktop layout shrunk down, and search indexing is done with a phone-sized view.",fix:'Add <meta name="viewport" content="width=device-width, initial-scale=1">.'});
    else out.passed.push("Viewport tag is present");

    /* social preview */
    var og=["og:title","og:description","og:image"].filter(function(p){return !q('meta[property="'+p+'" i],meta[name="'+p+'" i]').some(function(m){return attr(m,"content");});});
    if(og.length)warn("Missing sharing tags: "+og.join(", "),{why:"These decide how the link looks when it is shared in chat and on social sites. They do not affect ranking.",fix:"Add the missing Open Graph tags. The image should be a full https address."});
    else out.passed.push("Open Graph title, description and image");

    /* images */
    var imgs=q("img"),noAlt=imgs.filter(function(i){return !i.hasAttribute("alt");});
    if(noAlt.length)warn(noAlt.length+" of "+imgs.length+" images have no alt attribute",{evidence:noAlt.slice(0,4).map(function(i){return attr(i,"src")||"(no src)";}).join("\n"),why:"Alt text is how image search and screen readers know what a picture shows.",fix:'Describe each meaningful image. Give purely decorative ones an empty alt="".'});
    else if(imgs.length)out.passed.push("All "+imgs.length+" images have an alt attribute");

    /* structured data */
    var ld=q('script[type="application/ld+json" i]'),bad=0,types=[];
    ld.forEach(function(s){
      try{
        var data=JSON.parse(s.textContent);
        (Array.isArray(data)?data:(data["@graph"]||[data])).forEach(function(d){if(d&&d["@type"])types.push([].concat(d["@type"]).join("/"));});
      }catch(e){bad++;}
    });
    if(bad)fail(bad+" structured data "+(bad===1?"block does":"blocks do")+" not parse",{why:"A JSON-LD block with a syntax error is ignored whole.",fix:"Run the block through a JSON validator; a trailing comma is the usual cause."});
    else if(ld.length)out.passed.push("Structured data parses"+(types.length?" ("+types.slice(0,5).join(", ")+")":""));
    else out.skipped.push(["Structured data","None in the pasted source. Not every page needs it, and data added by JavaScript would not show here."]);

    /* links that go nowhere */
    var dead=q("a").filter(function(a){var h=attr(a,"href");return !a.hasAttribute("href")||h===""||h==="#"||/^javascript:/i.test(h);});
    if(dead.length>=3)warn(dead.length+" links have no real address",{why:"A link with href=\"#\" or a script in it cannot be followed by a crawler, so the page behind it may never be found.",fix:"Use real addresses in href, and attach any script to the link separately."});

    /* pages that are built in the browser */
    var bodyText=tidy(doc.body?doc.body.textContent:"");
    if(q("script").length&&len(bodyText)<200)out.skipped.push(["Everything above, in part","The pasted source has almost no text, so this page is probably built by JavaScript in the browser. Paste the rendered HTML instead: in the browser's developer tools, right-click the <html> element and copy its outer HTML."]);

    out.skipped.push(["Status code, redirects and the X-Robots-Tag header","These are sent by the server and are not in the page source."]);
    out.skipped.push(["robots.txt and sitemap coverage","These live at the site level. The seo-crawl skill reads them and crawls the rest of the site."]);
    out.skipped.push(["Page speed","Speed needs a real browser run. The pre-ship-performance-audit skill does that."]);
    return out;
  }

  function render(r){
    result.textContent="";
    var f=r.fails.length,w=r.warns.length;
    result.appendChild(el("p","verdict",f||w
      ?(f?T.plural(f,"thing","things")+" to fix":"Nothing broken")+(w?", "+w+" to look at.":".")
      :"Nothing found on this page."));
    var facts=el("div","facts"),s=el("span");
    s.appendChild(el("b",null,String(r.passed.length)));s.appendChild(document.createTextNode(" checks passed"));facts.appendChild(s);
    var s2=el("span");s2.appendChild(el("b",null,String(r.skipped.length)));s2.appendChild(document.createTextNode(" not checked, and not counted as passes"));facts.appendChild(s2);
    result.appendChild(facts);

    var serp=el("div","serp");
    serp.appendChild(el("p","k","How it may look in search"));
    var shown="your-site.com";
    try{if(r.url){var u=new URL(r.url);shown=u.hostname+u.pathname.replace(/\/$/,"").split("/").join(" › ");}}catch(e){}
    serp.appendChild(el("p","u",shown));
    serp.appendChild(el("p","t",r.title?clip(r.title,60):"(no title)"));
    serp.appendChild(el("p","d",r.desc?clip(r.desc,158):"No meta description, so the search engine will choose its own text from the page."));
    result.appendChild(serp);

    var list=el("ul","findings");
    r.fails.forEach(function(x){list.appendChild(T.finding("FAIL",x[0],x[1]));});
    r.warns.forEach(function(x){list.appendChild(T.finding("WARN",x[0],x[1]));});
    r.skipped.forEach(function(x){list.appendChild(T.finding("NOT CHECKED",x[0],{why:x[1]}));});
    result.appendChild(list);
    if(r.passed.length){var p=el("p","passed");p.appendChild(el("b",null,"Passed: "));p.appendChild(document.createTextNode(r.passed.join(" · ")));result.appendChild(p);}
    result.appendChild(T.upsell("One page is a start. A site has hundreds.","seo-crawl is the free, open skill behind this page. Your own agent crawls the whole site, reads robots.txt and the sitemap, and returns findings with evidence.","Get the skill, free","/seo-crawl/"));
    result.hidden=false;T.reveal(result);
  }

  form.addEventListener("submit",function(e){
    e.preventDefault();
    var html=src.value;
    if(!html.trim()){say("Paste the page source first. On the page, press Ctrl+U (Cmd+Option+U on a Mac), select all and copy.",true);src.focus();return;}
    if(!/<\w+[\s>]/.test(html)){say("That does not look like HTML. Paste the page's source, not its visible text.",true);return;}
    if(html.length>3000000){say("That is over three million characters. Paste one page at a time.",true);return;}
    var pageUrl=url.value.trim();
    if(pageUrl&&!/^https?:\/\//i.test(pageUrl))pageUrl="https://"+pageUrl;
    say("");render(check(html,pageUrl));
  });
  $("sample").addEventListener("click",function(){
    url.value="example.com/pricing";
    src.value='<!doctype html>\n<html>\n<head>\n<title>Pricing and Plans for Teams of Every Size and Every Kind of Budget | Example</title>\n<meta name="robots" content="noindex">\n<link rel="canonical" href="/pricing">\n<script type="application/ld+json">{"@type":"Product","name":"Example",}</script>\n</head>\n<body>\n<h1>Pricing</h1>\n<h1>Simple plans for every team</h1>\n<p>Pick the plan that fits. Every plan includes support, and you can change or cancel at any time from your account page without talking to anyone.</p>\n<p>Starter is for one person and one project. Team adds shared workspaces and roles for up to twenty people. Business adds single sign-on, an audit log and a named contact for support questions.</p>\n<img src="/img/plans.png">\n<img src="/img/logo.png" alt="Example">\n<a href="#">Start free</a>\n</body>\n</html>\n';
    form.requestSubmit?form.requestSubmit():form.dispatchEvent(new Event("submit",{cancelable:true}));
  });
})();

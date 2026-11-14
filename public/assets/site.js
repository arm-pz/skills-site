/* Skillsmith by Caffeinity: copy buttons, the skill filter and the proof tabs.
   Every page works without it; this only adds the conveniences. The last lines fetch
   /assets/motion.js (built from tools/fx), which adds the scroll motion and the homepage forge. */
(function(){
  var live=document.createElement('span');
  live.className='sr-only';live.setAttribute('role','status');live.setAttribute('aria-live','polite');
  document.body.appendChild(live);

  [].forEach.call(document.querySelectorAll('[data-copy]'),function(b){
    var label=b.querySelector('.copy')||b,idle=label.textContent,timer;
    b.addEventListener('click',function(){
      var text=b.getAttribute('data-copy');
      function done(){
        b.classList.add('is-done');label.textContent='Copied';live.textContent='Copied to clipboard.';
        clearTimeout(timer);
        timer=setTimeout(function(){b.classList.remove('is-done');label.textContent=idle;live.textContent='';},1600);
      }
      function fallback(){
        var source=b.querySelector('span:not(.copy)')||document.getElementById(b.getAttribute('data-copy-from')||'');
        if(!source)return;
        var r=document.createRange();r.selectNodeContents(source);
        var s=window.getSelection();s.removeAllRanges();s.addRange(r);
        live.textContent='Clipboard unavailable. The command is selected; press Ctrl+C.';
      }
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,fallback);}
      else{fallback();}
    });
  });

  var q=document.getElementById('q');
  if(q){
    var status=document.getElementById('find-status'),empty=document.getElementById('empty');
    var cards=[].slice.call(document.querySelectorAll('.skill')),groups=[].slice.call(document.querySelectorAll('.sk-group'));
    var filter=function(){
      var terms=q.value.toLowerCase().split(/\s+/).filter(Boolean),shown=0;
      cards.forEach(function(c){
        var hay=c.getAttribute('data-search'),on=terms.every(function(t){return hay.indexOf(t)!==-1;});
        c.hidden=!on;if(on)shown++;
      });
      groups.forEach(function(g){g.hidden=!g.querySelector('.skill:not([hidden])');});
      if(empty)empty.hidden=shown>0;
      if(status)status.textContent=terms.length?(shown+' of '+cards.length+(shown===1?' matches':' match')):'';
    };
    q.addEventListener('input',filter);
    document.addEventListener('keydown',function(e){
      if(e.key==='/'&&!/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)&&!e.metaKey&&!e.ctrlKey){e.preventDefault();q.focus();}
      if(e.key==='Escape'&&document.activeElement===q&&q.value){q.value='';filter();}
    });
    if(q.value)filter();
  }

  var tabs=[].slice.call(document.querySelectorAll('.tabs [role="tab"]'));
  function show(i,focus){
    tabs.forEach(function(t,j){
      var on=i===j;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;
      document.getElementById(t.getAttribute('aria-controls')).hidden=!on;
    });
    if(focus){tabs[i].focus();tabs[i].scrollIntoView({block:'nearest',inline:'nearest'});}
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){show(i);});
    t.addEventListener('keydown',function(e){
      var k={ArrowRight:1,ArrowLeft:-1}[e.key];
      if(k){e.preventDefault();show((i+k+tabs.length)%tabs.length,true);}
    });
  });
  if(tabs.length)show(0);

  var me=document.currentScript,motion=document.createElement('script');
  var ver=me&&me.src&&me.src.indexOf('?')>-1?me.src.slice(me.src.indexOf('?')):'';
  motion.type='module';motion.src=(me&&me.src?me.src.replace(/site\.js.*$/,''):'/assets/')+'motion.js'+ver;
  document.head.appendChild(motion);
})();

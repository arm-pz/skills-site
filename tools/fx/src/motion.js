/* Scroll choreography for every page that loads /assets/site.js. Nothing here carries content:
   with this file missing, blocked or switched off by prefers-reduced-motion, pages read the same.
   Each hero also gets an agent session (rig.js) and a rippling floor (forge.js, three.js),
   fetched as its own file only when it will show. */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { HOME_RUNS, pageRuns, mountBeside, play, rest } from './rig.js';

gsap.registerPlugin(ScrollTrigger);

const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;
const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => [].slice.call((el || document).querySelectorAll(s));
const OUT = 'expo.out';

/* wrap each word of a heading so it can rise out of its own mask; <em> and links are kept */
function words(el) {
  const out = [];
  (function walk(node) {
    [].slice.call(node.childNodes).forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'), i = document.createElement('span');
          w.className = 'w'; i.textContent = part; w.appendChild(i); frag.appendChild(w); out.push(i);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1) walk(n);
    });
  })(el);
  return out;
}

/* ---- the hero: an agent session over a rippling floor ---- */
const state = { p: 0, px: 0, py: 0, ping: 0, ox: 0.4, oy: -0.3 };
const stage = $('.stage');
let canvas = $('#forge'), hero = $('.hero'), rig = $('[data-rig]'), runs = rig ? HOME_RUNS : null;
if (!rig) {
  hero = $('.sk-hero') || $('.page-hero') || $('.lost');
  runs = hero ? pageRuns() : null;
  if (runs && runs.length) {
    rig = mountBeside(hero);
    const fx = document.createElement('div');
    fx.className = 'hero-fx';
    fx.setAttribute('aria-hidden', 'true');
    canvas = document.createElement('canvas');
    fx.appendChild(canvas);
    hero.insertBefore(fx, hero.firstChild);
  } else rig = null;
}
if (rig) rest(rig, runs[0]);

function webgl() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); }
  catch (e) { return false; }
}
if (canvas && webgl()) {
  import('./forge.js').then((m) => {
    if (m.mount(canvas, state, { still: reduced, page: !stage })) canvas.parentNode.classList.add('is-live');
  }).catch(() => {});
}

if (!reduced) {
  root.classList.add('fx-on');

  /* nav: glass once the page moves, tucked away on the way down */
  const nav = $('.home .nav');
  if (nav) {
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate(self) {
        const y = self.scroll();
        nav.classList.toggle('is-stuck', y > 24);
        nav.classList.toggle('is-away', y > innerHeight * 0.6 && self.direction === 1);
      },
    });
  }

  /* hero entrance */
  const h1 = $('.hero h1');
  if (h1) {
    const parts = words(h1);
    gsap.set(h1, { opacity: 1 });
    const tl = gsap.timeline({ defaults: { ease: OUT }, delay: 0.15 });
    tl.from(parts, { yPercent: 115, rotate: 4, duration: 1.25, stagger: 0.07 })
      .fromTo('.hero [data-r]', { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 1, stagger: 0.09 }, 0.45);

    /* the claim drifts up and out slower than the page: three depths, one scroll */
    const leave = { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true };
    gsap.to('.hero h1', { yPercent: -18, ease: 'none', scrollTrigger: leave });
    gsap.to('.hero .eyebrow,.hero .lead,.hero-act', { yPercent: -60, opacity: 0, ease: 'none', scrollTrigger: { ...leave, end: '60% top' } });
    gsap.to('.hero-rail', { opacity: 0, ease: 'none', scrollTrigger: { ...leave, end: '25% top' } });
  }

  /* count the numbers up */
  const stats = $('.hero .stats');
  if (stats) {
    const html = stats.textContent.split(' · ').map((part) =>
      '<span class="stat">' + part.replace(/^(\d+)\s*/, '<b data-n="$1">$1</b>') + '</span>').join('');
    stats.setAttribute('aria-label', stats.textContent);
    stats.innerHTML = html;
    $$('b[data-n]', stats).forEach((b) => {
      const end = +b.getAttribute('data-n'), o = { v: 0 };
      gsap.to(o, { v: end, duration: 1.8, delay: 0.9, ease: 'power3.out', onUpdate() { b.textContent = Math.round(o.v); } });
    });
  }

  /* scroll progress drives the forge: 0 at the claim, 1 once the brew menu holds the screen */
  if (stage) {
    ScrollTrigger.create({
      trigger: stage, start: 'top top', end: () => '+=' + innerHeight * 1.15, scrub: true,
      onUpdate(self) { state.p = self.progress; },
    });
    if (fine) addEventListener('pointermove', (e) => { state.px = (e.clientX / innerWidth) * 2 - 1; state.py = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });
    $$('.stage [data-copy]').forEach((b) => b.addEventListener('click', () => { state.ping = 1; }));
  }

  /* the agent session replays; on the homepage the floor follows the stage, elsewhere the hero */
  if (rig) play(rig, runs, { state, hero, fine, canvas, loop: true, started: !stage, delay: stage ? 2600 : 900, tiltY: stage ? -16 : -12 });
  if (!stage && hero) {
    ScrollTrigger.create({ trigger: hero, start: 'top top', end: 'bottom top', scrub: true, onUpdate(self) { state.p = self.progress; } });
    if (fine) addEventListener('pointermove', (ev) => { state.px = (ev.clientX / innerWidth) * 2 - 1; state.py = (ev.clientY / innerHeight) * 2 - 1; }, { passive: true });
  }

  /* the agents strip: loops on its own, leans into the scroll */
  const track = $('.marquee-track');
  if (track) {
    track.innerHTML += track.innerHTML;
    track.parentNode.classList.add('is-js');
    const loop = gsap.to(track, { xPercent: -50, duration: 36, ease: 'none', repeat: -1 });
    let settle;
    ScrollTrigger.create({
      trigger: track, start: 'top bottom', end: 'bottom top',
      onUpdate(self) {
        const v = gsap.utils.clamp(-6, 6, self.getVelocity() / 260);
        gsap.to(loop, { timeScale: (v < 0 ? -1 : 1) * (1 + Math.abs(v)), duration: 0.3, overwrite: true });
        gsap.to(track, { skewX: -v * 1.6, duration: 0.4, overwrite: 'auto' });
        clearTimeout(settle);
        settle = setTimeout(() => { gsap.to(loop, { timeScale: 1, duration: 1.2 }); gsap.to(track, { skewX: 0, duration: 0.8 }); }, 140);
      },
    });
  }

  /* headings below the fold rise word by word; everything else fades up in batches */
  $$('main h1, .page-hero h1, .sk-hero h1, .lost h1, section h2, .band h2, .contact h2').forEach((h) => {
    if (h.closest('.hero') || h.closest('.flow, .skill, .sk-head')) return;
    const parts = words(h);
    gsap.from(parts, { yPercent: 115, duration: 1.1, ease: OUT, stagger: 0.045, scrollTrigger: { trigger: h, start: 'top 88%', once: true } });
  });

  const rise = ['.sub', '.menu-sub', '.menu-head .text-link', '.brew', '.shell', '.inst', '.band p', '.band .btn',
    '.page-hero .crumbs', '.page-hero .lead', '.page-hero .stats', '.sk-hero .lead', '.install-line', '.facts',
    '.purpose .body', '.uses > *', '.files', '.related li', '.source', '.find', '.sk-head', '.skill', '.flow', '.router',
    '.step', '.pair', '.console', '.others li', '.plan', '.steps li', '.faq details', '.contact p', '.contact .mail', '.cta',
    '.lost .lead', '.lost-links li', '.close-grid p', '.aside', '.note', '.alt', '.work-line'];
  const items = $$(rise.join(',')).filter((el) => !el.closest('.hero'));
  gsap.set(items, { opacity: 0, y: 28 });
  ScrollTrigger.batch(items, {
    start: 'top 92%', once: true,
    onEnter: (batch) => gsap.to(batch, { opacity: 1, y: 0, duration: 0.9, ease: OUT, stagger: 0.06, overwrite: true, clearProps: 'transform' }),
  });

  /* flagships: each card settles back as the next one slides over it */
  const flags = $$('.flag');
  if (flags.length && matchMedia('(min-width:761px)').matches) {
    flags.forEach((card, i) => {
      gsap.from(card, { y: 90, opacity: 0, duration: 1.1, ease: OUT, scrollTrigger: { trigger: card, start: 'top 96%', once: true } });
      const next = flags[i + 1];
      if (next) gsap.to(card, { scale: 0.95 - (flags.length - 2 - i) * 0.025, ease: 'none',
        scrollTrigger: { trigger: next, start: 'top bottom', end: 'top ' + (92 + (i + 1) * 18) + 'px', scrub: true } });
    });
  }

  /* parallax: the big marks move against the scroll */
  if ($('.band-mark')) gsap.fromTo('.band-mark', { yPercent: 8 }, { yPercent: -14, ease: 'none', scrollTrigger: { trigger: '.band', start: 'top bottom', end: 'bottom top', scrub: true } });
  if ($('.proof')) gsap.fromTo('.proof', { '--py': '0px' }, { '--py': '200px', ease: 'none', scrollTrigger: { trigger: '.proof', start: 'top bottom', end: 'bottom top', scrub: true } });

  /* the wordmark rises letter by letter as the page ends */
  const mark = $('.wordmark');
  if (mark) {
    const dot = mark.querySelector('b'), text = mark.firstChild;
    if (text && text.nodeType === 3) {
      const frag = document.createDocumentFragment();
      text.textContent.split('').forEach((c) => { const s = document.createElement('span'); s.className = 'ch'; s.textContent = c; frag.appendChild(s); });
      mark.replaceChild(frag, text);
      if (dot) dot.classList.add('ch');
    }
    gsap.from($$('.ch', mark), { yPercent: 105, ease: 'power3.out', stagger: 0.06,
      scrollTrigger: { trigger: mark, start: 'top 98%', end: 'bottom bottom', scrub: 0.6 } });
  }

  /* pointer: cards are lit from where you are, the main buttons lean toward you */
  if (fine) {
    $$('.skill,.flow,.plan,.inst,.flag').forEach((card) => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      }, { passive: true });
      card.addEventListener('pointerleave', () => { card.style.setProperty('--mx', '-999px'); });
    });
    $$('.band .btn,.nav .btn,.cta .btn').forEach((b) => {
      const x = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3.out' }), y = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3.out' });
      b.addEventListener('pointermove', (e) => { const r = b.getBoundingClientRect(); x((e.clientX - r.left - r.width / 2) * 0.3); y((e.clientY - r.top - r.height / 2) * 0.4); });
      b.addEventListener('pointerleave', () => { x(0); y(0); });
    });
  }

  /* layout shifts after fonts and the filter change where things start */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => ScrollTrigger.refresh());
  const q = $('#q');
  if (q) q.addEventListener('input', () => { gsap.set('.skill,.sk-head', { opacity: 1, y: 0 }); ScrollTrigger.refresh(); });
}

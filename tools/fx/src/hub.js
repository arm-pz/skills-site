/* /checks/, the hub of free tools. Depth for a page about checking: the picker is a card you can
   turn, each tool card runs its sample result as it scrolls in, the three steps fill in as you
   read them, and the floor under the hero (forge.js) ripples from the row you point at.
   Called by motion.js only when motion is allowed; the page reads the same without it. */
const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => [].slice.call((el || document).querySelectorAll(s));
const OUT = 'expo.out';

/* a card that leans toward the pointer and is lit from it */
function tilt(gsap, card, max) {
  gsap.set(card, { transformPerspective: 1000 });
  const rx = gsap.quickTo(card, 'rotationX', { duration: 0.6, ease: 'power3.out' });
  const ry = gsap.quickTo(card, 'rotationY', { duration: 0.6, ease: 'power3.out' });
  card.addEventListener('pointermove', (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
    ry((x - 0.5) * 2 * max); rx(-(y - 0.5) * 2 * max);
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });
  card.addEventListener('pointerleave', () => { rx(0); ry(0); card.style.setProperty('--mx', '-999px'); });
}

/* count a number inside its own text, keeping whatever surrounds it ("$19", "3 of 11") */
function count(gsap, el, from, opts) {
  const node = [].find.call(el.childNodes, (n) => n.nodeType === 3 && /\d/.test(n.textContent));
  if (!node) return;
  const text = node.textContent, m = text.match(/\d+/), to = +m[0], o = { v: from };
  const paint = () => { node.textContent = text.replace(/\d+/, Math.round(o.v)); };
  paint();
  return gsap.to(o, Object.assign({ v: to, duration: 1.4, ease: 'power3.out', onUpdate: paint }, opts));
}

/* each sample result plays once: the verdict lands, the marks sweep in, the route draws */
function runDemo(gsap, card) {
  const tl = gsap.timeline({ delay: 0.35 });
  const lvls = $$('.demo .lvl', card), marks = $$('.demo mark', card), stat = $('.demo-stat b', card);
  const gate = $('.demo-gate', card), route = $$('.demo-route > *', card), terms = $$('.demo-terms code', card);
  if (lvls.length) tl.fromTo(lvls, { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2.4)', stagger: 0.22 }, 0);
  if (marks.length) tl.fromTo(marks, { backgroundSize: '0% 100%' }, { backgroundSize: '100% 100%', duration: 0.5, ease: 'power2.out', stagger: 0.24 }, 0);
  if (stat) tl.add(count(gsap, stat, 0, { duration: 1.1 }), 0);
  if (terms.length) tl.fromTo(terms, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.12 }, 0.5);
  if (gate) tl.fromTo(gate, { scale: 1.25, rotate: -4, opacity: 0 }, { scale: 1, rotate: 0, opacity: 1, duration: 0.55, ease: 'back.out(2)' }, 0);
  if (route.length) tl.fromTo(route, { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.4, stagger: 0.16 }, 0);
  tl.fromTo($$('.st', card), { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.45, ease: 'power3.out', stagger: 0.1 }, 0.3);
}

export function hub({ gsap, ScrollTrigger, state, fine, canvas }) {
  const hero = $('.hub-hero'), picker = $('.picker'), wide = matchMedia('(min-width:1021px)').matches;

  /* ---- hero: the picker arrives turned, then follows the pointer ---- */
  if (picker) {
    const rows = $$('li', picker);
    if (fine && wide) gsap.set(picker, { transformPerspective: 1100 });
    const rest = fine && wide ? { y: -7, x: 3 } : { y: 0, x: 0 };
    gsap.fromTo(picker, { opacity: 0, y: 70, rotationY: rest.y - 26, rotationX: rest.x + 8 },
      { opacity: 1, y: 0, rotationY: rest.y, rotationX: rest.x, duration: 1.5, delay: 0.25, ease: OUT });
    gsap.fromTo(rows, { opacity: 0, x: 28 }, { opacity: 1, x: 0, duration: 0.9, delay: 0.7, ease: OUT, stagger: 0.07 });
    if (fine && wide) {
      const rx = gsap.quickTo(picker, 'rotationX', { duration: 0.9, ease: 'power3.out' });
      const ry = gsap.quickTo(picker, 'rotationY', { duration: 0.9, ease: 'power3.out' });
      let ready = false;
      setTimeout(() => { ready = true; }, 1800);
      hero.addEventListener('pointermove', (e) => {
        if (!ready) return;
        const r = picker.getBoundingClientRect();
        ry(rest.y + gsap.utils.clamp(-1, 1, (e.clientX - r.left - r.width / 2) / innerWidth * 2) * 10);
        rx(rest.x - gsap.utils.clamp(-1, 1, (e.clientY - r.top - r.height / 2) / innerHeight * 2) * 8);
        picker.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        picker.style.setProperty('--my', (e.clientY - r.top) + 'px');
      }, { passive: true });
      hero.addEventListener('pointerleave', () => { rx(rest.x); ry(rest.y); picker.style.setProperty('--mx', '-999px'); });
    }
    /* the floor answers the row you point at */
    const ping = (el) => {
      if (!canvas) return;
      const r = el.getBoundingClientRect(), cr = canvas.getBoundingClientRect();
      if (!cr.width || !cr.height) return;
      state.ox = ((r.left + r.width / 2 - cr.left) / cr.width) * 2 - 1;
      state.oy = -(((r.bottom + 40 - cr.top) / cr.height) * 2 - 1);
      state.ping = 1;
    };
    rows.forEach((li) => {
      const a = $('a', li);
      a.addEventListener('pointerenter', () => ping(a));
      a.addEventListener('focus', () => ping(a));
    });
    setTimeout(() => ping(picker), 1500);

    /* two depths on the way out: the claim leaves first, the picker lingers */
    if (wide) {
      const leave = { trigger: hero, start: 'top top', end: 'bottom top', scrub: true };
      gsap.to('.hub-hero-grid > div:first-child', { yPercent: -14, ease: 'none', scrollTrigger: leave });
      gsap.to(picker, { y: 90, ease: 'none', scrollTrigger: leave, immediateRender: false });
    }
  }

  /* the facts: six counts up, the three zeros fall to zero */
  const from = [0, 29, 12, 40];
  $$('.hub-facts b').forEach((b, i) => count(gsap, b, from[i] || 0, { duration: 1.6, delay: 0.9 + i * 0.12 }));

  /* ---- tool cards: rise out of the page, then run their sample ---- */
  const tools = $$('.tool');
  gsap.set(tools, fine ? { opacity: 0, y: 80, rotationX: 14, transformPerspective: 1000, transformOrigin: '50% 100%' } : { opacity: 0, y: 48 });
  ScrollTrigger.batch(tools, {
    start: 'top 90%', once: true,
    onEnter: (batch) => {
      gsap.to(batch, { opacity: 1, y: 0, rotationX: 0, duration: 1.1, ease: OUT, stagger: 0.1, overwrite: true, clearProps: fine ? '' : 'transform' });
      batch.forEach((card, i) => setTimeout(() => runDemo(gsap, card), i * 100));
    },
  });
  if (fine) {
    tools.forEach((card) => tilt(gsap, card, 5));
    $$('.plan').forEach((card) => tilt(gsap, card, 3));
  }

  /* ---- three steps: the rule over each one fills as you read across ---- */
  const steps = $$('#how .steps li');
  if (steps.length) {
    ScrollTrigger.create({
      trigger: '#how .steps', start: 'top 78%', end: 'top 28%', scrub: 0.5,
      onUpdate(self) {
        steps.forEach((li, i) => {
          const p = gsap.utils.clamp(0, 1, self.progress * steps.length - i);
          li.style.setProperty('--p', p);
          li.classList.toggle('is-lit', p > 0.02);
        });
      },
    });
  }

  /* the launch price counts up when its plan arrives */
  const price = $('.plan.roast .price');
  if (price) ScrollTrigger.create({ trigger: price, start: 'top 88%', once: true, onEnter: () => count(gsap, price, 0, { duration: 1.3 }) });

  /* ---- four rules: the two columns travel at different speeds ---- */
  const rules = $$('.rules li');
  gsap.set(rules, { opacity: 0 });
  ScrollTrigger.batch(rules, { start: 'top 94%', once: true,
    onEnter: (batch) => gsap.to(batch, { opacity: 1, duration: 0.9, ease: 'power2.out', stagger: 0.08 }) });
  if (matchMedia('(min-width:701px)').matches) {
    rules.forEach((li, i) => {
      gsap.fromTo(li, { y: i % 2 ? 110 : 30 }, { y: i % 2 ? -50 : -10, ease: 'none',
        scrollTrigger: { trigger: '.rules', start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  }

  /* the closing band's ground drifts under its words */
  const band = $('.contact.ember');
  if (band) gsap.fromTo(band, { '--by': '-12%' }, { '--by': '12%', ease: 'none',
    scrollTrigger: { trigger: band, start: 'top bottom', end: 'bottom top', scrub: true } });
}

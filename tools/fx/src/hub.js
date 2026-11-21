/* /checks/ tool examples, workflow steps and hero canvas feedback. */
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
  if (canvas) {
    const ping = (link) => {
      const r = link.getBoundingClientRect(), cr = canvas.getBoundingClientRect();
      if (!cr.width || !cr.height) return;
      state.ox = ((r.left + r.width / 2 - cr.left) / cr.width) * 2 - 1;
      state.oy = -(((r.bottom + 40 - cr.top) / cr.height) * 2 - 1);
      state.ping = 1;
    };
    $$('.picker a').forEach((link) => {
      link.addEventListener('pointerenter', () => ping(link));
      link.addEventListener('focus', () => ping(link));
    });
  }

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

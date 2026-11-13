/* Stacked sections: on skill pages each section below the hero is a card that pins as the next
   one slides over it, then settles back a little, like the flagship cards on the homepage.
   A card taller than the window scrolls through first and pins by its foot, so nothing is ever
   hidden. No dependencies; without it the sections are plain cards in a column. */

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

export function stack(cards) {
  if (cards.length < 2) return;
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const wide = matchMedia('(min-width:761px)');
  let tops = [];

  function layout() {
    if (!wide.matches) {
      root.classList.remove('is-stacked');
      cards.forEach((c) => { c.style.top = ''; c.style.transform = ''; c.style.removeProperty('--shade'); });
      return;
    }
    root.classList.add('is-stacked');
    const vh = innerHeight;
    tops = cards.map((c, i) => {
      const t = Math.round(Math.min(84 + i * 14, vh - c.offsetHeight - 16));
      c.style.top = t + 'px';
      return t;
    });
    paint();
  }

  /* each card settles back as the next one covers it */
  function paint() {
    if (reduced || !wide.matches) return;
    const vh = innerHeight;
    for (let i = 0; i < cards.length - 1; i++) {
      const nextTop = cards[i + 1].getBoundingClientRect().top;
      const p = clamp((vh - nextTop) / Math.max(1, vh - tops[i + 1]), 0, 1);
      cards[i].style.transform = p ? 'scale(' + (1 - p * 0.045).toFixed(4) + ')' : '';
      cards[i].style.setProperty('--shade', (p * 0.32).toFixed(3));
    }
  }

  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; paint(); });
  }, { passive: true });
  addEventListener('resize', layout);
  if (wide.addEventListener) wide.addEventListener('change', layout);
  if (window.ResizeObserver) { const ro = new ResizeObserver(layout); cards.forEach((c) => ro.observe(c)); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  layout();
}

/* the hand-written skill pages load this file on its own */
export function auto() {
  const cards = [].slice.call(document.querySelectorAll('body > header.hero ~ section, body > .sk-hero ~ section'));
  stack(cards);
}

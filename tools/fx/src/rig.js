/* The rig: an agent session in three planes (the SKILL.md the agent read, the terminal that ran
   it, the verdict stamp), replayed line by line. The homepage replays real runs; every other page
   builds its session from its own content (a skill's install and files, a workflow's route, a
   catalogue's tested skills), so nothing here is made up. Pages read the same without it. */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => [].slice.call((el || document).querySelectorAll(s));
const e = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const txt = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

/* word-wrap to a column width; the last line ends in an ellipsis when text is left over */
function wrap(text, width, max) {
  const out = [];
  let line = '';
  const words = text.split(' ');
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    if ((line + ' ' + w).trim().length > width) {
      out.push(line.trim()); line = w;
      if (out.length === max) { out[max - 1] = out[max - 1].replace(/[\s,;:.]*$/, '') + '…'; return out; }
    } else line += ' ' + w;
  }
  if (line.trim()) out.push(line.trim());
  while (out.length < max) out.push('');
  return out.slice(0, max);
}

/* ---- the sessions ---- */

export const HOME_RUNS = [
  { bar: 'agent · real run · 24 Oct 2026', repo: 'arm-pz/web-preflight', verdict: 'PASS', note: 'nothing exposed · see the run', href: '#proof',
    md: { name: 'web-preflight', desc: ['Checks a site you own', 'before you ship it. A check that never', 'ran is INCONCLUSIVE, never a pass.'], title: 'Web Preflight', body: ['Probe the paths that leak, read the', 'headers, then give one verdict.'] },
    lines: [['p', '/web-preflight skillsmith.tech'], ['d', 'reading SKILL.md · 4 checks'], ['ok', 'http → https        ', '301'], ['ok', 'HSTS, CSP           ', 'present'], ['ok', 'X-Frame, nosniff    ', 'present'], ['d', 'probing 19 sensitive paths'], ['ok', '.env .git maps admin  ', '404 × 19'], ['ok', 'catch-all routing     ', 'none'], ['v', 'verdict  PASS']] },
  { bar: 'agent · real run · 23 Oct 2026', repo: 'arm-pz/seo-crawl', verdict: '1 ERROR', note: 'found, fixed, re-crawled clean', bad: true, href: '#proof',
    md: { name: 'seo-crawl', desc: ['Crawls a site you own and', 'returns evidence-backed technical SEO', 'findings. Unrun checks: INCONCLUSIVE.'], title: 'SEO Crawl', body: ['Fetch every page, run five checks,', 'cite the URL behind each finding.'] },
    lines: [['p', '/seo-crawl skills.caffeinity.com'], ['ok', 'pages      ', '24 of 24'], ['ok', 'checks     ', '5 complete'], ['bad', 'broken-internal-link'], ['d', '  /cdn-cgi/l/email-protection → 404'], ['ok', 'titles, canonicals ', 'clean'], ['d', 'findings   1 error · 12 info'], ['v', 'verdict  FIX 1, then re-crawl']] },
  { bar: 'agent · real run · 24 Oct 2026', repo: 'arm-pz/tune-skill', verdict: '41/42', note: 'one skill would not load · fixed', bad: true, href: '#proof',
    md: { name: 'tune-skill', desc: ['Audits a skill that', 'already exists: why it does not', 'trigger, where it overlaps a sibling.'], title: 'Tune Skill', body: ['Run check_skill.py, read the failures,', 'propose the smallest fix.'] },
    lines: [['p', '/tune-skill audit every skill'], ['d', 'python check_skill.py × 42'], ['ok', 'frontmatter      ', '41 pass'], ['bad', 'crash-test  invalid YAML'], ['d', '  unquoted ": " in description'], ['ok', 'folder = name    ', '42 / 42'], ['d', 'WARN 16 · NOTE 2'], ['v', 'verdict  1 FAIL → fixed']] },
];

const ROUTER = { name: 'caffeinity-routing', desc: ['Tell it the outcome you', 'want and it picks the skills, in order,', 'from twelve workflows.'], title: 'Caffeinity Routing', body: ['Each step hands its work to the', 'next and stops at its own gate.'] };

function route(title, brew, steps, href) {
  const lines = [['p', '/caffeinity-routing ' + title.toLowerCase()], ['d', 'matched ' + brew]];
  steps.slice(0, 6).forEach((s, i) => lines.push(['f', (i + 1) + '  ' + s.names, s.optional ? 'optional' : '']));
  lines.push(['v', 'route  ' + steps.length + ' steps, in order']);
  return { bar: 'agent · routing', repo: 'arm-pz/caffeinity-skills', md: ROUTER, lines,
    verdict: (brew.split('·')[1] || brew).trim(), note: steps.length + ' skills hand work along', href };
}

function install(name, title, cmd, desc, facts, files, stamp) {
  const lines = [['p', cmd]];
  if (/^npx /.test(cmd)) lines.push(['d', 'into .claude/skills/' + name + '/']);
  if (files) { if (facts) lines.push(['d', facts]); }
  else (facts || '').split(' · ').filter(Boolean).forEach((f) => lines.push(['ok', f.padEnd(22), '']));
  (files || []).slice(0, 5).forEach((f) => lines.push(['f', f[0].padEnd(28), f[1]]));
  if (files && files.length > 5) lines.push(['d', '+ ' + (files.length - 5) + ' more']);
  lines.push(['v', 'installed  ' + name]);
  const d = wrap(desc, 36, 6);
  return Object.assign({ bar: 'agent · install', repo: 'arm-pz/' + name,
    md: { name, desc: [d[0], d[1], d[2]], title, body: [d[3], d[4]] }, lines }, stamp);
}

/* read this page's own content into sessions; null where a page has nothing to show */
export function pageRuns() {
  /* a generated skill or mod page: its install command and the files it ships */
  const sk = $('.sk-hero');
  if (sk && $('#cmd', sk)) {
    const name = txt($('.crumbs span', sk)) || 'skill';
    const files = $$('.files tbody tr').map((tr) => [txt(tr.cells[0]), txt(tr.cells[1]) + ' lines']);
    const foot = $('.files tfoot tr');
    const facts = foot ? txt(foot.cells[0]) + ' · ' + txt(foot.cells[1]) + ' lines' : '';
    const dt = $$('.qb dt').find((d) => /nightly/i.test(d.textContent));
    const health = dt && dt.nextElementSibling ? txt(dt.nextElementSibling.firstChild) : '';
    return [install(name, txt($('h1', sk)), txt($('#cmd', sk)), txt($('.lead', sk)), facts, files,
      health ? { verdict: health, note: 'nightly check · see the record', bad: !/^pass/i.test(health), href: '#qb-h' }
        : { verdict: files.length + ' files', note: 'plain markdown · read it first', href: '#files-h' })];
  }
  const ph = $('.page-hero');
  /* one workflow */
  if (ph && $('.steps-list')) {
    const slug = (a) => (a.getAttribute('href') || '').replace(/^\/|\/$/g, '') || txt(a);
    const steps = $$('.steps-list .step').map((s) => ({ names: $$('a.step-skill', s).map(slug).join(' or '), optional: /optional/i.test(txt($('.step-n', s))) }));
    return [route(txt($('h1', ph)), txt($('.crumbs span', ph)), steps, '#steps-h')];
  }
  /* every workflow */
  if (ph && $('.flow')) {
    return $$('.flow').slice(0, 6).map((f) => route(txt($('h3', f)), txt($('.flow-id', f)),
      $$('.flow-steps li', f).map((li) => ({ names: $$('a', li).map(txt).join(' or '), optional: !!$('.opt', li) })), '#' + (f.id || '')));
  }
  /* a catalogue: the tested skills first, each with its install and what it weighs */
  if (ph && $('.skill')) {
    const cards = $$('.skill');
    const tested = cards.filter((c) => $$('.chip-hot', c).some((x) => /^tested/i.test(x.textContent)));
    return (tested.length ? tested : cards).slice(0, 4).map((c) => {
      const chip = $$('.chip-hot', c).map(txt).find((x) => /^tested/i.test(x));
      const btn = $('[data-copy]', c);
      return install(c.id, txt($('h3', c)), btn ? btn.getAttribute('data-copy') : '', txt($('.sk-blurb', c)), txt($('.sk-stats', c)), null,
        chip ? { verdict: 'TESTED', note: chip.replace(/^tested\s*/i, '') + ' · real run', href: '#' + c.id }
          : /^\/plugin/.test(btn ? btn.getAttribute('data-copy') : '') ? { verdict: 'MOD', note: 'Claude Code plugin · read its hooks', href: '#' + c.id }
          : { verdict: txt($('.chip', c)) || 'skill', note: 'plain markdown · 0 API keys', href: '#' + c.id });
    });
  }
  /* custom work: an example, and labelled as one */
  if (ph && $('.plans')) {
    return [{ bar: 'agent · example', repo: 'your-team/release-checklist', verdict: 'YOURS', note: 'tested on your real tasks', href: '#contact',
      md: { name: 'release-checklist', desc: ['Runs our release', 'checklist before a tag: changelog,', 'migrations, flags, rollback note.'], title: 'Release Checklist', body: ['Written in your house style, from', 'the steps your team already follows.'] },
      lines: [['p', '/draft-skill turn our release checklist into a skill'], ['d', 'confirming the purpose before writing'], ['ok', 'installed skills   ', 'no overlap'], ['ok', 'SKILL.md           ', 'drafted'], ['ok', 'trigger cases      ', '10 + 4 pairs'], ['ok', 'check_skill.py     ', '0 fail'], ['d', 'next: run it on last week\'s release'], ['v', 'ready for your review']] }];
  }
  /* the 404: a real one, for the address you asked for */
  const lost = $('.lost');
  if (lost) {
    const path = (location.pathname || '/missing').slice(0, 34);
    return [{ bar: 'agent · this request', repo: 'arm-pz/web-preflight', verdict: '404', note: 'a real one · try the skills', bad: true, href: '/skills/',
      md: HOME_RUNS[0].md,
      lines: [['p', 'curl -I skillsmith.tech' + path], ['bad', 'HTTP/2 404'], ['d', 'no catch-all: a missing page'], ['d', 'answers 404, not the homepage'], ['ok', '/skills/      ', '200'], ['ok', '/workflows/   ', '200'], ['v', 'verdict  nothing brewed here']] }];
  }
  return null;
}

/* ---- the markup ---- */

export function buildRig() {
  const fig = document.createElement('figure');
  fig.className = 'rig';
  fig.setAttribute('data-rig', '');
  fig.innerHTML = '<div class="rig-stack"><div class="rig-file" aria-hidden="true"><p class="rig-bar"><span>SKILL.md</span><span class="rig-repo"></span></p><pre class="rig-src"></pre></div>'
    + '<div class="rig-term" aria-hidden="true"><p class="rig-bar"><i></i><i></i><i></i><span></span></p><pre class="rig-out"></pre></div>'
    + '<a class="rig-stamp" href="#"><b></b><span></span></a></div><figcaption class="sr-only"></figcaption>';
  return fig;
}

/* put the rig beside a hero's copy */
export function mountBeside(hero) {
  const wrapEl = $('.wrap', hero);
  if (!wrapEl) return null;
  const copy = document.createElement('div');
  copy.className = 'rig-copy';
  while (wrapEl.firstChild) copy.appendChild(wrapEl.firstChild);
  wrapEl.appendChild(copy);
  wrapEl.classList.add('rig-host');
  const fig = buildRig();
  wrapEl.appendChild(fig);
  return fig;
}

const line = (l) => l[0] === 'ok' ? e(l[1]) + '<span class="ok">' + e(l[2]) + '</span>'
  : l[0] === 'f' ? e(l[1]) + (l[2] ? '  <span class="d">' + e(l[2]) + '</span>' : '')
  : l[0] === 'bad' ? '<span class="bad">' + e(l[1]) + '</span>'
  : '<span class="' + l[0] + '">' + e(l[1]) + '</span>';

function paintFile(rig, run) {
  const m = run.md, n = (i, s) => '<span class="n">' + i + '</span>' + s;
  $('.rig-src', rig).innerHTML = [n(1, '<span class="k">---</span>'), n(2, '<span class="k">name:</span> ' + e(m.name)),
    n(3, '<span class="k">description:</span> ' + e(m.desc[0])), n(4, '  ' + e(m.desc[1])), n(5, '  ' + e(m.desc[2])),
    n(6, '<span class="k">---</span>'), n(7, '<span class="h"># ' + e(m.title) + '</span>'), n(8, e(m.body[0] || '')), n(9, e(m.body[1] || ''))].join('\n');
  $('.rig-repo', rig).textContent = run.repo;
  $('.rig-term .rig-bar span', rig).textContent = run.bar;
  const cap = $('figcaption', rig);
  if (cap && !cap.textContent) cap.textContent = run.lines.map((l) => l.slice(1).join(' ')).join('. ');
}
function paintStamp(rig, run) {
  const s = $('.rig-stamp', rig);
  $('b', s).textContent = run.verdict;
  $('span', s).textContent = run.note;
  s.setAttribute('href', run.href || '#');
  s.classList.toggle('is-bad', !!run.bad);
}

/* show a session finished, with no motion */
export function rest(rig, run) {
  paintFile(rig, run);
  $('.rig-out', rig).innerHTML = run.lines.map(line).join('\n');
  paintStamp(rig, run);
}

/* replay sessions, tilt with the pointer, spread on scroll, and tell the floor where to ripple */
export function play(rig, runs, opts) {
  const { state, hero, fine, loop } = opts;
  const out = $('.rig-out', rig), stack = $('.rig-stack', rig), stamp = $('.rig-stamp', rig);
  let visible = true;
  new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(rig);
  const idle = async () => { while (!visible || document.hidden) await wait(400); };

  async function run(r, first) {
    await idle();
    if (!first) {
      gsap.to(stamp, { opacity: 0, scale: 0.8, duration: 0.3 });
      await gsap.to(out, { opacity: 0, duration: 0.35 });
    } else gsap.set(stamp, { opacity: 0 });
    paintFile(rig, r);
    out.innerHTML = '<span class="caret"></span>';
    gsap.set(out, { opacity: 1 });
    const html = [];
    for (const l of r.lines) {
      await idle();
      if (l[0] === 'p') {
        for (let i = 1; i <= l[1].length; i += l[1].length > 40 ? 2 : 1) {
          out.innerHTML = html.concat('<span class="p">' + e(l[1].slice(0, i)) + '</span><span class="caret"></span>').join('\n');
          await wait(30 + Math.random() * 36);
        }
        html.push('<span class="p">' + e(l[1]) + '</span>');
        await wait(420);
        continue;
      }
      html.push(line(l));
      out.innerHTML = html.join('\n') + '\n<span class="caret"></span>';
      if (l[0] === 'ok' || l[0] === 'f') state.ping = 1;
      if (l[0] === 'bad') state.ping = -1;
      await wait(l[0] === 'd' ? 360 : 480);
    }
    out.innerHTML = html.join('\n');
    paintStamp(rig, r);
    gsap.fromTo(stamp, { opacity: 0, scale: 1.6, rotate: -12 }, { opacity: 1, scale: 1, rotate: -4, duration: 0.55, ease: 'back.out(2.2)' });
    state.ping = r.bad ? -1 : 1;
    await wait(4200);
  }
  (async () => {
    await wait(opts.delay || 1200);
    for (let i = 0; ; i++) {
      if (i >= runs.length) { if (!loop || runs.length < 2) return; i = 0; }
      await run(runs[i], i === 0 && !opts.started);
      opts.started = true;
    }
  })();

  const base = { y: opts.tiltY || -16, x: opts.tiltX || 7 };
  const rx = gsap.quickTo(stack, 'rotationX', { duration: 1, ease: 'power3.out' });
  const ry = gsap.quickTo(stack, 'rotationY', { duration: 1, ease: 'power3.out' });
  gsap.set(stack, { rotationY: base.y, rotationX: base.x });
  if (fine) addEventListener('pointermove', (ev) => {
    ry(base.y + ((ev.clientX / innerWidth) * 2 - 1) * 9); rx(base.x - ((ev.clientY / innerHeight) * 2 - 1) * 6);
  }, { passive: true });
  const spread = { trigger: hero, start: 'top top', end: 'bottom top', scrub: true };
  gsap.to($('.rig-file', rig), { z: -260, x: -40, ease: 'none', scrollTrigger: spread });
  gsap.to(stamp, { z: 240, y: -40, ease: 'none', scrollTrigger: spread });
  gsap.from(stack, { opacity: 0, y: 60, rotationY: base.y - 24, duration: 1.6, delay: 0.3, ease: 'expo.out' });

  const where = () => {
    const c = opts.canvas;
    if (!c) return;
    const r = $('.rig-term', rig).getBoundingClientRect(), cr = c.getBoundingClientRect();
    if (!cr.width || !cr.height) return;
    state.ox = ((r.left + r.width / 2 - cr.left) / cr.width) * 2 - 1;
    state.oy = -(((r.bottom + 30 - cr.top) / cr.height) * 2 - 1);
  };
  where();
  addEventListener('resize', where);
  ScrollTrigger.create({ trigger: hero, start: 'top top', end: 'bottom top', onUpdate: where });
}

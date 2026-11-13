// Playwright ground truth for SEO runs: render every sitemap URL and report on-page facts.
//   node truth_seo.mjs https://skillsmith.tech [max-pages]
import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const { chromium } = require(process.env.PW_MODULE || 'playwright')
const base = (process.argv[2] || 'https://skillsmith.tech').replace(/\/$/, ''), max = +(process.argv[3] || 200)
const xml = await (await fetch(base + '/sitemap.xml')).text()
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]).slice(0, max)
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined })
const page = await browser.newPage(), rows = [], links = new Set()
for (const u of urls) {
  const r = await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(e => null)
  const f = await page.evaluate(() => ({
    title: document.title, desc: document.querySelector('meta[name=description]')?.content || '',
    h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim().replace(/\s+/g, ' ')),
    canonical: document.querySelector('link[rel=canonical]')?.href || '',
    robots: document.querySelector('meta[name=robots]')?.content || '',
    hrefs: [...document.querySelectorAll('a[href]')].map(a => a.href),
  })).catch(() => ({ title: '', desc: '', h1: [], canonical: '', robots: '', hrefs: [] }))
  f.hrefs.filter(h => h.startsWith(base)).forEach(h => links.add(h.split('#')[0]))
  rows.push({ url: u, status: r ? r.status() : 'ERR', ...f, hrefs: undefined })
}
await browser.close()
const broken = []
for (const l of links) { const s = await fetch(l, { method: 'HEAD', redirect: 'manual' }).then(r => r.status).catch(() => 'ERR'); if (s >= 400 || s === 'ERR') broken.push(`${s} ${l}`) }
const dup = (k) => Object.entries(rows.reduce((a, r) => ((a[r[k]] ||= []).push(r.url), a), {})).filter(([v, us]) => v && us.length > 1)
console.log(`pages rendered: ${rows.length} of ${urls.length} in sitemap; internal links checked: ${links.size}`)
console.log(`non-200 pages: ${rows.filter(r => r.status !== 200).map(r => r.status + ' ' + r.url).join(', ') || 'none'}`)
console.log(`broken internal links: ${broken.length ? broken.join(', ') : 'none'}`)
console.log(`titles over 60 chars: ${rows.filter(r => r.title.length > 60).length}; descriptions missing: ${rows.filter(r => !r.desc).length}; over 160 chars: ${rows.filter(r => r.desc.length > 160).length}`)
console.log(`pages without exactly one h1: ${rows.filter(r => r.h1.length !== 1).map(r => r.url + ' (' + r.h1.length + ')').join(', ') || 'none'}`)
console.log(`canonical missing or pointing elsewhere: ${rows.filter(r => r.canonical.replace(/\/$/, '') !== r.url.replace(/\/$/, '')).map(r => r.url + ' -> ' + (r.canonical || 'none')).join(', ') || 'none'}`)
console.log(`duplicate titles: ${dup('title').map(([v, us]) => JSON.stringify(v) + ' x' + us.length).join('; ') || 'none'}`)
console.log(`duplicate descriptions: ${dup('desc').length}`)
console.log('\nper page: status | title (len) | h1')
for (const r of rows) console.log(`${r.status} ${r.url.replace(base, '') || '/'} | ${r.title} (${r.title.length}) | ${r.h1.join(' / ')}`)

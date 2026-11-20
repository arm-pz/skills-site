// Ledgerboard: marketing page + dashboard stats for local performance testing. No dependencies.
// Start: node server.js   (http://127.0.0.1:3200)   First run: node make_assets.js
const http = require('http'), fs = require('fs'), path = require('path')
const sleep = ms => new Promise(r => setTimeout(r, ms))
async function query(sql) { await sleep(30); return { sql, rows: 1 } }   // stands in for a DB round trip
http.createServer(async (req, res) => {
  if (req.url === '/api/stats') {
    const customers = await query('select id from customers limit 30')
    const out = []
    for (let i = 0; i < 30; i++) out.push(await query(`select sum(total) from invoices where customer_id=${i}`))  // one query per customer
    res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify({ customers: 30, totals: out.length }))
  }
  const f = req.url === '/' ? 'index.html' : path.basename(req.url)
  const p = path.join(__dirname, 'public', f)
  if (!fs.existsSync(p)) { res.writeHead(404); return res.end() }
  const type = f.endsWith('.png') ? 'image/png' : f.endsWith('.js') ? 'text/javascript' : f.endsWith('.css') ? 'text/css' : 'text/html'
  res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-store' })   // nothing is cached, nothing compressed
  res.end(fs.readFileSync(p))
}).listen(3200, '127.0.0.1', () => console.log('Ledgerboard on http://127.0.0.1:3200'))

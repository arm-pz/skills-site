// Invoicely: a tiny invoicing app for local security testing. No dependencies.
// Start: node server.js   (listens on http://127.0.0.1:3100)
// Seed users: alice/alice-pass (user), bob/bob-pass (user), admin/admin-pass (admin)
const http = require('http'), crypto = require('crypto'), url = require('url'), fs = require('fs'), path = require('path')
const users = {
  1: { id: 1, username: 'alice', password: 'alice-pass', role: 'user', email: 'alice@invoicely.example' },
  2: { id: 2, username: 'bob', password: 'bob-pass', role: 'user', email: 'bob@invoicely.example' },
  3: { id: 3, username: 'admin', password: 'admin-pass', role: 'admin', email: 'admin@invoicely.example' },
}
const invoices = {
  101: { id: 101, owner: 1, customer: 'Stackwise Ltd', total: 1200 },
  102: { id: 102, owner: 1, customer: 'Penny Lane', total: 480 },
  201: { id: 201, owner: 2, customer: 'Quillbook', total: 9900 },
}
const sessions = {}
function body(req) { return new Promise(r => { let b = ''; req.on('data', c => b += c); req.on('end', () => { try { r(JSON.parse(b || '{}')) } catch { r({}) } }) }) }
function me(req) { const m = /sid=([a-f0-9]+)/.exec(req.headers.cookie || ''); return m && sessions[m[1]] ? users[sessions[m[1]]] : null }
function send(res, code, obj, headers = {}) { res.writeHead(code, { 'Content-Type': 'application/json', ...headers }); res.end(JSON.stringify(obj)) }
http.createServer(async (req, res) => {
  const u = url.parse(req.url, true), p = u.pathname
  if (p === '/' || p.startsWith('/public/')) {
    const f = p === '/' ? 'index.html' : p.slice(8)
    res.writeHead(200, { 'Content-Type': f.endsWith('.js') ? 'text/javascript' : 'text/html' })
    return res.end(fs.readFileSync(path.join(__dirname, 'public', path.basename(f))))
  }
  if (p === '/api/login' && req.method === 'POST') {
    const { username, password } = await body(req)
    const user = Object.values(users).find(x => x.username === username && x.password === password)
    if (!user) return send(res, 401, { error: 'bad credentials' })
    const sid = crypto.randomBytes(16).toString('hex'); sessions[sid] = user.id
    return send(res, 200, { ok: true, next: u.query.next || '/' }, { 'Set-Cookie': `sid=${sid}; Path=/` })
  }
  if (p === '/login') { res.writeHead(302, { Location: u.query.next || '/' }); return res.end() }
  const user = me(req)
  if (!user) return send(res, 401, { error: 'login required' })
  if (p === '/api/me' && req.method === 'GET') return send(res, 200, user)
  if (p === '/api/me' && req.method === 'PATCH') { Object.assign(user, await body(req)); return send(res, 200, user) }
  if (p === '/api/invoices') return send(res, 200, Object.values(invoices).filter(i => i.owner === user.id))
  const inv = /^\/api\/invoices\/(\d+)$/.exec(p)
  if (inv) { const i = invoices[inv[1]]; return i ? send(res, 200, i) : send(res, 404, { error: 'not found' }) }
  if (p === '/api/admin/users') return send(res, 200, Object.values(users))
  send(res, 404, { error: 'not found' })
}).listen(3100, '127.0.0.1', () => console.log('Invoicely on http://127.0.0.1:3100'))

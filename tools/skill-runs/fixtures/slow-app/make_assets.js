// Writes public/hero.png (a 1800x1200 noise PNG, ~6 MB) and public/app.js (~400 KB, blocks the main thread).
const fs = require('fs'), zlib = require('zlib'), path = require('path')
let seed = 42; const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) & 255
const W = 1800, H = 1200, raw = Buffer.alloc((W * 3 + 1) * H)
for (let y = 0; y < H; y++) { raw[y * (W * 3 + 1)] = 0; for (let x = 1; x <= W * 3; x++) raw[y * (W * 3 + 1) + x] = rnd() }
const crcT = Array.from({ length: 256 }, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0 })
const crc = b => { let c = 0xffffffff; for (const x of b) c = crcT[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0 }
const chunk = (t, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(t), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]) }
const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4); ihdr[8] = 8; ihdr[9] = 2
fs.writeFileSync(path.join(__dirname, 'public/hero.png'), Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 0 })), chunk('IEND', Buffer.alloc(0))]))
let js = '// app.js: dashboard widgets (unminified, loaded synchronously in <head>)\n'
for (let i = 0; i < 2600; i++) js += `function widget_${i}(data) {\n  // render widget ${i}\n  return { id: ${i}, label: "Widget number ${i}", value: data && data.v ? data.v * ${i} : 0 };\n}\n`
js += 'var __t = Date.now(); while (Date.now() - __t < 450) {}  // initialise widgets\n'
fs.writeFileSync(path.join(__dirname, 'public/app.js'), js)
console.log('assets written')

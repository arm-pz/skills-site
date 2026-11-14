I couldn't run the live attacks. The sandbox denied my Bash call, the one that sends the exploit requests to 127.0.0.1:3100. An earlier read-only Bash call (`ls`/`cat`/`curl` to `/`) worked, so I'm stopping here instead of retrying in another form.

**Please do one of these:**
- Allow Bash for `curl` against `http://127.0.0.1:3100` (and `node` for the fix and regression-test steps), then I'll run the attacks and capture evidence.
- Or run the attacks yourself and paste me the output.

**What I found by reading `server.js`.** None of this has been executed, so under the skill's rules every item is `not-proven`, not confirmed.

| Priority | Suspected issue | Where | Why |
|---|---|---|---|
| 1 | Any user can make themselves admin | `PATCH /api/me`, line 37 | `Object.assign(user, body)` copies the request body onto the user record, so `{"role":"admin"}` should work. `{"id":3}` may also work. |
| 2 | Any logged-in user can read other users' invoices | `GET /api/invoices/:id`, line 40 | It looks up the invoice by id and never checks `owner`. Bob should be able to read Alice's invoice 101. |
| 3 | Any logged-in user can list all users with plaintext passwords | `GET /api/admin/users`, line 41 | It never checks `role`. It returns the full records, including `password`. |
| 4 | Open redirect | `/login?next=` (line 33) and the `next` value returned by `POST /api/login` (line 31) | The `next` value is passed through unvalidated, so it can be used for phishing. |
| 5 | Weak session and login hygiene | lines 26–31 | The cookie has no `HttpOnly`, `SameSite` or `Secure`. There is no login throttling. Passwords are stored and compared in plaintext. |

Scenarios that look not-applicable because the features don't exist: password reset, quotas and races, SSRF, uploads, AI ingestion. Stored XSS and the cache and preview checks still need a look at `public/`, which I haven't read.

**Fix first, in this order:**
1. Allowlist the fields `PATCH /api/me` accepts, or remove it. This closes the role escalation.
2. Add `i.owner === user.id` to the invoice lookup. Return 404 if it doesn't match, so the response doesn't reveal that the invoice exists.
3. Add `user.role === 'admin'` to the admin route, and never return `password`.
4. Only accept same-origin relative `next` paths, meaning a leading `/` and not `//`.
5. Set `HttpOnly; SameSite=Lax` on the cookie, hash the passwords, and add login rate limiting.

After you decide on access, I'll apply the fixes, write the regression tests, and run the negative controls.
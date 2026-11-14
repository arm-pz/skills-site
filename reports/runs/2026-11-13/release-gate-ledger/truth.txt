Planted defects in fixtures/vuln-app (6):
1. IDOR: GET /api/invoices/:id returns any invoice with no owner check (alice can read bob's 201).
2. Broken function-level authorization: GET /api/admin/users returns every user (with passwords) to any logged-in user; the admin link is only hidden in the UI.
3. Mass assignment / privilege escalation: PATCH /api/me merges the whole body, so {"role":"admin"} makes any user an admin (also can overwrite id/password).
4. Session cookie set without HttpOnly, Secure or SameSite; no security headers on any response.
5. Open redirect: /login?next=https://evil.example redirects anywhere; /api/login echoes next unvalidated.
6. No rate limit or lockout on POST /api/login.
Also true: passwords stored and returned in plain text (seen through #2 and GET /api/me).

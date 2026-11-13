# Fact sheet: Reconcile (Ledgerline Ltd, England, company no. 14XXXXX — fill in), contact privacy@ledgerline.example
- Accounts: name, work email, company name, password hash.
- Connected data: read-only OAuth tokens for Stripe, GoCardless and Xero; we store payout and invoice records (amounts, dates, customer names on invoices) to match them.
- Hosting: AWS eu-west-2 (London). Email via Postmark (US). Error tracking via Sentry (US). Payments to us via Stripe.
- Analytics: Plausible (no cookies). One strictly necessary session cookie.
- Retention: account data kept while subscribed; deleted 30 days after cancellation; invoices synced deleted with the account. Backups roll off after 35 days.
- Billing: monthly, cancel any time, takes effect end of period; refunds only for billing errors.
- Customers are UK/EU businesses; we act as processor for invoice data and controller for account data.
- Not decided yet: whether we will use customer data to improve matching models. (Do not state either way.)

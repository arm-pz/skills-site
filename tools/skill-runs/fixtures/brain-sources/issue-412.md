GitHub issue #412 (ledgerline/reconcile), opened 2026-10-02 by hana-stackwise
Title: Partial payments from GoCardless show as unmatched
Body: When a customer pays an invoice in two instalments via GoCardless, the first instalment stays "unmatched" until the second arrives. We expected it to show as "partially matched". 14 invoices affected in October.
Comment (dev, 2026-10-03): Confirmed. Matcher only matches when payout total == invoice total. Fix needs a tolerance + partial state.

# Why we rebuilt our invoicing engine

Our old invoicing engine handled about 40,000 invoices a day. At month end, when volume roughly triples, it fell behind, and some invoices went out up to six hours late. Customers noticed, and late invoices hurt their cash flow.

The new engine queues invoices per customer, retries failures with backoff, and lets finance teams see where each invoice is. In testing, a month-end run finished in 38 minutes. The old engine took 5 hours and 50 minutes.

We think this may help some customers get paid a little sooner, but we haven't measured that yet.

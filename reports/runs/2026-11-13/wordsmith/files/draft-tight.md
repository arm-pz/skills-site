# Why we rebuilt our invoicing engine

Invoicing shows customers how much a business values them. At Brightfold, we rebuilt our engine from the ground up.

Our old engine processed about 40,000 invoices a day, but it struggled at month end, when volume roughly triples. Some invoices went out up to six hours late. Customers noticed. Experts agree that late invoices hurt cash flow.

The new engine queues invoices per customer, retries failures with backoff, and lets finance teams see exactly where each invoice is. In testing, month-end runs finished in 38 minutes instead of 5 hours and 50 minutes.

We think this may help some customers get paid a little sooner, although we have not measured that yet.

Let us know if you have any questions.

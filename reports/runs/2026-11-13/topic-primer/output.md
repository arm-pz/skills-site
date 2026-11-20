# Double-entry bookkeeping: foundation

**Why it matters:** A startup's ledger is the source of truth for money, the way a database is for application state. Double-entry is the rule set that keeps it consistent. Once you see it as an append-only log with an invariant, you can read any ledger.

## Step 1: Account
**Account** = a named bucket that tracks one kind of thing (e.g. "Cash", "Rent expense"). Think of it as a variable with a name and a running balance.

## Step 2: Transaction and entry
A **transaction** is one business event (e.g. "paid AWS $500"). It is recorded as two or more **entries** (also called lines or postings). Each entry touches one account and moves an amount in one of two directions: **debit** or **credit**.

## Step 3: Debit and credit
Forget the everyday meanings (credit is not "good", debit is not "bad"). They are just **left** and **right**: the two directions of a signed number. Debit = left column, credit = right column.

## Step 4: The invariant
**Every transaction must have total debits = total credits.** This is like a checksum or a transaction that must net to zero. If it doesn't balance, the entry is invalid. This is the "double" in double-entry: every event is recorded twice, from two sides (where the value came from and where it went).

## Step 5: The five account types
Every account is one of five types:

| Type | Meaning | Example |
|---|---|---|
| **Asset** | What the company owns | Cash, Accounts receivable (money customers owe you) |
| **Liability** | What it owes | Accounts payable, loans, Deferred revenue |
| **Equity** | Owners' claim on what's left | Founder capital, Retained earnings |
| **Revenue** (income) | Money earned | Subscription revenue |
| **Expense** | Costs of operating | Salaries, AWS, Rent |

## Step 6: Normal balance (which side increases an account)
- **Assets and Expenses:** debit increases, credit decreases.
- **Liabilities, Equity, Revenue:** credit increases, debit decreases.

Mnemonic: the accounting equation **Assets = Liabilities + Equity**. Assets sit on the left side of the equals sign, so they grow with left (debit). The other side grows with right (credit). Revenue and expenses are temporary sub-accounts of equity: revenue raises equity, expenses lower it.

## Step 7: Worked examples
Written as `Dr` (debit) / `Cr` (credit):

1. **Investors wire $100,000 for shares.**
   - Dr Cash 100,000 (asset up)
   - Cr Founder/Investor capital 100,000 (equity up)

2. **Pay $5,000 rent in cash.**
   - Dr Rent expense 5,000 (expense up)
   - Cr Cash 5,000 (asset down)

3. **Customer is invoiced $2,000, hasn't paid yet.**
   - Dr Accounts receivable 2,000 (asset up)
   - Cr Revenue 2,000 (revenue up)

4. **Customer pays that invoice.**
   - Dr Cash 2,000
   - Cr Accounts receivable 2,000
   (Revenue isn't touched again. It was already recorded in step 3.)

Each one nets to zero, and the equation Assets = Liabilities + Equity holds after every one.

## Step 8: How to read the ledger itself
- **Journal:** chronological list of transactions (your append-only event log).
- **General ledger (GL):** the same entries grouped by account (a materialized view).
- **Trial balance:** a report listing every account's balance. Total debits must equal total credits. It works as a test suite for the books.
- **Balance sheet** (assets, liabilities, equity at a point in time) and **income statement / P&L** (revenue minus expenses over a period) are views derived from those balances.

## What it is *not*
- Not "debit = money out". Debiting Cash *increases* cash.
- Not a record of cash only. Revenue is recorded when earned (accrual basis), even if the cash arrives later.
- Corrections are not edits. You post a new reversing entry, as in an immutable log.

## You now know
Accounts, transactions made of debit/credit entries that must balance, the five account types and which side increases each, and how the journal, ledger, and trial balance relate.

**Mini-check:** A customer prepays you $1,200 for a year of service you haven't delivered yet. Which account would you debit, which would you credit, and what type is the credit account?

---

Thanks, that tells me where to start. My last message moved too fast, so ignore its mini-check. Let's go slower, in code you already read.

## The one idea underneath everything

A ledger is a list of **transactions**. Each transaction is a list of **lines**. Each line says "this much moved in or out of this named bucket." The one rule is that the amounts in a transaction must sum to zero.

```python
# Signed amounts: + means "left side" (debit), - means "right side" (credit)
txn = {
    "date": "2026-01-05",
    "memo": "Investors wire money for shares",
    "lines": [
        {"account": "Cash",            "amount": +100_000},
        {"account": "Investor capital", "amount": -100_000},
    ],
}
assert sum(l["amount"] for l in txn["lines"]) == 0   # the whole rule
```

- **Account** is a named bucket, like a dict key: `"Cash"`, `"Rent"`.
- **Debit** and **credit** are only the sign. Debit is `+` (the left column on paper). Credit is `-` (the right column). They don't mean "good" or "bad", and a debit to Cash doesn't mean money left.
- **Balance** of an account is the sum of all its lines so far.

Every real ledger is this structure, plus two practical details that I'll cover next:

1. Accounts come in 5 types, so you can tell what each bucket means.
2. Printed ledgers show debits and credits as two positive columns instead of one signed number.

## Why two sides?

Money never appears from nowhere. It comes *from* somewhere and goes *to* somewhere. The two lines record both ends of the movement. If a transaction doesn't balance, you know something was left out, much like a failed checksum.

## Mini-check

Using the signed convention above (debit `+`, credit `-`), here is a transaction:

```python
{"memo": "Paid $5,000 office rent from bank", 
 "lines": [{"account": "Rent expense", "amount": +5000},
           {"account": "Cash",         "amount": ?}]}
```

What number goes where the `?` is?

---

Your scenario is right, and your reasoning shows the exact trap, so it's worth fixing now.

**Right:** Cash goes up £100 and revenue goes up £100.

**Wrong:** "Both increase, so both are debits." Debit isn't a synonym for "increase." If both lines were debits, they'd be `+100` and `+100`, which sums to 200, and our one rule (sum to zero) would reject it.

The correct entry is:

```python
{"account": "Cash",    "amount": +100},   # debit
{"account": "Revenue", "amount": -100},   # credit
```

Revenue went *up* but is recorded as a negative number. The sign records which side the line is on, not whether the bucket grew. Accountants call revenue a "credit-balance" account, and reports print it as a positive 100 for readability. Raw ledger data, like the code above, keeps the minus sign.

Here is the rule of thumb to hold onto for now:

| Bucket | Meaning | Grows with |
|---|---|---|
| Cash (an **asset**: something you own) | what you have | debit (`+`) |
| Rent (an **expense**: a cost) | what you spent | debit (`+`) |
| Revenue (**income**: money earned) | what you earned | credit (`-`) |
| Investor capital (**equity**: owners' stake) | what owners put in | credit (`-`) |

There are two more types, liabilities and the exact meaning of equity, and I'll cover them later. For now, the pattern is that things you own and costs you incur grow on the debit side, and sources (earnings, owner money) grow on the credit side.

**Your turn:** You pay £30 in cash for a software subscription, and the bucket for that cost is called "Software expense." Write the two lines with their signs, in the same format as above.
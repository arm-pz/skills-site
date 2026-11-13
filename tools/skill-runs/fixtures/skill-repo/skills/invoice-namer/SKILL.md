---
name: invoice-namer
description: Renames invoice PDFs in a folder to a consistent pattern (YYYY-MM-DD_customer_number.pdf) by reading the date, customer and invoice number from each file. Use when someone asks to rename, tidy or standardise invoice files. Not for extracting line items or totals.
---

# Invoice Namer

1. List the PDFs in the folder the user names.
2. For each file, read the invoice date, customer name and invoice number.
3. Propose the new names in a table and wait for the user's go-ahead before renaming anything.
4. Rename only after approval; never overwrite an existing file.

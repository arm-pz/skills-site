#!/usr/bin/env python3
"""Clean a provider leads CSV.

Drops role inboxes, free-mail addresses, companies over --max-employees,
rows with no usable email or unparseable employee count, and dedupes by
lowercased email (first occurrence wins). Standard library only.
"""
import argparse
import csv
import sys

ROLE_LOCALPARTS = frozenset("""
info admin administrator sales support contact hello help office team mail
enquiries enquiry inquiries inquiry marketing billing accounts accounting
finance hr jobs careers recruitment press media pr legal privacy security
abuse postmaster webmaster noreply no-reply donotreply do-not-reply service
services customerservice orders booking bookings reception general
""".split())

FREE_DOMAINS = frozenset("""
gmail.com googlemail.com yahoo.com yahoo.co.uk yahoo.ie ymail.com
hotmail.com hotmail.co.uk outlook.com live.com live.co.uk msn.com
aol.com icloud.com me.com mac.com proton.me protonmail.com pm.me
gmx.com gmx.net gmx.co.uk mail.com zoho.com yandex.com fastmail.com
btinternet.com sky.com talktalk.net virginmedia.com eircom.net
""".split())

REASONS = ("no_email", "role_inbox", "free_mail", "bad_employees",
           "over_limit", "duplicate")


def split_email(raw):
    """Return (localpart, domain) lowercased, or None if not a usable address."""
    email = (raw or "").strip().lower()
    local, sep, domain = email.rpartition("@")
    if not sep or not local or not domain:
        return None
    return local, domain


def parse_employees(raw):
    """Parse '1,200' / '250' / '250.0' to int; None if missing or invalid."""
    text = (raw or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def is_role_inbox(local):
    # Compare the part before any +tag, so sales+eu@ is still a role inbox.
    return local.split("+", 1)[0] in ROLE_LOCALPARTS


def is_free_mail(domain):
    return domain in FREE_DOMAINS


def clean_rows(rows, max_employees=500):
    """Return (kept_rows, dropped_counts). Pure function over dict rows."""
    kept = []
    dropped = dict.fromkeys(REASONS, 0)
    seen = set()
    for row in rows:
        parts = split_email(row.get("email"))
        if parts is None:
            dropped["no_email"] += 1
            continue
        local, domain = parts
        if is_role_inbox(local):
            dropped["role_inbox"] += 1
            continue
        if is_free_mail(domain):
            dropped["free_mail"] += 1
            continue
        employees = parse_employees(row.get("employees"))
        if employees is None:
            dropped["bad_employees"] += 1
            continue
        if employees > max_employees:
            dropped["over_limit"] += 1
            continue
        key = f"{local}@{domain}"
        if key in seen:
            dropped["duplicate"] += 1
            continue
        seen.add(key)
        kept.append(row)
    return kept, dropped


def clean_file(src, dst, max_employees=500):
    with open(src, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        missing = [c for c in ("email", "employees") if c not in fields]
        if missing:
            raise ValueError(f"{src}: missing required column(s): {', '.join(missing)}")
        kept, dropped = clean_rows(reader, max_employees)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept)
    return len(kept), dropped


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("input", help="provider CSV, e.g. leads_providerA.csv")
    p.add_argument("-o", "--output", default="clean.csv",
                   help="output path (default: clean.csv)")
    p.add_argument("--max-employees", type=int, default=500,
                   help="drop companies with more employees than this (default: 500)")
    args = p.parse_args(argv)
    try:
        n, dropped = clean_file(args.input, args.output, args.max_employees)
    except (OSError, ValueError, csv.Error) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    summary = ", ".join(f"{k}={v}" for k, v in dropped.items() if v) or "none"
    print(f"wrote {n} rows to {args.output}; dropped: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

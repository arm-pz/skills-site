"""Ground truth for the checkout A/B fixture: two-proportion z-tests, overall and per device,
with and without the day-9 outage."""
import csv, math, sys
rows = list(csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else "checkout_test.csv")))
def z(rows, dev=None, drop9=False):
    s = {"A": [0, 0], "B": [0, 0]}
    for r in rows:
        if dev and r["device"] != dev: continue
        if drop9 and r["date"].endswith("-09"): continue
        s[r["variant"]][0] += int(r["orders"]); s[r["variant"]][1] += int(r["sessions"])
    (xa, na), (xb, nb) = s["A"], s["B"]
    pa, pb = xa / na, xb / nb; p = (xa + xb) / (na + nb)
    zz = (pb - pa) / math.sqrt(p * (1 - p) * (1 / na + 1 / nb))
    pv = math.erfc(abs(zz) / math.sqrt(2))
    return f"A {pa:.4f} ({xa}/{na})  B {pb:.4f} ({xb}/{nb})  lift {100*(pb/pa-1):+.1f}%  z {zz:.2f}  p {pv:.4f}"
for dev in (None, "mobile", "desktop"):
    for drop in (False, True):
        print(f"{dev or 'all':8} {'excl day 9' if drop else 'all days  '}  {z(rows, dev, drop)}")
day9 = [r for r in rows if r["date"].endswith("-09") and r["variant"] == "B"]
print("day 9, variant B orders:", [r["orders"] for r in day9], "(tracking outage planted)")

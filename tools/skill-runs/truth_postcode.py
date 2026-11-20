"""Ground truth for do-better: import is_uk_postcode from postcode.py and run fixed cases."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("p", "postcode.py"); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
good = ["M1 1AE", "W1A 0AX", "SW1A 1AA", "B33 8TH", "CR2 6XH", "DN55 1PT", "ec1a 1bb", "EC1A1BB", "GIR 0AA"]
bad = ["SW1A 1AAXYZ", "12345", "M1 1A", "QQ1 1AA", ""]
fails = [s for s in good if not m.is_uk_postcode(s)] + [s for s in bad if m.is_uk_postcode(s)]
print(f"{len(good)+len(bad)-len(fails)}/{len(good)+len(bad)} cases right; wrong on: {fails}")
sys.exit(1 if fails else 0)

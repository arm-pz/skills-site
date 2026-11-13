import re
def is_uk_postcode(s):
    return bool(re.match(r"[A-Z]{2}[0-9]{2} [0-9][A-Z]{2}", s))

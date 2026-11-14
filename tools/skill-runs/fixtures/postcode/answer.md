Earlier answer I got for "write a Python function that validates UK postcodes":

```python
import re
def is_uk_postcode(s):
    return bool(re.match(r"[A-Z]{2}[0-9]{2} [0-9][A-Z]{2}", s))
```
It rejects "M1 1AE" and "W1A 0AX" and lowercase input, and it accepts "SW1A 1AAXYZ". I need a version that is right.

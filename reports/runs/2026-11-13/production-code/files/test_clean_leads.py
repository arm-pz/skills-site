import csv
import os
import tempfile
import unittest

import clean_leads as cl


def row(email, employees="100", **kw):
    d = {"first_name": "A", "email": email, "employees": employees}
    d.update(kw)
    return d


class CleanRowsTests(unittest.TestCase):
    def test_role_inboxes_dropped(self):
        rows = [row("info@x.example"), row("Sales@x.example"),
                row("sales+eu@x.example"), row("jo@x.example")]
        kept, d = cl.clean_rows(rows)
        self.assertEqual([r["email"] for r in kept], ["jo@x.example"])
        self.assertEqual(d["role_inbox"], 3)

    def test_name_starting_with_role_word_kept(self):
        kept, _ = cl.clean_rows([row("information.guy@x.example")])
        self.assertEqual(len(kept), 1)

    def test_free_mail_dropped(self):
        kept, d = cl.clean_rows([row("a@gmail.com"), row("b@Yahoo.co.uk"),
                                 row("c@corp.example")])
        self.assertEqual(len(kept), 1)
        self.assertEqual(d["free_mail"], 2)

    def test_employee_limit_inclusive_and_configurable(self):
        rows = [row("a@x.example", "500"), row("b@x.example", "501"),
                row("c@x.example", "1,200")]
        kept, d = cl.clean_rows(rows)
        self.assertEqual([r["email"] for r in kept], ["a@x.example"])
        self.assertEqual(d["over_limit"], 2)
        kept, _ = cl.clean_rows(rows, max_employees=1000)
        self.assertEqual(len(kept), 2)

    def test_bad_employees_dropped(self):
        kept, d = cl.clean_rows([row("a@x.example", ""), row("b@x.example", "many")])
        self.assertEqual(kept, [])
        self.assertEqual(d["bad_employees"], 2)

    def test_dedupe_case_insensitive_first_wins(self):
        rows = [row("Jo@X.example", first_name="First"),
                row("jo@x.example", first_name="Second")]
        kept, d = cl.clean_rows(rows)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["first_name"], "First")
        self.assertEqual(d["duplicate"], 1)

    def test_filtered_row_does_not_shadow_later_duplicate(self):
        rows = [row("jo@x.example", "9999"), row("jo@x.example", "10")]
        kept, _ = cl.clean_rows(rows)
        self.assertEqual(len(kept), 1)

    def test_missing_or_malformed_email(self):
        kept, d = cl.clean_rows([row(""), row("nope"), row("@x.example"), {"employees": "1"}])
        self.assertEqual(kept, [])
        self.assertEqual(d["no_email"], 4)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.src = os.path.join(self.tmp.name, "in.csv")
        self.dst = os.path.join(self.tmp.name, "clean.csv")

    def write(self, text):
        with open(self.src, "w", encoding="utf-8-sig", newline="") as f:
            f.write(text)

    def read_out(self):
        with open(self.dst, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_end_to_end_preserves_columns(self):
        self.write("first_name,company,employees,email\n"
                   "Ann,A,10,ann@a.example\n"
                   "Info,B,10,info@b.example\n"
                   "Bob,C,900,bob@c.example\n"
                   "Cy,D,10,cy@gmail.com\n"
                   "Ann2,A,10,ANN@a.example\n")
        self.assertEqual(cl.main([self.src, "-o", self.dst]), 0)
        out = self.read_out()
        self.assertEqual([r["email"] for r in out], ["ann@a.example"])
        self.assertEqual(list(out[0]), ["first_name", "company", "employees", "email"])

    def test_max_employees_flag(self):
        self.write("employees,email\n900,bob@c.example\n")
        cl.main([self.src, "-o", self.dst, "--max-employees", "1000"])
        self.assertEqual(len(self.read_out()), 1)

    def test_missing_column_returns_error(self):
        self.write("name,mail\nx,y\n")
        self.assertEqual(cl.main([self.src, "-o", self.dst]), 1)
        self.assertFalse(os.path.exists(self.dst))

    def test_missing_file_returns_error(self):
        self.assertEqual(cl.main([os.path.join(self.tmp.name, "nope.csv")]), 1)


if __name__ == "__main__":
    unittest.main()

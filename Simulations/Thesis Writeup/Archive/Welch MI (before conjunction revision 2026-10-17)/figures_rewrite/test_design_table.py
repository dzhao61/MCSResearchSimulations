"""Check the simplified design table without arithmetic annotations."""

import unittest

import audit_evidence as audit


class DesignTableTests(unittest.TestCase):
    def setUp(self):
        self.source = (audit.HERE.parent / "chapters_rewrite/05_experimental_design.tex").read_text()
        self.counts = audit.REPORTED_DISPLAY.groupby("section").agg(
            unique_configurations=("configuration_id", "nunique"),
        )

    def test_plain_counts_match_saved_settings(self):
        audit.check_family_counts(self.counts, source=self.source)
        self.assertNotIn(r"\familycount", self.source)
        self.assertNotIn("shape/pattern choices", self.source)

    def test_incorrect_count_is_rejected(self):
        incorrect = self.source.replace("Main & 504 &", "Main & 648 &")
        self.assertNotEqual(incorrect, self.source)
        with self.assertRaises(AssertionError):
            audit.check_family_counts(self.counts, source=incorrect)


if __name__ == "__main__":
    unittest.main()

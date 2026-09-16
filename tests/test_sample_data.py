"""Integrity checks for the repository's bundled Online Retail sample.

These tests intentionally use only the Python standard library so contributors can
validate the sample before installing the notebook's heavier ML dependencies.
"""

import csv
import math
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data_sample.csv"
EXPECTED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]


class SampleDataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SAMPLE.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            cls.fieldnames = reader.fieldnames
            cls.rows = list(reader)

    def test_schema_matches_notebook_input(self):
        self.assertEqual(self.fieldnames, EXPECTED_COLUMNS)

    def test_sample_contains_usable_rows(self):
        self.assertGreater(len(self.rows), 0)
        for row in self.rows:
            self.assertTrue(row["InvoiceNo"].strip())
            self.assertTrue(row["StockCode"].strip())
            self.assertTrue(row["Country"].strip())

    def test_numeric_fields_are_finite_and_sensible(self):
        for row in self.rows:
            quantity = int(row["Quantity"])
            unit_price = float(row["UnitPrice"])
            customer_id = float(row["CustomerID"])

            self.assertNotEqual(quantity, 0)
            self.assertTrue(math.isfinite(unit_price))
            self.assertGreaterEqual(unit_price, 0)
            self.assertTrue(math.isfinite(customer_id))

    def test_invoice_dates_are_parseable(self):
        for row in self.rows:
            datetime.strptime(row["InvoiceDate"], "%m/%d/%Y %H:%M")


if __name__ == "__main__":
    unittest.main()

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import REQUIRED_COLUMNS, validate_dataset


class ValidateDatasetTests(unittest.TestCase):
    def _write_csv(self, rows, fieldnames=None):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "data.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames or sorted(REQUIRED_COLUMNS))
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_valid_row_passes(self):
        path = self._write_csv(
            [
                {
                    "InvoiceNo": "536365",
                    "StockCode": "85123A",
                    "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
                    "Quantity": "6",
                    "InvoiceDate": "12/1/2010 8:26",
                    "UnitPrice": "2.55",
                    "CustomerID": "17850.0",
                    "Country": "United Kingdom",
                }
            ]
        )
        rows_checked, errors = validate_dataset(path)
        self.assertEqual(rows_checked, 1)
        self.assertEqual(errors, [])

    def test_missing_columns_fail_fast(self):
        path = self._write_csv([], fieldnames=["InvoiceNo", "StockCode"])
        rows_checked, errors = validate_dataset(path)
        self.assertEqual(rows_checked, 0)
        self.assertTrue(errors)
        self.assertIn("missing required columns", errors[0])

    def test_invalid_numeric_and_date_values_are_reported(self):
        path = self._write_csv(
            [
                {
                    "InvoiceNo": "1",
                    "StockCode": "A",
                    "Description": "Example",
                    "Quantity": "six",
                    "InvoiceDate": "not-a-date",
                    "UnitPrice": "free",
                    "CustomerID": "abc",
                    "Country": "United Kingdom",
                }
            ]
        )
        rows_checked, errors = validate_dataset(path)
        self.assertEqual(rows_checked, 1)
        self.assertGreaterEqual(len(errors), 4)


if __name__ == "__main__":
    unittest.main()

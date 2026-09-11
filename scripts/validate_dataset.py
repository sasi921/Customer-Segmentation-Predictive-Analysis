"""Validate an Online Retail CSV before running the analysis notebook.

The notebook expects the UCI Online Retail schema. This utility provides a quick,
actionable preflight check so missing columns or malformed numeric/date values are
caught before a long notebook run.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

REQUIRED_COLUMNS = {
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
}

DATE_FORMATS = ("%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S")


def _parse_date(value: str) -> None:
    for date_format in DATE_FORMATS:
        try:
            datetime.strptime(value, date_format)
            return
        except ValueError:
            continue
    raise ValueError(f"unsupported InvoiceDate format: {value!r}")


def validate_dataset(path: Path, max_rows: int | None = None) -> tuple[int, list[str]]:
    """Return ``(rows_checked, errors)`` for *path*.

    ``max_rows`` can be used for a fast smoke check on very large files. ``None``
    validates the entire file.
    """
    errors: list[str] = []

    if not path.exists():
        return 0, [f"file does not exist: {path}"]

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            return 0, [f"missing required columns: {', '.join(missing)}"]

        rows_checked = 0
        for line_number, row in enumerate(reader, start=2):
            if max_rows is not None and rows_checked >= max_rows:
                break
            rows_checked += 1

            try:
                int(row["Quantity"])
            except (TypeError, ValueError):
                errors.append(f"line {line_number}: invalid Quantity {row['Quantity']!r}")

            try:
                unit_price = float(row["UnitPrice"])
                if unit_price < 0:
                    errors.append(f"line {line_number}: UnitPrice must be non-negative")
            except (TypeError, ValueError):
                errors.append(f"line {line_number}: invalid UnitPrice {row['UnitPrice']!r}")

            try:
                _parse_date(row["InvoiceDate"])
            except ValueError as exc:
                errors.append(f"line {line_number}: {exc}")

            customer_id = row["CustomerID"].strip()
            if customer_id:
                try:
                    float(customer_id)
                except ValueError:
                    errors.append(
                        f"line {line_number}: invalid CustomerID {row['CustomerID']!r}"
                    )

    if rows_checked == 0:
        errors.append("dataset contains no data rows")

    return rows_checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("data.csv"),
        help="CSV to validate (default: data.csv)",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="validate only the first N data rows for a quick smoke check",
    )
    args = parser.parse_args()

    rows_checked, errors = validate_dataset(args.path, args.max_rows)
    if errors:
        print(f"Validation failed for {args.path} after checking {rows_checked} row(s):")
        for error in errors[:20]:
            print(f"  - {error}")
        if len(errors) > 20:
            print(f"  - ... and {len(errors) - 20} more error(s)")
        return 1

    print(f"Validation passed: {args.path} ({rows_checked} row(s) checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

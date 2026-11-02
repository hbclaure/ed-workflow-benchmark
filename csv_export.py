"""Export literature JSON records as one CSV row per paper."""

import argparse
import csv
import json
from pathlib import Path


def export_json_to_csv(json_path="output.json", csv_path=None):
    """Export a JSON list of records and return the output Path.

    Nested dictionaries become columns such as ``PubDate.year``. Lists and
    empty dictionaries are stored as JSON text, preserving their contents.
    Columns include fields from every record; missing values and JSON nulls
    become blank cells. An empty list produces no CSV headers or rows.
    """
    json_path = Path(json_path)
    csv_path = Path(csv_path) if csv_path is not None else json_path.with_suffix(".csv")
    if json_path.resolve() == csv_path.resolve():
        raise ValueError("The CSV output path must differ from the JSON input path.")

    with json_path.open(encoding="utf-8-sig") as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError("Expected a JSON list of paper records.")
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a JSON object.")

    def flatten_record(record, prefix=""):
        row = {}
        for key, value in record.items():
            column = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict) and value:
                row.update(flatten_record(value, column))
            elif isinstance(value, (list, dict)):
                row[column] = json.dumps(value, ensure_ascii=False)
            else:
                row[column] = value
        return row

    rows = [flatten_record(record) for record in records]
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    with csv_path.open("w", newline="", encoding="utf-8-sig") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
        writer.writerows(rows)
    return csv_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", nargs="?", default="output.json")
    parser.add_argument("csv_path", nargs="?", default=None)
    args = parser.parse_args()
    print(export_json_to_csv(args.json_path, args.csv_path))

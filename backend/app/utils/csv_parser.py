"""Utilitaires de parsing CSV."""

import csv
import io
from typing import Dict, List, Tuple

REQUIRED_COLUMNS = {"date", "description", "amount"}
OPTIONAL_COLUMNS = {"category"}
SUPPORTED_SEPARATORS = [",", ";"]


def detect_csv_delimiter(content: str) -> str:
    sample = "\n".join(content.splitlines()[:5])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=SUPPORTED_SEPARATORS)
        return dialect.delimiter
    except csv.Error:
        comma_count = sample.count(",")
        semicolon_count = sample.count(";")
        return ";" if semicolon_count > comma_count else ","


def parse_csv_content(content: str) -> Tuple[List[Dict[str, str]], str, List[str]]:
    delimiter = detect_csv_delimiter(content)
    reader = csv.DictReader(io.StringIO(content), delimiter=delimiter)

    if not reader.fieldnames:
        return [], delimiter, ["Le fichier CSV doit contenir un en-tête."]

    normalized_fields = {field.strip().lower() for field in reader.fieldnames if field}
    missing_columns = REQUIRED_COLUMNS - normalized_fields
    if missing_columns:
        return [], delimiter, [
            f"Colonnes obligatoires manquantes: {', '.join(sorted(missing_columns))}"
        ]

    unknown_columns = normalized_fields - REQUIRED_COLUMNS - OPTIONAL_COLUMNS
    errors = []
    if unknown_columns:
        errors.append(f"Colonnes non reconnues ignorées: {', '.join(sorted(unknown_columns))}")

    rows = []
    for row in reader:
        normalized = {(k or "").strip().lower(): (v or "") for k, v in row.items()}
        rows.append({
            "date": normalized.get("date", ""),
            "description": normalized.get("description", ""),
            "amount": normalized.get("amount", ""),
            "category": normalized.get("category", ""),
        })

    return rows, delimiter, errors

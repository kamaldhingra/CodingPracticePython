import argparse
import csv
import json
import re
from pathlib import Path


# Common timestamp patterns seen in logs.
TIMESTAMP_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?\b"),
    re.compile(r"\b\d{2}/\d{2}/\d{4}[ T]\d{2}:\d{2}:\d{2}\b"),
    re.compile(r"\b[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\b"),
]


def extract_timestamp(line: str) -> str:
    for pattern in TIMESTAMP_PATTERNS:
        match = pattern.search(line)
        if match:
            return match.group(0)
    return "N/A"


def build_error_code_pattern(codes: list[str]) -> re.Pattern:
    escaped_codes = [re.escape(code.strip()) for code in codes if code.strip()]
    if not escaped_codes:
        raise ValueError("At least one valid error code is required.")

    # Match exact codes, commonly wrapped as [CODE], (CODE), or code=CODE.
    return re.compile(
        rf"(?:\[|\(|\bcode\s*=\s*|\berror\s*=\s*)?({'|'.join(escaped_codes)})(?:\]|\))?\b",
        re.IGNORECASE,
    )


def extract_message(line: str, code_match: re.Match) -> str:
    trailing_text = line[code_match.end():].strip()
    trailing_text = re.sub(r"^[\]\)\s\-:|]+", "", trailing_text)
    if trailing_text:
        return trailing_text

    # Fallback: keep the whole line when no clean trailing message exists.
    return line.strip()


def parse_log_file(log_file: Path, error_codes: list[str]) -> list[dict]:
    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    code_pattern = build_error_code_pattern(error_codes)
    results = []

    with log_file.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            code_match = code_pattern.search(line)
            if not code_match:
                continue

            results.append(
                {
                    "line_number": line_number,
                    "timestamp": extract_timestamp(line),
                    "error_code": code_match.group(1),
                    "error_message": extract_message(line, code_match),
                }
            )

    return results


def write_csv(records: list[dict], output_file: Path) -> None:
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["line_number", "timestamp", "error_code", "error_message"],
        )
        writer.writeheader()
        writer.writerows(records)


def write_json(records: list[dict], output_file: Path) -> None:
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Parse a log file, find specific error codes, and store timestamp + error message."
        )
    )
    parser.add_argument("log_file", help="Path to the input log file")
    parser.add_argument(
        "--codes",
        required=True,
        help="Comma-separated error codes to search (example: E101,E404,ERR_TIMEOUT)",
    )
    parser.add_argument(
        "--output",
        default="matched_errors.csv",
        help="Output file path (default: matched_errors.csv)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv)",
    )

    args = parser.parse_args()
    codes = [code.strip() for code in args.codes.split(",") if code.strip()]

    records = parse_log_file(Path(args.log_file), codes)

    output_file = Path(args.output)
    if args.format == "json":
        write_json(records, output_file)
    else:
        write_csv(records, output_file)

    print(f"Found {len(records)} matching log entries.")
    print(f"Saved results to: {output_file}")


if __name__ == "__main__":
    main()

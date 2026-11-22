import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


TIMESTAMP_FORMATS = [
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S,%f",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S,%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
]

MONTHS = {
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
}


def clean_token(token: str) -> str:
    return token.strip("[](){}<>,;|\t\n\r")


def is_month_day_time(candidate: str) -> bool:
    parts = candidate.split()
    if len(parts) != 3:
        return False

    month, day, time_part = parts
    if month.upper() not in MONTHS:
        return False

    if not day.isdigit():
        return False
    day_value = int(day)
    if day_value < 1 or day_value > 31:
        return False

    time_segments = time_part.split(":")
    if len(time_segments) != 3:
        return False
    if not all(segment.isdigit() for segment in time_segments):
        return False

    hour, minute, second = map(int, time_segments)
    if hour < 0 or hour > 23:
        return False
    if minute < 0 or minute > 59:
        return False
    if second < 0 or second > 59:
        return False

    return True


def extract_timestamp(line: str) -> str:
    tokens = line.split()
    candidates = []

    for token in tokens:
        cleaned = clean_token(token)
        if cleaned:
            candidates.append(cleaned)

    for i in range(len(tokens) - 1):
        part1 = clean_token(tokens[i])
        part2 = clean_token(tokens[i + 1])
        if part1 and part2:
            candidates.append(f"{part1} {part2}")

    for i in range(len(tokens) - 2):
        part1 = clean_token(tokens[i])
        part2 = clean_token(tokens[i + 1])
        part3 = clean_token(tokens[i + 2])
        if part1 and part2 and part3:
            candidates.append(f"{part1} {part2} {part3}")

    for candidate in candidates:
        if is_month_day_time(candidate):
            return candidate

        for time_format in TIMESTAMP_FORMATS:
            try:
                datetime.strptime(candidate, time_format)
                return candidate
            except ValueError:
                continue

    return "N/A"


def build_error_code_lookup(codes: list[str]) -> dict[str, str]:
    lookup = {}
    for code in codes:
        cleaned = code.strip()
        if cleaned:
            lookup[cleaned.upper()] = cleaned

    if not lookup:
        raise ValueError("At least one valid error code is required.")

    return lookup


def find_error_code_in_line(line: str, lookup: dict[str, str]) -> str | None:
    separators = "[](){}=,:|;\t"
    translation_table = str.maketrans({char: " " for char in separators})
    normalized_line = line.translate(translation_table)

    for raw_token in normalized_line.split():
        token = raw_token.strip(".!?\"'`")
        if token.upper() in lookup:
            return lookup[token.upper()]

    return None


def extract_message(line: str, matched_code: str) -> str:
    line_upper = line.upper()
    code_upper = matched_code.upper()
    code_index = line_upper.find(code_upper)

    if code_index == -1:
        return line.strip()

    trailing_text = line[code_index + len(matched_code):].strip()

    while trailing_text and trailing_text[0] in "] )-:|\t":
        trailing_text = trailing_text[1:]

    trailing_text = trailing_text.strip()
    if trailing_text:
        return trailing_text

    return line.strip()


def parse_log_file(log_file: Path, error_codes: list[str]) -> list[dict]:
    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    code_lookup = build_error_code_lookup(error_codes)
    results = []

    with log_file.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            matched_code = find_error_code_in_line(line, code_lookup)
            if not matched_code:
                continue

            results.append(
                {
                    "line_number": line_number,
                    "timestamp": extract_timestamp(line),
                    "error_code": matched_code,
                    "error_message": extract_message(line, matched_code),
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

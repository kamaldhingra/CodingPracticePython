"""
Log File Parser
----------------
Parses a log file (without using regex) to search for specific error codes
and stores their timestamps and messages.

Expected log line format:
    YYYY-MM-DD HH:MM:SS LEVEL message...

Error codes can show up in the message in a few different styles, e.g.:
    [E404] ...
    code=E500 ...
    (ERR_TIMEOUT) ...
"""

LOG_FILE = "sample_logfile.log"

# Error codes we care about. Add/remove codes here as needed.
ERROR_CODES_OF_INTEREST = ["E404", "E500", "ERR_TIMEOUT", "AUTH_401"]


def clean_token(token):
    """Strip common wrapping characters like [], (), and trailing punctuation."""
    return token.strip("[](),:;")


def extract_error_codes(message, codes_of_interest):
    """
    Find which of the codes_of_interest appear in the message.
    Uses plain word splitting + substring checks (no regex).
    """
    found_codes = []
    for word in message.split():
        cleaned = clean_token(word)
        # Handle "code=E500" style tokens
        if cleaned.startswith("code="):
            cleaned = cleaned.split("=", 1)[1]
        if cleaned in codes_of_interest:
            found_codes.append(cleaned)
    return found_codes


def parse_log_line(line):
    """
    Split a single log line into (timestamp, level, message).
    Expected format: 'YYYY-MM-DD HH:MM:SS LEVEL message...'
    Returns None if the line doesn't match the expected shape.
    """
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return None  # malformed/blank line, skip it

    date, time, level, message = parts
    timestamp = f"{date} {time}"
    return timestamp, level, message


def parse_log_file(file_path, codes_of_interest):
    """
    Read the log file and collect entries for the given error codes.

    Returns a dict:
        {error_code: [{"timestamp": ..., "level": ..., "message": ...}, ...]}
    """
    results = {code: [] for code in codes_of_interest}

    with open(file_path, "r") as f:
        for line in f:
            parsed = parse_log_line(line)
            if not parsed:
                continue

            timestamp, level, message = parsed
            found_codes = extract_error_codes(message, codes_of_interest)

            for code in found_codes:
                results[code].append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message
                })

    return results


def print_report(results):
    print("=" * 60)
    print("ERROR CODE REPORT")
    print("=" * 60)

    for code, entries in results.items():
        print(f"\nError Code: {code}  (occurrences: {len(entries)})")
        if not entries:
            print("  No occurrences found.")
            continue
        for entry in entries:
            print(f"  [{entry['timestamp']}] ({entry['level']}) {entry['message']}")


if __name__ == "__main__":
    report = parse_log_file(LOG_FILE, ERROR_CODES_OF_INTEREST)
    print_report(report)

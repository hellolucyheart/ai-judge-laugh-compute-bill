#!/usr/bin/env python3
"""One line of comedy for make.fun's "Make the Judge Laugh in One Line".

The entry is the writing itself: a single original joke of at most 200
characters, spoken straight to the AI judge that reads it. Nothing is
built, installed or fetched — the program only checks the line against
the sealed gate (UTF-8, 1 to 200 characters, one line) and writes it to
/output/entry.txt, falling back to entry.txt beside this file when
/output cannot be written, e.g. on a developer machine.

Deterministic by design: every run writes the same bytes, so the two
grading runs match exactly.
"""

import sys
from pathlib import Path

LINE = "I asked the AI judge to laugh at my joke, and it did \u2014 then it billed me for the compute."

LIMIT = 200
PRIMARY = Path("/output") / "entry.txt"


def normalise(raw):
    """Squeeze any stray whitespace to single spaces.

    The gate counts every character, so the line must be exactly the
    joke as written — no leading or trailing space, no double space.
    """
    return " ".join(raw.split())


def gate(line):
    """Name the reason the sealed gate would reject this line, else None."""
    if not line.strip():
        return "the line is empty"
    if len(line) > LIMIT:
        return "the line is %d chars, over the %d limit" % (len(line), LIMIT)
    if "\n" in line or "\r" in line:
        return "the line must be a single line"
    return None


def emit(line):
    """Write the line plus one newline; return the path written."""
    payload = line + "\n"
    try:
        PRIMARY.parent.mkdir(parents=True, exist_ok=True)
        PRIMARY.write_text(payload, encoding="utf-8")
        return PRIMARY
    except OSError:
        fallback = Path(__file__).resolve().parent / "entry.txt"
        fallback.write_text(payload, encoding="utf-8")
        return fallback


def main():
    line = normalise(LINE)
    problem = gate(line)
    if problem is not None:
        print("error: %s" % problem, file=sys.stderr)
        return 1
    path = emit(line)
    print("wrote %d chars to %s" % (len(line), path))
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

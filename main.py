#!/usr/bin/env python3
"""Office-joke one-liner entry: the raise that arrived as pizza.

Writes the winning line to $MAKEFUN_OUTPUT_DIR/entry.txt, one line
terminated by a newline, exactly as the competition expects it.
"""

import hashlib
import os
import sys

# The joke, assembled from its two beats so the punchline lands on the
# second clause: HR's "generosity", then the hourly rate in slices.
_RAISE_SETUP = "I asked for a raise and HR threw me a pizza party instead."
_PUNCHLINE = "I now earn 0.4 slices an hour — before tax."
JOKE_LINE = f"{_RAISE_SETUP} {_PUNCHLINE}"

# Guard: the entry is a one-liner, so it must stay on a single line and
# within the competition's character budget.
MAX_ENTRY_CHARS = 140

# sha256 of the exact entry line plus its trailing newline; the write is
# verified against this so a silent encoding slip can never ship.
EXPECTED_SHA256 = "835800bb973a000f36ea08906cf7122c95f588bb2cce77d1fb6935b9168b14cb"


def _output_dir() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not out_dir:
        sys.stderr.write("MAKEFUN_OUTPUT_DIR is not set\n")
        raise SystemExit(2)
    return out_dir


def _sanity_check(line: str) -> None:
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_ENTRY_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_ENTRY_CHARS} limit")
    if "—" not in line:
        raise ValueError("punchline dash missing; entry text was altered")


def write_entry() -> str:
    _sanity_check(JOKE_LINE)
    out_dir = _output_dir()
    os.makedirs(out_dir, exist_ok=True)
    entry_path = os.path.join(out_dir, "entry.txt")
    # Trailing newline: the file is one complete line, not a fragment.
    payload = JOKE_LINE + "\n"
    with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(f"wrote {entry_path} ({len(payload)} bytes, sha256 {digest})")
    # Read the file back and prove the bytes on disk are the bytes intended.
    with open(entry_path, "rb") as handle:
        on_disk = hashlib.sha256(handle.read()).hexdigest()
    if on_disk != EXPECTED_SHA256:
        raise SystemExit(f"entry hash mismatch: got {on_disk}, want {EXPECTED_SHA256}")
    return entry_path


if __name__ == "__main__":
    write_entry()

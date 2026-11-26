"""The Absurd Clause Contest — one-line entry for make.fun.

The program assembles the absurd clause from named fragments, guards
it against the competition gate (1-200 chars, single line, no control
characters), and writes it to $MAKEFUN_OUTPUT_DIR/entry.txt only.
"""

import os

ENTRY_PARTS = (
    "Clause 47: if the pigeon is late, the contract renews itself, ",
    "the fridge judges you, and ticket #4821 becomes your landlord.",
)

MIN_LEN = 1
MAX_LEN = 200


def build_line():
    """Assemble the clause from its named parts."""
    return "".join(ENTRY_PARTS)


def guard_line(line):
    """Check the line against the gate before publishing."""
    if not (MIN_LEN <= len(line) <= MAX_LEN):
        raise ValueError(f"line is {len(line)} chars, gate is {MIN_LEN}-{MAX_LEN}")
    if line != line.strip() or "\n" in line or "\r" in line:
        raise ValueError("line must be a single line with no edge whitespace")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("line must not contain control characters")
    if any(ch in line for ch in ("\u200b", "\ufeff", "\u00ad")):
        raise ValueError("line must not contain invisible characters")
    return line


def publish(line):
    """Write the line to the grader's output directory only."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "rb") as f:
        written = f.read().decode("utf-8")
    if written != line:
        raise ValueError("read-back mismatch: entry.txt differs from the line")
    return path


def main():
    line = guard_line(build_line())
    publish(line)


if __name__ == "__main__":
    main()

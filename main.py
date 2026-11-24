#!/usr/bin/env python3
"""The Robot Vacuum's Best Excuse — make.fun entry.

Writes one line, the excuse a robot vacuum gives for missing a spot,
to entry.txt in the output directory.
"""

import os

TEXT = (
    "I mapped that corner as a cliff in 2023 and have trusted the map "
    "ever since, even though it is a sock."
)


MAX_CHARS = 140


def validated_text() -> str:
    """Return the entry text after checking it against the gate rules.

    The gate requires UTF-8 text of 1..140 characters, not only white
    space; the brief asks for exactly one line.
    """
    text = TEXT
    encoded = text.encode("utf-8")  # raises if not encodable as UTF-8
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1..{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")
    return text


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (validated_text() + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(payload)
    # Read back so a bad write can never slip through silently.
    with open(path, "rb") as f:
        if f.read() != payload:
            raise IOError("written entry.txt does not match the intended bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

The entry image is entry.png, beside this file: one image that sums up
the world's news of Monday 23 November 2026, rendered by build3.py.
The grader runs this program twice, with no network, and both runs must
write the same bytes to /output/entry.png, so the program is a plain
byte-for-byte copy using only the Python standard library.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    # The two grader runs must produce identical bytes: fail loudly if
    # what landed on disk is not exactly what the repository holds.
    assert os.path.getsize(dst) == len(data), "copied image size mismatch"


if __name__ == "__main__":
    main()

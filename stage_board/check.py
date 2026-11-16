#!/usr/bin/env python3
"""Self-check for the project "Stage Board" (u03).

Run it in the project directory:

    python3 check.py

The script reads only the files your program produced. It never runs
your program, so generate the files first, then check them. Each
[fail] line names one requirement; fix it and run the script again.
"""

import csv
import html as html_lib
import os
import re
import sys


class Fail(Exception):
    pass


CHECKS = []
WARNINGS = []


def check(name):
    def register(function):
        CHECKS.append((name, function))
        return function
    return register


def warn(message):
    WARNINGS.append(message)


def read_text(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_csv(path):
    if not os.path.exists(path):
        raise Fail("%s is missing" % path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise Fail("%s is empty" % path)
    return rows


def require_files(*names):
    missing = [name for name in names if not os.path.exists(name)]
    if missing:
        raise Fail("missing: %s" % ", ".join(missing))


def require_notes(*headings):
    text = read_text("notes.md")
    missing = [heading for heading in headings if heading not in text]
    if missing:
        raise Fail("notes.md has no section: %s" % " | ".join(missing))


def read_pnm(path):
    text = read_text(path)
    lines = [line.split("#")[0] for line in text.splitlines()]
    tokens = " ".join(lines).split()
    if not tokens:
        raise Fail("%s is empty" % path)
    magic = tokens[0]
    if magic not in ("P1", "P2", "P3"):
        raise Fail("%s starts with %r; use the text formats P1, P2 or P3" % (path, magic))
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except (IndexError, ValueError):
        raise Fail("%s: the width and the height are missing from the header" % path)
    index = 3
    maxval = 1
    if magic in ("P2", "P3"):
        try:
            maxval = int(tokens[3])
        except (IndexError, ValueError):
            raise Fail("%s: the maximum value is missing from the header" % path)
        index = 4
    channels = 3 if magic == "P3" else 1
    needed = width * height * channels
    values = tokens[index:]
    if len(values) != needed:
        raise Fail("%s: the header says %dx%d, which needs %d values, but the file has %d"
                   % (path, width, height, needed, len(values)))
    try:
        numbers = [int(value) for value in values]
    except ValueError:
        raise Fail("%s contains a value that is not an integer" % path)
    for number in numbers:
        if number < 0 or number > maxval:
            raise Fail("%s has the value %d, outside 0..%d" % (path, number, maxval))
    return {"magic": magic, "width": width, "height": height,
            "maxval": maxval, "values": numbers, "path": path}


def find_frames(minimum=8):
    if not os.path.isdir("frames"):
        raise Fail("the frames/ directory is missing")
    names = sorted(name for name in os.listdir("frames") if name.endswith(".pgm"))
    if not names:
        raise Fail("frames/ has no .pgm files")
    bad = [name for name in names if not re.match(r"^frame_\d\d\.pgm$", name)]
    if bad:
        raise Fail("these names do not use two digits: %s" % ", ".join(bad[:3]))
    if len(names) < minimum:
        raise Fail("only %d frames; the animation needs at least %d" % (len(names), minimum))
    return ["frames/" + name for name in names]


def numbers_in(text):
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", text)]


def require_gif(path):
    if not os.path.exists(path):
        raise Fail("%s is missing; build it with the convert command from the brief" % path)
    with open(path, "rb") as handle:
        head = handle.read(6)
    if not head.startswith(b"GIF8"):
        raise Fail("%s does not start with GIF8; is it really a GIF?" % path)


def scan_sources(forbidden):
    for name in sorted(os.listdir(".")):
        if not name.endswith(".py") or name == "check.py":
            continue
        with open(name, encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                code = line.split("#")[0]
                for token in forbidden:
                    if token in code:
                        warn("%s:%d uses %s; the brief asks for a different tool."
                             % (name, number, token))


def main():
    print("")
    print("Checking the project in %s" % os.getcwd())
    print("")
    passed = 0
    failed = 0
    for name, function in CHECKS:
        try:
            function()
        except Fail as error:
            failed += 1
            print("[fail] %s" % name)
            print("       %s" % error)
        except Exception as error:
            failed += 1
            print("[fail] %s" % name)
            print("       the check itself stopped: %s: %s" % (type(error).__name__, error))
        else:
            passed += 1
            print("[ok]   %s" % name)
    print("")
    for message in WARNINGS:
        print("[warn] %s" % message)
    if WARNINGS:
        print("")
    print("%d passed, %d failed" % (passed, failed))
    if failed:
        print("NOT READY YET - fix the [fail] lines above and run the script again.")
        return 1
    print("PROJECT READY - every automatic check passed. Show the program and notes.md.")
    return 0



@check("the files named in the brief exist")
def files():
    require_files("times.csv", "stage_board.py", "results.csv", "board.txt",
                  "stages.pgm", "notes.md")


@check("times.csv has four columns and twelve rows, with two unusable times")
def times():
    rows = read_csv("times.csv")
    if len(rows) != 13:
        raise Fail("times.csv has %d lines; a header and twelve rows are expected" % len(rows))
    for number, row in enumerate(rows, start=1):
        if len(row) != 4:
            raise Fail("line %d has %d cells, four expected" % (number, len(row)))
    numeric = 0
    for row in rows[1:]:
        try:
            float(row[3])
        except ValueError:
            continue
        numeric += 1
    if numeric < 9:
        raise Fail("only %d rows have a numeric time; ten of the twelve rows should" % numeric)


@check("results.csv runs from the fastest crew to the slowest in some numeric column")
def results():
    rows = read_csv("results.csv")
    if len(rows) < 5:
        raise Fail("results.csv has %d lines; a header and four crews are expected" % len(rows))
    cells = len(rows[0])
    data = rows[1:]
    for number, row in enumerate(data, start=2):
        if len(row) != cells:
            raise Fail("line %d has %d cells, the header has %d" % (number, len(row), cells))
    for index in range(cells):
        try:
            values = [float(row[index]) for row in data]
        except ValueError:
            continue
        if len(set(values)) < 2:
            continue
        ordered = True
        for first, second in zip(values, values[1:]):
            if second < first - 0.0001:
                ordered = False
                break
        if ordered:
            return
    raise Fail("no numeric column of results.csv is in ascending order; "
               "the board must run from the leader to the last crew")


@check("stages.pgm has one eight-pixel block per crew and stage")
def stages():
    image = read_pnm("stages.pgm")
    if image["magic"] != "P2":
        raise Fail("stages.pgm is %s; the map uses the PGM format P2" % image["magic"])
    if image["width"] % 8 or image["height"] % 8:
        raise Fail("width %d and height %d must both be multiples of 8"
                   % (image["width"], image["height"]))
    if image["width"] // 8 != 4:
        raise Fail("%d blocks across; four crews are expected" % (image["width"] // 8))
    if image["height"] // 8 != 3:
        raise Fail("%d blocks down; three stages are expected" % (image["height"] // 8))


@check("board.txt shows the crews, the times and the gaps")
def board():
    text = read_text("board.txt")
    lines = [line for line in text.splitlines() if re.search(r"\d+\.\d", line)]
    if len(lines) < 4:
        raise Fail("board.txt has %d lines with a time; four crews are expected" % len(lines))


@check("notes.md has both research notes and the notional-time note")
def notes():
    require_notes("## The New Thing – validating a time",
                  "## The New Thing – insertion sort",
                  "## Milestone 6 – the notional time on the map")


scan_sources(["min("])

if __name__ == "__main__":
    sys.exit(main())

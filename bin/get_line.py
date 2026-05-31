#!/usr/bin/env python3
"""get_line.py

Usage patterns supported (backwards-compatible):
  get_line.py <filename> <pattern> [<offset>]
  get_line.py <pattern> <offset> --file <filename>
  cat file | get_line.py <pattern> <offset>

Behaviour:
  - Finds lines matching the given regular expression (first capture not used).
  - For each match, prints the line at (match_line_index + offset).
  - Offset may be negative; defaults to 0 (print the matching line).

This keeps compatibility with calls like:
  get_line.py "^TAXABLE.*SUMMARY" 2 --file file.csv
while making the filename the first positional argument when possible.
"""
import sys
import argparse
import os
import re


def parse_args():
    p = argparse.ArgumentParser(description="Print line relative to matches of a regex")
    p.add_argument('positional', nargs='*', help='[filename] pattern [offset]')
    p.add_argument('--file', '-f', dest='file', help='input file (alternate to giving filename first)')
    p.add_argument('--encoding', default='utf-8', help='file encoding (default: utf-8)')
    return p.parse_args()


def main():
    args = parse_args()
    pos = list(args.positional)

    filename = None
    pattern = None
    offset = 0

    # If the first positional arg exists and is a path to a file, treat it as filename
    if len(pos) >= 1 and os.path.exists(pos[0]):
        filename = pos.pop(0)

    # If --file provided, it takes precedence unless filename already set
    if args.file and not filename:
        filename = args.file

    # Now interpret remaining positionals: pattern and optional offset
    if len(pos) >= 1:
        pattern = pos[0]
    if len(pos) >= 2:
        try:
            offset = int(pos[1])
        except ValueError:
            print(f"Error: offset must be an integer, got '{pos[1]}'", file=sys.stderr)
            sys.exit(2)

    # If pattern not provided, that's an error
    if pattern is None:
        print("Usage: get_line.py <filename> <pattern> [<offset>]\n       or: get_line.py <pattern> <offset> --file <filename>", file=sys.stderr)
        sys.exit(2)

    # Read input lines
    if filename:
        try:
            with open(filename, 'r', encoding=args.encoding, errors='replace') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error opening file '{filename}': {e}", file=sys.stderr)
            sys.exit(2)
    else:
        # read from stdin
        lines = sys.stdin.read().splitlines(keepends=True)

    # Compile regex
    try:
        rx = re.compile(pattern)
    except re.error as e:
        print(f"Invalid regular expression '{pattern}': {e}", file=sys.stderr)
        sys.exit(2)

    # Find all match line indices
    match_indices = [i for i, line in enumerate(lines) if rx.search(line)]

    # For each match index, compute target line index and print if valid
    out_lines = []
    for m in match_indices:
        target = m + offset
        if 0 <= target < len(lines):
            out_lines.append(lines[target])

    # If nothing found, exit non-zero to help scripts detect failures
    if not out_lines:
        # no output but not necessarily an error; return success code but nothing printed
        sys.exit(0)

    # Print results
    for l in out_lines:
        # ensure newline presence
        if l.endswith('\n'):
            sys.stdout.write(l)
        else:
            sys.stdout.write(l + "\n")


if __name__ == '__main__':
    main()

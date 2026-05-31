#!/usr/bin/env python
"""get_line.py
"""
import sys
import argparse
import os
import re


def parse_args():
    p = argparse.ArgumentParser(description="Print line relative to matches of a regex")
    p.add_argument('filename', default=None, help='input filename')
    p.add_argument('pattern',  default=None, help='pattern')
    p.add_argument('offset',   default=None, help='offset')
    p.add_argument('--encoding', default='utf-8', help='file encoding (default: utf-8)')
    return p.parse_args()


def main():
    args = parse_args()

    if args.filename == None or args.pattern == None or args.offset == None:
        sys.exit(1)

    filename = args.filename
    pattern  = args.pattern 
    offset   = int(args.offset)


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

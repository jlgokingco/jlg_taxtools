#!/usr/bin/env python
"""filter_csv.py - Filter and print records from Schwab-style CSV files."""

import argparse
import csv
import os
import re
import sys

FILTER_OPTIONS = {
    'Account_Number': 'Account Number',
    'Account_Name': 'Account Name',
    'Account_Type': 'Account Type',
    'Security_Description': 'Security Description',
    'Symbol': 'Symbol',
    'Type': 'Security Type',
    'Transaction_Type': 'Transaction Type',
    'Income_Type': 'Income Type',
}


def arg_to_column(name: str) -> str:
    return name.replace('_', ' ')


def parse_args():
    p = argparse.ArgumentParser(
        description='Filter and print records from a CSV file (header on line 2).'
    )
    p.add_argument('filename', help='Path to the CSV file')
    for opt_name in FILTER_OPTIONS:
        p.add_argument(
            f'--{opt_name}',
            metavar='REGEX',
            help=f'Filter by {FILTER_OPTIONS[opt_name]} (regular expression)',
        )
    p.add_argument(
        '--print',
        dest='print_columns',
        action='append',
        metavar='COLUMN',
        help='Print only this column (underscores become spaces); repeatable',
    )
    return p.parse_args()


def compile_filters(args, column_index):
    filters = {}
    for opt_name, column_name in FILTER_OPTIONS.items():
        pattern = getattr(args, opt_name, None)
        if pattern is None:
            continue
        if column_name not in column_index:
            print(
                f"Error: column '{column_name}' not found in header.",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            filters[column_name] = re.compile(pattern)
        except re.error as e:
            print(
                f"Invalid regular expression for --{opt_name} '{pattern}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)
    return filters


def resolve_print_columns(print_args, column_index):
    if not print_args:
        return []
    columns = []
    for arg in print_args:
        column_name = arg_to_column(arg)
        if column_name not in column_index:
            print(
                f"Error: column '{column_name}' not found in header.",
                file=sys.stderr,
            )
            sys.exit(1)
        columns.append(column_name)
    return columns


def row_matches(row, filters, column_index):
    for column_name, regex in filters.items():
        idx = column_index[column_name]
        value = row[idx] if idx < len(row) else ''
        if not regex.search(value):
            return False
    return True


def main():
    args = parse_args()

    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.filename, 'r', newline='', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Error opening file '{args.filename}': {e}", file=sys.stderr)
        sys.exit(1)

    if len(lines) < 2:
        print('Error: file must have a title line and a header line.', file=sys.stderr)
        sys.exit(1)

    header_row = next(csv.reader([lines[1]]))
    column_index = {name: i for i, name in enumerate(header_row) if name}

    if not column_index:
        print('Error: no column headers found on line 2.', file=sys.stderr)
        sys.exit(1)

    filters = compile_filters(args, column_index)
    print_columns = resolve_print_columns(args.print_columns, column_index)

    out = sys.stdout
    csv_writer = csv.writer(out) if print_columns else None

    for raw_line in lines[2:]:
        if not raw_line.strip():
            continue

        row = next(csv.reader([raw_line]))
        if not row_matches(row, filters, column_index):
            continue

        if print_columns:
            values = []
            for column_name in print_columns:
                idx = column_index[column_name]
                values.append(row[idx] if idx < len(row) else '')
            csv_writer.writerow(values)
        else:
            if raw_line.endswith('\n'):
                out.write(raw_line)
            else:
                out.write(raw_line + '\n')


if __name__ == '__main__':
    main()

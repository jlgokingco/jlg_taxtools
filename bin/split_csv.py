import csv
import os
import sys
import argparse

def split_csv(input_path):
    """
    Splits a CSV file into multiple CSV files using empty lines as a separator.
    
    Args:
        input_path (str): Path to the input CSV file.
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    base, ext = os.path.splitext(input_path)
    
    current_file = None
    current_writer = None
    file_idx = 1
    split_files = []
    
    try:
        # Use utf-8-sig to automatically handle potential BOM (Byte Order Mark)
        with open(input_path, 'r', newline='', encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)
            
            for row in reader:
                # A row is considered empty if all cells are empty or contain only whitespace
                is_empty = not any(cell.strip() for cell in row)
                
                if is_empty:
                    # If we hit an empty row and have an open output file, close it
                    if current_file is not None:
                        current_file.close()
                        current_file = None
                        current_writer = None
                        file_idx += 1
                else:
                    # If we don't have an active writer, create the next split file
                    if current_writer is None:
                        out_path = f"{base}_{file_idx}{ext}"
                        current_file = open(out_path, 'w', newline='', encoding='utf-8')
                        current_writer = csv.writer(current_file)
                        split_files.append(out_path)
                    
                    current_writer.writerow(row)
                    
        # Close the last file if it's still open
        if current_file is not None:
            current_file.close()
            
        print(f"Successfully split '{input_path}' into {len(split_files)} files:")
        for path in split_files:
            print(f"  - {path}")
            
    except Exception as e:
        # Clean up any open files in case of failure
        if current_file is not None:
            try:
                current_file.close()
            except Exception:
                pass
        print(f"Error occurred during split: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split a CSV file into multiple files using empty lines as separators.")
    parser.add_argument("input_file", help="Path to the CSV file to be split.")
    
    args = parser.parse_args()
    split_csv(args.input_file)

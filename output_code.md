```python
import csv
from typing import Dict, List

def read_csv_file(file_path: str) -> None:
    """
    Reads a CSV file and prints its contents.

    Args:
    file_path (str): The path to the CSV file.
    """
    try:
        with open(file_path, 'r') as file:
                print(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_csv_file_with_delimiter(file_path: str, delimiter: str) -> None:
    """
    Reads a CSV file with a specified delimiter and prints its contents.

    Args:
    file_path (str): The path to the CSV file.
    delimiter (str): The delimiter used in the CSV file.
    """
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_csv_file_with_dict_reader(file_path: str) -> None:
    """
    Reads a CSV file using DictReader and prints its contents.

    Args:
    file_path (str): The path to the CSV file.
    """
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row['Name'], row['Age'])
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main() -> None:
    read_csv_file('data.csv')
    read_csv_file_with_delimiter('data.csv', ';')
    read_csv_file_with_dict_reader('data.csv')

if __name__ == "__main__":
    main()
```
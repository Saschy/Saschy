## Simple Python Expense Tracker

This repository now includes `expense_tracker.py`, a beginner-friendly script that lets you:

1. Add an expense (date, category, description, amount).
2. Save expenses to a CSV file (`expenses.csv`).
3. Show the total spent for a given month.

The script uses only the Python standard library (`argparse`, `csv`, `datetime`, and `pathlib`).

### How to run

1. Make sure you have Python 3 installed.
2. From this folder, run one of the commands below.

#### Add an expense

```bash
python expense_tracker.py add 2024-05-15 groceries "Milk and eggs" 12.50
```

- The date is optional; if you omit it, today's date is used:

```bash
python expense_tracker.py add groceries "Bus ticket" 3.00
```

Each added expense is appended to `expenses.csv` with a header row the first time the file is created.

#### Show total for a month

```bash
python expense_tracker.py total --year 2024 --month 5
```

If you omit the flags, the script summarizes the current month by default:

```bash
python expense_tracker.py total
```

### How the code works

- `CSV_FILE` keeps the file name in one place so it is easy to change later.
- `ensure_csv_file_exists()` creates `expenses.csv` with a header row if it does not yet exist.
- `add_expense()` appends a new row to the CSV file and prints a confirmation message.
- `read_expenses()` loads all rows into a list of dictionaries.
- `total_for_month()` sums amounts for the given year and month, skipping any invalid rows.
- `parse_arguments()` sets up two subcommands: `add` and `total`.
- `main()` parses user input and routes to the right function, including a friendly date validation for `add`.

Feel free to edit the file name or extend the script with more features like category summaries or exporting to other formats.

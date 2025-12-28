"""A beginner-friendly expense tracker.

This script lets you:
1. Add an expense (date, category, description, amount).
2. Save expenses to a CSV file (``expenses.csv``).
3. Show the total spent for a specific month.

You can run it directly from the command line. See the README for examples.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, List, Dict


# We keep the CSV file name in a single place so it is easy to change later.
CSV_FILE = Path("expenses.csv")


def ensure_csv_file_exists() -> None:
    """Create the CSV file with a header row if it is missing.

    The tracker is intentionally simple: it keeps all data in one file and uses
    the built-in ``csv`` module instead of any external libraries.
    """

    if CSV_FILE.exists():
        return

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "category", "description", "amount"])


def add_expense(date_str: str, category: str, description: str, amount: float) -> None:
    """Append a new expense to the CSV file.

    Args:
        date_str: Date as ``YYYY-MM-DD`` (for example, ``2024-05-15``).
        category: A short label like "groceries" or "rent".
        description: A brief note about the expense.
        amount: How much you spent, as a number.
    """

    ensure_csv_file_exists()

    # ``newline=""`` prevents extra blank lines on Windows.
    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date_str, category, description, f"{amount:.2f}"])

    print(f"Added expense on {date_str}: {category} - {description} (${amount:.2f})")


def read_expenses() -> List[Dict[str, str]]:
    """Load all expenses from the CSV file.

    The function returns a list of dictionaries, one per row. If the file does
    not exist yet, we create it and return an empty list.
    """

    if not CSV_FILE.exists():
        ensure_csv_file_exists()
        return []

    with CSV_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def total_for_month(year: int, month: int) -> float:
    """Calculate the total amount spent in the given month."""

    expenses = read_expenses()
    total = 0.0

    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
            amount = float(expense["amount"])
        except (ValueError, KeyError):
            # Skip rows with missing or invalid data.
            continue

        if expense_date.year == year and expense_date.month == month:
            total += amount

    return total


def parse_arguments() -> argparse.Namespace:
    """Set up command-line arguments and parse them."""

    parser = argparse.ArgumentParser(description="Simple CSV-based expense tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ``add`` command: add a new expense row.
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument(
        "date",
        nargs="?",
        default=date.today().isoformat(),
        help="Date of the expense in YYYY-MM-DD format (default: today)",
    )
    add_parser.add_argument("category", help="Category such as groceries, rent, or travel")
    add_parser.add_argument("description", help="Short note about the expense")
    add_parser.add_argument("amount", type=float, help="Amount spent (numbers only)")

    # ``total`` command: show how much was spent in a month.
    total_parser = subparsers.add_parser("total", help="Show total spent for a month")
    total_parser.add_argument(
        "--year",
        type=int,
        default=date.today().year,
        help="Year to summarize (default: current year)",
    )
    total_parser.add_argument(
        "--month",
        type=int,
        default=date.today().month,
        help="Month number 1-12 (default: current month)",
    )

    return parser.parse_args()


def main() -> None:
    """Handle user commands and show helpful output."""

    args = parse_arguments()

    if args.command == "add":
        # Validate the date early so we can show a clear error message.
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            raise SystemExit("Please use YYYY-MM-DD for the date (example: 2024-05-15)")

        add_expense(args.date, args.category, args.description, args.amount)

    elif args.command == "total":
        monthly_total = total_for_month(args.year, args.month)
        month_name = datetime(args.year, args.month, 1).strftime("%B %Y")
        print(f"Total spent in {month_name}: ${monthly_total:.2f}")


if __name__ == "__main__":
    main()

# Library Transaction System

A console program written in Python that records book borrowing and returning in a small library.
It keeps track of available copies, remembers who is holding a book, computes overdue fines,
and saves its data to text files so nothing is lost between runs.

**Course:** CS 26 – Software Development Fundamentals (2nd Laboratory Examination)
**Authors:** Almario Garcia and Jayden Cloyd Celocia

## Features

- Borrow a book (validates book number, borrower name, and loan days of 1-7)
- Return a book and compute the fine: PHP 5.00 for every day kept beyond 7 days
- View the catalog with available copies
- Saves the catalog and active loans to `.csv` files; appends every transaction to a log
- Handles invalid input, a missing or malformed data file, and closed input without crashing

## Requirements

Python 3.8 or newer. No external libraries are needed.

## How to run

1. Download or clone this repository.
2. Open a terminal inside the project folder.
3. Run:

```
python library_app.py
```

The data files (`inventory.csv`, `loans.csv`, `transactions.csv`) are created automatically on first use.

## Project structure

```text
library-transaction-system/
├── library_app.py      # main program: menu and user interaction
├── library_logic.py    # library rules: validation, loans, fines
├── library_data.py     # file handling: load, save, log
├── CS26_Exam2_Garcia_Celocia.md   # full technical documentation and test results
├── README.md
└── .gitignore
```

| Module | Responsibility |
|---|---|
| `library_app.py` | Menu, user input and output; imports the other two modules |
| `library_logic.py` | Rules only: `parse_int_in_range`, `compute_fine`, `find_loan`, `borrow_book`, `return_book` |
| `library_data.py` | Files only: `load_inventory`, `load_loans`, `save_inventory`, `save_loans`, `log_transaction` |

## Data structures used

- **Dictionary:** the inventory, `{title: copies}`
- **List:** the active loans, a list of `{"borrower": ..., "title": ...}` dictionaries
- **Tuple:** the loan rules, `LOAN_RULES = (7, 5.0)`

## Testing

Fourteen test cases (normal, boundary, invalid, file-handling, and one debugging case) are recorded
with expected and actual results in [`CS26_Exam2_Garcia_Celocia.md`](CS26_Exam2_Garcia_Celocia.md), Section J.

## Known limitations

- The borrow date is not stored; the number of days kept is typed in at return time.
- Book titles and borrower names cannot contain commas (commas separate fields in the files).
- Two borrowers with the same name cannot be told apart.

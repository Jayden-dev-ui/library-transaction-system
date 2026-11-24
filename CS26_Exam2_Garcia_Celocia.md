# CS 26 Exam 2 – Technical Documentation
## Library Transaction System (Python)

**Prepared by:** Almario Garcia and Jayden Cloyd Celocia
**Course:** CS 26 – Software Development Fundamentals
**Program files:** `library_app.py`, `library_logic.py`, `library_data.py`

---

## A. Program Title and Overview

**Program name:** Library Transaction System

The Library Transaction System is a console program that records the borrowing and returning of books in a small school library. It keeps track of how many copies of each title are available, remembers who currently has a book, and computes the overdue fine when a book is returned late.

The intended users are library staff or student assistants who currently record loans by hand. The program saves its data in plain text files, so the catalog and the list of active loans are still there the next time the program is started.

---

## B. Problem Description

In a small library that uses a paper logbook, three problems appear often:

- The number of available copies is miscounted after many borrow and return transactions.
- Overdue fines are calculated by hand, which leads to arithmetic mistakes and inconsistent amounts.
- There is no quick way to check whether a book is available or who is holding it.

The program is needed so that every transaction updates the stock automatically and applies the same fine rule every time.

### Inputs
- Menu option (1–4)
- Book number chosen from the catalog
- Borrower name
- Number of days to borrow (1–7)
- Number of days the book was kept (on return)
- Saved data from `inventory.csv` and `loans.csv`

### Processing
- Validate every input and reject wrong values with a message.
- Check that a copy is available before lending.
- Reduce the stock when a book is borrowed and increase it when returned.
- Compute the fine: PHP 5.00 for every day kept beyond the 7-day loan period.
- Save the updated data and append the transaction to a log.

### Outputs
- The catalog with the available copies per title
- Success, error, and fine messages
- Updated `inventory.csv` and `loans.csv`
- A new line in `transactions.csv` for every borrow or return

---

## C. Program Objectives

1. Display a numbered catalog and reduce the available copies of a title by one each time it is borrowed, and refuse the loan when no copy is left.
2. Accept a loan period only from 1 to 7 days and reject non-numeric or out-of-range input without crashing.
3. Compute a fine of PHP 5.00 per overdue day when a book is returned after more than 7 days, and no fine for 7 days or fewer.
4. Keep the catalog and active loans between runs by saving them to text files, and append every transaction to a log file.
5. Separate the program into three modules: one for the menu, one for the library rules, and one for file operations.

---

## D. Program Requirements and Features

### Implemented features

| Feature | Description |
|---|---|
| Borrow a book | Validates the book number, name, and days; reduces stock; records the loan |
| Return a book | Finds the loan, computes the fine, restores the stock |
| View catalog | Lists all titles with available copies |
| File persistence | Loads and saves the catalog and loans in `.csv` text files |
| Transaction log | Appends one line per borrow or return |
| Input validation | Rejects invalid menu choices, book numbers, days, and names |
| Safe file loading | Handles a missing file and skips malformed lines |

### Assumptions
- The program is started from inside its own folder, because the data files are created in the current working directory.
- Each borrower has a name that is typed the same way (letters are matched ignoring upper/lower case).
- Book titles and borrower names do not contain commas, because commas separate the fields in the files.

### Limitations
- The borrow date is not stored. The number of days kept is typed in by the user when the book is returned.
- If two loans have the same borrower name, a return closes the first matching loan in the list.
- A malformed line that was skipped while loading is not written back the next time the file is saved.
- The transaction log records the name exactly as typed during the transaction (for example `ana`), not as originally stored (`Ana`).
- The program has a text interface only.

### Planned enhancements (not yet implemented)
- Store the borrow date and calculate the due date automatically.
- Search books by title.
- Limit the number of books one borrower may hold.

---

## E. Program Structure and Modules

```text
library_system/
├── library_app.py        # main program: menu and user interaction
├── library_logic.py      # library rules: validation, loans, fines
├── library_data.py       # file handling: load, save, log
├── inventory.csv         # created automatically: title,copies
├── loans.csv             # created automatically: borrower,title
└── transactions.csv      # created automatically: action,borrower,title,fine
```

| File | Purpose |
|---|---|
| `library_app.py` | Shows the menu, reads input from the user, calls the other modules, and prints results |
| `library_logic.py` | Contains the rules only (no `input()` and no files): number validation, fine computation, borrowing and returning |
| `library_data.py` | Reads and writes `inventory.csv`, `loans.csv`, and `transactions.csv` |
| `inventory.csv` | Saved stock, one `title,copies` line per book |
| `loans.csv` | Saved active loans, one `borrower,title` line per loan |
| `transactions.csv` | Append-only history, one `action,borrower,title,fine` line per transaction |

### How the modules work together

`library_app.py` imports the two other modules and uses their functions with the module name as a prefix. The other two modules do not import each other, so the rules can change without touching the file code and the other way around.

```python
import library_data
import library_logic

inventory = library_data.load_inventory()          # from library_data.py
loans = library_data.load_loans(inventory)

number = library_logic.parse_int_in_range(choice, 1, len(titles))   # from library_logic.py
```

**How to run:** open a terminal in the `library_system` folder and enter `python library_app.py`.

---

## F. Data Structures

### Dictionary – the inventory
The inventory maps each book title (key) to the number of available copies (value).

```python
DEFAULT_INVENTORY = {
    "Python Crash Course": 3,
    "Clean Code": 2,
    "Intro to Algorithms": 1,
    "Data Structures": 2,
    "Digital Logic": 0,
}
```

**Why a dictionary:** a title is looked up directly by name (`inventory[title] -= 1`) without searching through the data, and each title appears only once because keys are unique.

### List – the active loans
The loans are kept in a list because the number of loans grows when books are borrowed and shrinks when they are returned. Each loan is a small dictionary with a borrower and a title. The program also builds a list of titles with `list(inventory)` so a number typed by the user can be matched to a title.

```python
loans = [
    {"borrower": "Ana", "title": "Clean Code"},
    {"borrower": "Dan", "title": "Intro to Algorithms"},
]
loans.append({"borrower": borrower, "title": title})   # borrow
loans.pop(position)                                    # return
```

**Why a list:** it can grow and shrink with `append()` and `pop()`, and it keeps loans in the order they were made.

### Tuple – the loan rules
The loan period and the fine per day are the library's fixed rules, so they are stored in a tuple, which cannot be changed accidentally while the program runs.

```python
LOAN_RULES = (7, 5.0)                       # (maximum loan days, fine per day in PHP)
MAX_LOAN_DAYS, FINE_PER_DAY = LOAN_RULES    # tuple unpacking
```

**Why a tuple:** the values are constants that belong together. The `return_book()` function also returns a tuple `(title, fine)` so that two results can be sent back at once.

---

## G. Functions

### `library_logic.py`

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `parse_int_in_range` | `text, low, high` | `int` | Converts text to a whole number and checks the range; raises `ValueError` if invalid |
| `compute_fine` | `days_kept` | `float` | Computes the overdue fine |
| `find_loan` | `loans, borrower` | `int` (index, or -1) | Finds a borrower's loan, ignoring letter case |
| `borrow_book` | `inventory, loans, title, borrower` | `None` | Checks the rules, reduces stock, adds a loan; raises `ValueError` if a rule is broken |
| `return_book` | `inventory, loans, borrower, days_kept` | `tuple (title, fine)` | Closes a loan and restores stock; raises `ValueError` if no loan exists |

### `library_data.py`

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `load_inventory` | `filename` | `dict` | Reads the catalog file, with warnings and defaults for bad data |
| `load_loans` | `inventory, filename` | `list` | Reads active loans, skipping invalid lines |
| `save_inventory` | `inventory, filename` | `bool` | Overwrites the catalog file |
| `save_loans` | `loans, filename` | `bool` | Overwrites the loans file |
| `log_transaction` | `action, borrower, title, fine, filename` | `None` | Appends one line to the log |

### `library_app.py`

| Function | Parameters | Returns | Purpose |
|---|---|---|---|
| `show_catalog` | `inventory` | `None` | Prints the numbered catalog |
| `handle_borrow` | `inventory, loans` | `None` | Reads borrow details and runs the borrow steps |
| `handle_return` | `inventory, loans` | `None` | Reads return details and prints the fine |
| `main` | none | `None` | Loads data and runs the menu loop |

### Code excerpt 1 – validating a number

```python
def parse_int_in_range(text, low, high):
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a whole number.")
    if value < low or value > high:
        raise ValueError(f"Number must be between {low} and {high}.")
    return value
```

`input()` always gives a string, so `int()` converts it. If the text cannot be converted (for example `abc`), Python raises a `ValueError`, which the function replaces with a clearer message. If the number is valid but outside the allowed range, a second `ValueError` is raised. This single function is reused for the book number, the loan days, and the days kept.

### Code excerpt 2 – computing the fine

```python
def compute_fine(days_kept):
    if days_kept > MAX_LOAN_DAYS:
        return (days_kept - MAX_LOAN_DAYS) * FINE_PER_DAY
    return 0.0
```

The condition uses `>` instead of `>=`, so a book kept for exactly 7 days is still on time. A book kept for 8 days has 1 overdue day, and the fine is `1 * 5.0 = 5.0`. This is the boundary that tests T2 and T3 check.

---

## H. File Handling

| File | Format | Modes used | Role |
|---|---|---|---|
| `inventory.csv` | Text, one `title,copies` per line | `"r"` to load, `"w"` to save | Saved stock |
| `loans.csv` | Text, one `borrower,title` per line | `"r"` to load, `"w"` to save | Saved active loans |
| `transactions.csv` | Text, one `action,borrower,title,fine` per line | `"a"` | History of all transactions |

- **`"r"` (read)** opens an existing file to load data at the start of the program.
- **`"w"` (write)** replaces the entire file. It is used after each transaction so the file always matches the data in memory.
- **`"a"` (append)** adds a new line at the end without erasing older lines, which suits a history log.

All files are opened with `with open(...)`, which closes the file automatically after the block, even if an error occurs while reading or writing.

```python
try:
    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.strip().split(",")
            if len(parts) != 2 or not parts[1].strip().isdigit():
                print(f"Warning: skipped malformed line {line_number} in {filename}.")
                continue
            inventory[parts[0].strip()] = int(parts[1])
except FileNotFoundError:
    print(f"{filename} not found. Starting with the default catalog.")
    return dict(DEFAULT_INVENTORY)
```

### Absent or malformed files
- **Missing `inventory.csv`:** a `FileNotFoundError` is caught, a message is printed, and the program starts with a copy of `DEFAULT_INVENTORY`.
- **Missing `loans.csv`:** treated as "no loans yet" and an empty list is used, with no message.
- **Malformed lines:** a line that does not have exactly two fields, or whose copies value is not a number, is skipped with a warning that names the line number. Blank lines are ignored.
- **No valid lines at all:** the default catalog is used.

### Persistence between runs
Records **do persist**. After each successful borrow or return, `inventory.csv` and `loans.csv` are rewritten, and a new line is appended to `transactions.csv`. Test T9 confirms that a loan made in one run is still present in the next run.

---

## I. Error Handling

### Expected errors (input validation)

These are mistakes a user can make. They are expected, so the program reports them and continues.

| Situation | How it is handled |
|---|---|
| Menu option is not 1–4 | `else` branch prints "Invalid option" |
| Book number or days is not a number | `int()` raises `ValueError` inside `parse_int_in_range`, which is caught in `handle_borrow` / `handle_return` |
| Number is out of range | `parse_int_in_range` raises `ValueError` with the allowed range |
| Empty name, or name with a comma | `borrow_book` raises `ValueError` |
| No copies left | `borrow_book` raises `ValueError` |
| Returning with no active loan | `return_book` raises `ValueError` |

```python
try:
    choice = input("Enter book number to borrow: ").strip()
    number = library_logic.parse_int_in_range(choice, 1, len(titles))
    ...
    library_logic.borrow_book(inventory, loans, title, name)
except ValueError as error:          # validation errors only
    print(f"Cannot borrow: {error}")
    return
```

Because the `return` is inside the `except` block, nothing is saved and no stock changes when a rule fails.

### File and environment errors

| Error | Where | Handling |
|---|---|---|
| `FileNotFoundError` | `load_inventory`, `load_loans` | Default catalog / empty loan list |
| `OSError` | `save_*`, `log_transaction` | A message is printed and the program keeps running |
| `EOFError`, `KeyboardInterrupt` | menu loop in `main` | Prints "Input closed. Exiting." and ends the loop |

### Unexpected programming errors

The menu loop in `main()` also has a last `except Exception as error` clause that prints "Unexpected error" and returns to the menu instead of crashing. It is placed **after** the specific handlers and is meant only for mistakes in the program itself. During our testing no test triggered this clause, so it was not observed in action.

The design keeps the two kinds separate: `ValueError` is used on purpose for user mistakes, while the general `Exception` handler is only a safety net for bugs we did not predict.

---

## J. Testing, Debugging, and Results

Each test was run with a fresh, empty folder (no saved `.csv` files) unless the scenario says otherwise. Inputs are listed in the order the prompts appear (menu option first).

| Test ID | Scenario | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1 | **Normal:** borrow a book | `1, 2, Ana, 5, 4` | Loan recorded; Clean Code copies drop from 2 to 1; files updated | "Success! Ana borrowed 'Clean Code' for 5 day(s)." `inventory.csv` shows `Clean Code,1`; `loans.csv` shows `Ana,Clean Code`; log shows `BORROW,Ana,Clean Code,0.00` | Pass |
| T2 | **Boundary:** return after exactly 7 days | `1, 1, Ben, 7, 2, Ben, 7, 4` | Loan of 7 days accepted; no fine | "Success! Ben borrowed 'Python Crash Course' for 7 day(s)." then "Returned on time. No fine."; `loans.csv` empty; stock back to 3 | Pass |
| T3 | **Boundary:** return after 8 days | `1, 1, Ben, 7, 2, Ben, 8, 4` | 1 overdue day, fine PHP 5.00 | "Overdue! Fine: PHP 5.00"; log shows `RETURN,Ben,Python Crash Course,5.00` | Pass |
| T4 | **Boundary:** borrow for 8 days (above limit) | `1, 1, Cy, 8, 4` | Loan rejected; nothing saved | "Cannot borrow: Number must be between 1 and 7." No data files were written | Pass |
| T5 | **Invalid:** days is text | `1, 1, Cy, abc, 4` | Error message; program does not crash | "Cannot borrow: 'abc' is not a whole number." Menu continued and exited normally with "Goodbye!" | Pass |
| T6 | **Failure:** book with no copies | `1, 5, Cy, 3, 4` | Loan rejected | "Cannot borrow: No copies of 'Digital Logic' are available." | Pass |
| T7 | **Invalid:** menu option `x` | `x, 1, 9, 4` (first entry) | "Invalid option" message | "Invalid option. Please enter a number from 1 to 4." | Pass |
| T8 | **Invalid:** book number outside the catalog | `x, 1, 9, 4` (second entry, same run as T7) | Range error | "Cannot borrow: Number must be between 1 and 5." | Pass |
| T9 | **Persistence:** data survives a restart | Run 1: `1, 3, Dan, 4, 4`. Run 2 (same folder): `3, 4` | Run 2 shows Intro to Algorithms with 0 copies and no "not found" message | Run 2 showed "Intro to Algorithms (copies available: 0)" with no "not found" message; `loans.csv` contained `Dan,Intro to Algorithms` | Pass |
| T10 | **Malformed file:** bad lines in `inventory.csv` | File lines: `Clean Code,2`, `Bad line without comma`, `Data Structures,abc`, a blank line, `Digital Logic,4`. Input: `3, 4` | Bad lines skipped with warnings; valid lines loaded | Warnings for line 2 and line 3. Catalog showed only Clean Code (2) and Digital Logic (4). The file itself was not changed because no transaction was made | Pass |
| T11 | **Missing file:** no `inventory.csv` | Start in an empty folder, then `3, 4` | Message and default catalog | "inventory.csv not found. Starting with the default catalog." followed by the five default titles (seen at the start of T1) | Pass |
| T12 | **Invalid:** borrower name with a comma | `1, 1, "Smith, John", 3, 4` (the name typed is `Smith, John`) | Name rejected | "Cannot borrow: Borrower name cannot contain commas." | Pass |
| T13 | **Case matching:** borrow as `Ana`, return as `ana` | `1, 2, Ana, 3, 2, ana, 3, 4` | Return accepted | **Before fix:** "Cannot return: No active loan found for 'ana'." **After fix:** "Returned on time. No fine."; `loans.csv` empty | Fail, then Pass after fix |
| T14 | **Failure:** input stream closed | No input at all (end of input at the first prompt) | Program exits without a crash | "Input closed. Exiting." | Pass |

### Debugging observation

**Problem found (T13).** While testing returns, we borrowed a book under the name `Ana` and then tried to return it by typing `ana`. The program answered `Cannot return: No active loan found for 'ana'.` even though `loans.csv` clearly contained `Ana,Clean Code`. A real user can easily type a name with different capital letters, so the book could never be returned.

**Cause.** `find_loan()` compared the names with `==`, and Python treats `"Ana"` and `"ana"` as different strings.

**Original code:**

```python
if loans[index]["borrower"] == borrower:
```

**Correction.** Both names are converted to lowercase before they are compared:

```python
if loans[index]["borrower"].lower() == borrower.lower():
```

**Verification.**
1. We repeated the same inputs as T13. This time the result was "Returned on time. No fine." and `loans.csv` was empty.
2. We re-ran T3 (fine of PHP 5.00) and T6 (no copies) to confirm that the change did not break other features. Both gave the same results as before.

**Side effect noted:** the transaction log stores the name as typed during the return (`RETURN,ana,Clean Code,0.00`), while the borrow line stores `Ana`. This is listed under the limitations in Section D.

---

## K. Conclusion

The Library Transaction System meets its objectives: it lends and receives books while keeping the stock correct, rejects invalid input without crashing, applies the PHP 5.00 per day fine only after the 7-day loan period, and keeps its data between runs through plain text files. Splitting the code into menu, rules, and file modules made it easier to test each part and to fix the case-matching defect in one place.

**Limitations:** it does not store borrow dates, it cannot tell apart two borrowers with the same name, and it uses only a text interface.

**Possible improvements:**
1. Store the borrow date so the number of days kept is calculated automatically instead of typed in.
2. Add a borrower ID so that people with the same name can be told apart.

---

## L. References

- Python Software Foundation. *The Python Tutorial – Input and Output (reading and writing files).* https://docs.python.org/3/tutorial/inputoutput.html
- Python Software Foundation. *The Python Tutorial – Errors and Exceptions.* https://docs.python.org/3/tutorial/errors.html
- Python Software Foundation. *The Python Tutorial – Data Structures.* https://docs.python.org/3/tutorial/datastructures.html
- Python Software Foundation. *The Python Tutorial – Modules.* https://docs.python.org/3/tutorial/modules.html

**Acknowledgment of assistance:** An AI assistant (Claude, by Anthropic) was used to help design and draft the program structure and this documentation. The program was run and tested, and the results in Section J were recorded from those runs.

# Tuple: loan rules that must never change while the program runs.
# (maximum loan days, fine in pesos per overdue day)
LOAN_RULES = (7, 5.0)
MAX_LOAN_DAYS, FINE_PER_DAY = LOAN_RULES   # tuple unpacking


def parse_int_in_range(text, low, high):
    """Convert text to an int and check that low <= value <= high.

    Raises ValueError with a friendly message if the text is not a whole
    number or the number is outside the allowed range.
    """
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a whole number.")
    if value < low or value > high:
        raise ValueError(f"Number must be between {low} and {high}.")
    return value


def compute_fine(days_kept):
    """Return the overdue fine (float) for a book kept for days_kept days."""
    if days_kept > MAX_LOAN_DAYS:
        return (days_kept - MAX_LOAN_DAYS) * FINE_PER_DAY
    return 0.0


def find_loan(loans, borrower):
    """Return the index of the borrower's loan in the list, or -1 if none.

    Names are compared in lowercase so 'Ana' and 'ana' match.
    """
    for index in range(len(loans)):
        if loans[index]["borrower"].lower() == borrower.lower():
            return index
    return -1


def borrow_book(inventory, loans, title, borrower):
    """Record a loan. Raises ValueError if a rule is broken."""
    if borrower == "":
        raise ValueError("Borrower name cannot be empty.")
    if "," in borrower:
        raise ValueError("Borrower name cannot contain commas.")
    if inventory[title] == 0:
        raise ValueError(f"No copies of '{title}' are available.")

    inventory[title] -= 1
    loans.append({"borrower": borrower, "title": title})


def return_book(inventory, loans, borrower, days_kept):
    """Close a loan. Returns a tuple (title, fine).

    Raises ValueError if the borrower has no active loan.
    """
    position = find_loan(loans, borrower)
    if position == -1:
        raise ValueError(f"No active loan found for '{borrower}'.")

    title = loans[position]["title"]
    inventory[title] += 1
    loans.pop(position)
    return title, compute_fine(days_kept)
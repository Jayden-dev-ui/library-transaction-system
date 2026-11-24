"""library_data.py - File handling for the Library Transaction System.

Files used (all plain text, one record per line):
    inventory.csv     title,copies           (read and overwritten)
    loans.csv         borrower,title         (read and overwritten)
    transactions.csv  action,borrower,title,fine   (appended only)
"""

INVENTORY_FILE = "inventory.csv"
LOANS_FILE = "loans.csv"
TRANSACTIONS_FILE = "transactions.csv"

# Dictionary used when inventory.csv is missing or unusable.
DEFAULT_INVENTORY = {
    "Python Crash Course": 3,
    "Clean Code": 2,
    "Intro to Algorithms": 1,
    "Data Structures": 2,
    "Digital Logic": 0,
}


def load_inventory(filename=INVENTORY_FILE):
    """Read title,copies lines into a dictionary {title: copies}.

    Malformed lines are skipped with a warning. If the file is missing or
    has no valid line, a copy of DEFAULT_INVENTORY is returned.
    """
    inventory = {}
    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if line.strip() == "":
                    continue                      # ignore blank lines
                parts = line.strip().split(",")
                if len(parts) != 2 or not parts[1].strip().isdigit():
                    print(f"Warning: skipped malformed line {line_number} "
                          f"in {filename}.")
                    continue
                inventory[parts[0].strip()] = int(parts[1])
    except FileNotFoundError:
        print(f"{filename} not found. Starting with the default catalog.")
        return dict(DEFAULT_INVENTORY)

    if len(inventory) == 0:
        print(f"No valid records in {filename}. Using the default catalog.")
        return dict(DEFAULT_INVENTORY)
    return inventory


def load_loans(inventory, filename=LOANS_FILE):
    """Read borrower,title lines into a list of dictionaries.

    Lines that are malformed or name a book not in the inventory are skipped.
    """
    loans = []
    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if line.strip() == "":
                    continue
                parts = line.strip().split(",")
                if len(parts) != 2 or parts[1] not in inventory:
                    print(f"Warning: skipped malformed line {line_number} "
                          f"in {filename}.")
                    continue
                loans.append({"borrower": parts[0], "title": parts[1]})
    except FileNotFoundError:
        pass                                      # no loans yet is normal
    return loans


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Overwrite the inventory file. Returns True if saved, else False."""
    try:
        with open(filename, "w") as file:
            for title, copies in inventory.items():
                file.write(f"{title},{copies}\n")
        return True
    except OSError as error:
        print(f"Could not save {filename}: {error}")
        return False


def save_loans(loans, filename=LOANS_FILE):
    """Overwrite the loans file. Returns True if saved, else False."""
    try:
        with open(filename, "w") as file:
            for loan in loans:
                file.write(f"{loan['borrower']},{loan['title']}\n")
        return True
    except OSError as error:
        print(f"Could not save {filename}: {error}")
        return False


def log_transaction(action, borrower, title, fine=0.0,
                    filename=TRANSACTIONS_FILE):
    """Append one line to the transaction log (mode 'a' keeps old lines)."""
    try:
        with open(filename, "a") as file:
            file.write(f"{action},{borrower},{title},{fine:.2f}\n")
    except OSError as error:
        print(f"Could not write to {filename}: {error}")
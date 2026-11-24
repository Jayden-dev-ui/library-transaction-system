
import library_data
import library_logic


def show_catalog(inventory):
    """Print every title with its number and available copies."""
    print("\n--- Library Catalog ---")
    titles = list(inventory)                      # list of titles, in order
    for number, title in enumerate(titles, start=1):
        print(f"{number}. {title} (copies available: {inventory[title]})")


def handle_borrow(inventory, loans):
    """Ask for borrow details, apply the rules, then save the changes."""
    show_catalog(inventory)
    titles = list(inventory)
    try:
        choice = input("Enter book number to borrow: ").strip()
        number = library_logic.parse_int_in_range(choice, 1, len(titles))
        title = titles[number - 1]

        name = input("Enter borrower name: ").strip()
        days_text = input(
            f"Days to borrow (1-{library_logic.MAX_LOAN_DAYS}): ").strip()
        library_logic.parse_int_in_range(
            days_text, 1, library_logic.MAX_LOAN_DAYS)

        library_logic.borrow_book(inventory, loans, title, name)
    except ValueError as error:                   # validation errors only
        print(f"Cannot borrow: {error}")
        return

    library_data.save_inventory(inventory)
    library_data.save_loans(loans)
    library_data.log_transaction("BORROW", name, title)
    print(f"Success! {name} borrowed '{title}' for {days_text} day(s).")


def handle_return(inventory, loans):
    """Ask for return details, compute the fine, then save the changes."""
    try:
        name = input("Enter borrower name: ").strip()
        days_text = input("How many days was the book kept? ").strip()
        days_kept = library_logic.parse_int_in_range(days_text, 1, 365)

        title, fine = library_logic.return_book(
            inventory, loans, name, days_kept)
    except ValueError as error:
        print(f"Cannot return: {error}")
        return

    library_data.save_inventory(inventory)
    library_data.save_loans(loans)
    library_data.log_transaction("RETURN", name, title, fine)
    if fine > 0:
        print(f"Overdue! Fine: PHP {fine:.2f}")
    else:
        print("Returned on time. No fine.")
    print(f"'{title}' returned. Thank you, {name}!")


def main():
    """Load saved data, then repeat the menu until the user exits."""
    inventory = library_data.load_inventory()
    loans = library_data.load_loans(inventory)

    running = True
    while running:
        print("\n=== LIBRARY TRANSACTION SYSTEM ===")
        print("1. Borrow a book")
        print("2. Return a book")
        print("3. View available books")
        print("4. Exit")
        try:
            option = input("Choose an option (1-4): ").strip()

            if option == "1":
                handle_borrow(inventory, loans)
            elif option == "2":
                handle_return(inventory, loans)
            elif option == "3":
                show_catalog(inventory)
            elif option == "4":
                print("Goodbye!")
                running = False
            else:
                print("Invalid option. Please enter a number from 1 to 4.")
        except (EOFError, KeyboardInterrupt):     # Ctrl+Z / Ctrl+C / no input
            print("\nInput closed. Exiting.")
            running = False
        except Exception as error:                # unexpected programming bug
            print(f"Unexpected error: {error}")


main()
"""
CS26L - 1st Lab Exam: Project Prototype
Topic: Simple Library Transaction System
SDG 9 - Industry, Innovation and Infrastructure

PROBLEM ANALYSIS
  Inputs     : menu choice, book number, borrower name, days borrowed/kept
  Processing : check book availability, record loans, compute overdue fine
  Outputs    : transaction receipts, fine amount, list of available books
  Conditions : book must have copies left, loan is 1-7 days,
               fine = FINE_PER_DAY for each day kept beyond the loan period

PSEUDOCODE
  repeat until user chooses Exit:
      show menu and read choice
      if 1 (Borrow): validate book number, copies and days -> record loan
      if 2 (Return): find loan by borrower name -> compute fine -> restore copy
      if 3 (View)  : print every book with copies left
      if 4 (Exit)  : stop the loop
      else         : show an invalid-choice message
"""

# ----- Variables and data -----
titles = ["Python Crash Course", "Clean Code", "Intro to Algorithms",
          "Data Structures", "Digital Logic", "Python object oriented programming"]
copies = [1, 3, 0, 5, 4, 6]          # copies currently available per title

loan_names = []                   # borrower of each active loan
loan_books = []                   # book index of each active loan

MAX_LOAN_DAYS = 7                 # allowed loan period (days)
FINE_PER_DAY = 5.0                # fine in pesos per overdue day
total_fines = 0.0                 # fines collected this session


def show_books():
    """Print every book and how many copies are available."""
    print("\n--- Library Catalog ---")
    for i in range(len(titles)):
        print(f"{i + 1}. {titles[i]} (copies available: {copies[i]})")


def borrow_book():
    """Handle a borrowing transaction with input validation."""
    show_books()
    choice = input("Enter book number to borrow: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(titles)):
        print("Invalid book number.")
        return
    index = int(choice) - 1                      # type conversion: str -> int

    if copies[index] == 0:
        print("Sorry, no copies of that book are available.")
        return

    name = input("Enter borrower name: ").strip()
    if name == "":
        print("Name cannot be empty.")
        return

    days_text = input(f"Days to borrow (1-{MAX_LOAN_DAYS}): ").strip()
    if not days_text.isdigit() or not (1 <= int(days_text) <= MAX_LOAN_DAYS):
        print(f"Invalid number of days. Loan must be 1-{MAX_LOAN_DAYS} days.")
        return

    copies[index] -= 1
    loan_names.append(name)
    loan_books.append(index)
    print(f"Success! {name} borrowed '{titles[index]}' for {days_text} day(s).")


def return_book():
    """Handle a return transaction and compute any overdue fine."""
    global total_fines
    name = input("Enter borrower name: ").strip()

    if name not in loan_names:
        print("No active loan found for that name.")
        return

    days_text = input("How many days was the book kept? ").strip()
    if not days_text.isdigit() or int(days_text) < 1:
        print("Invalid number of days.")
        return
    days_kept = int(days_text)

    position = loan_names.index(name)
    book_index = loan_books[position]

    if days_kept > MAX_LOAN_DAYS:
        overdue_days = days_kept - MAX_LOAN_DAYS
        fine = overdue_days * FINE_PER_DAY
        print(f"Overdue by {overdue_days} day(s). Fine: PHP {fine:.2f}")
        total_fines += fine
    else:
        print("Returned on time. No fine.")

    copies[book_index] += 1
    loan_names.pop(position)
    loan_books.pop(position)
    print(f"'{titles[book_index]}' returned. Thank you, {name}!")


# ----- Main program loop -----
running = True
while running:
    print("\n=== LIBRARY TRANSACTION SYSTEM ===")
    print("1. Borrow a book")
    print("2. Return a book")
    print("3. View available books")
    print("4. Exit")
    option = input("Choose an option (1-4): ").strip()

    if option == "1":
        borrow_book()
    elif option == "2":
        return_book()
    elif option == "3":
        show_books()
    elif option == "4":
        print(f"\nTotal fines collected: PHP {total_fines:.2f}")
        print("Goodbye!")
        running = False
    else:
        print("Invalid option. Please enter a number from 1 to 4.")
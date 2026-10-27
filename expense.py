
from tracker.commands import (
    add_expense_command,
    list_expenses_command,
    update_expense_command,
    delete_expense_command,
    monthly_expenses_command,
    monthly_summary_command,
    set_budget_command,
    budgets_command,
    export_expenses_command
)


def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. List Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Monthly Expenses")
        print("6. Monthly Summary")
        print("7. Set Monthly Budget")
        print("8. View All Budgets")
        print("9. Export Expenses to CSV")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                amount = input("Enter amount: ")
                category = input("Enter category: ")
                note = input("Enter note (optional): ")
                spent_on = input("Enter spent on (e.g. dinner): ")

                add_expense_command(
                    amount, category, note, spent_on
                )

            elif choice == "2":
                list_expenses_command()

            elif choice == "3":
                expense_id = int(input("Enter expense ID: "))
                amount = input("Enter new amount: ")
                category = input("Enter new category: ")
                note = input("Enter new note (optional): ")
                spent_on = input("Enter new spent on (e.g. lunch): ")

                update_expense_command(
                    expense_id,
                    amount,
                    category,
                    note,
                    spent_on
                )

            elif choice == "4":
                expense_id = int(input("Enter expense ID: "))
                delete_expense_command(expense_id)

            elif choice == "5":
                month = input("Enter month (YYYY-MM): ")
                monthly_expenses_command(month)

            elif choice == "6":
                month = input("Enter month (YYYY-MM): ")
                monthly_summary_command(month)

            elif choice == "7":
                category = input("Enter category: ")
                amount = input("Enter monthly budget amount: ")
                set_budget_command(category, amount)

            elif choice == "8":
                budgets_command()

            elif choice == "9":
                month = input("Enter month (YYYY-MM): ")
                export_expenses_command(month)

            elif choice == "10":
                print("Exit!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 10.")

        except (ValueError, TypeError) as error:
            print("Error:", error)

        except Exception as error:
            print("Something went wrong:", error)


if __name__ == "__main__":
    main()

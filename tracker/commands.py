
from datetime import date
import csv
from tracker.db import (
    initialize_db,
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_expenses_by_month,
    get_monthly_summary,
    set_monthly_budget,
    get_all_budgets,
    get_monthly_budget,
    get_category_month_total,
    get_highest_expense,
    get_monthly_total,
    export_expenses_by_month
)

from tracker.validators import (
    validate_amount,
    validate_category,
    validate_month,
    validate_note,
    validate_date
)


def add_expense_command(amount, category, note, spent_on):
    amount = validate_amount(amount)
    category = validate_category(category)
    note = validate_note(note)
    spent_on = spent_on.strip()

    if not spent_on:
        raise ValueError("Spent on cannot be empty.")

    initialize_db()

    add_expense(amount, category, note, spent_on)

    print("Expense added successfully!")

    check_budget_warning(category)


def list_expenses_command():
    initialize_db()
    expenses = get_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("\n===== ALL EXPENSES =====")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]} | "
            f"Category: {expense[2]} | "
            f"Note: {expense[3]} | "
            f"Spent on: {expense[4]} | "
            f"Created at: {expense[5]}"
        )


def update_expense_command(
    expense_id, amount, category, note, spent_on
):
    amount = validate_amount(amount)
    category = validate_category(category)
    note = validate_note(note)
    spent_on = spent_on.strip()

    if not spent_on:
        raise ValueError("Spent on cannot be empty.")

    initialize_db()

    updated = update_expense(
        expense_id, amount, category, note, spent_on
    )

    if updated:
        print("Expense updated successfully!")
        check_budget_warning(category)
    else:
        print("Expense ID not found.")


def delete_expense_command(expense_id):
    initialize_db()
    deleted = delete_expense(expense_id)

    if deleted:
        print("Expense deleted successfully!")
    else:
        print("Expense ID not found.")


def monthly_expenses_command(month):
    month = validate_month(month)

    initialize_db()
    expenses = get_expenses_by_month(month)

    if not expenses:
        print("No expenses found for", month)
        return

    print(f"\n===== MONTHLY EXPENSES: {month} =====")

    for expense in expenses:
        (
            expense_id,
            amount,
            category,
            note,
            spent_on,
            created_at,
        ) = expense

        print(f"ID: {expense_id}")
        print(f"Amount: ₹{amount}")
        print(f"Category: {category}")
        print(f"Note: {note}")
        print(f"Spent on: {spent_on}")
        print(f"Created at: {created_at}")
        print("-" * 35)



def monthly_summary_command(month):
    month = validate_month(month)
    initialize_db()

    summary = get_monthly_summary(month)

    if not summary:
        print("No expenses found for", month)
        return

    budget_data = get_all_budgets()
    budgets = {
        category: float(amount)
        for category, amount in budget_data
    }

    total = sum(float(amount) for _, amount in summary)

    print(f"\n===== MONTHLY SUMMARY: {month} =====")
    print("-" * 75)
    print(
        f"{'Category':<18}"
        f"{'Spent':>14}"
        f"{'Budget':>14}"
        f"{'Used %':>12}"
        f"{'% Total':>12}"
    )
    print("-" * 75)

    over_budget = []

    for category, amount in summary:
        spent = float(amount)
        budget = budgets.get(category)

        if budget is not None:
            used = spent / budget * 100

            if spent > budget:
                status = " ✘"
                over_budget.append(category.title())
            else:
                status = ""

            budget_text = f"{budget:,.2f}"
            used_text = f"{used:.1f}%{status}"
        else:
            budget_text = "-"
            used_text = "-"

        total_percent = spent / total * 100 if total else 0

        print(
            f"{category.title():<18}"
            f"{spent:>14,.2f}"
            f"{budget_text:>14}"
            f"{used_text:>12}"
            f"{total_percent:>11.1f}%"
        )

    print("-" * 75)
    print(f"{'TOTAL':<18}{total:>14,.2f}{'':>14}{'':>12}{'100.0%':>12}")

    highest = get_highest_expense(month)

    if highest:
        amount, category, spent_on, created_at = highest
        print(
            f"\nHighest single expense : ₹{float(amount):,.2f} "
            f"({category.title()}, {created_at:%d-%b})"
        )

    monthly_total = float(get_monthly_total(month))

    year, month_number = map(int, month.split("-"))
    today = date.today()

    if (year, month_number) == (today.year, today.month):
        days = today.day
    else:
        import calendar
        days = calendar.monthrange(year, month_number)[1]

    daily_average = monthly_total / days if days else 0
    print(f"Daily average : ₹{daily_average:,.2f} ({days} days)")

    if over_budget:
        print("Over budget :", ", ".join(over_budget))


def set_budget_command(category, amount):
    category = validate_category(category)
    amount = validate_amount(amount)

    initialize_db()
    set_monthly_budget(category, amount)

    print(
        f"{category.title()} budget set successfully: "
        f"₹{amount}"
    )


def budgets_command():
    initialize_db()
    budgets = get_all_budgets()

    if not budgets:
        print("No budgets set yet.")
        return

    print("\n===== MONTHLY BUDGETS =====")
    print(f"{'Category':<20}{'Budget (₹)':>15}")
    print("-" * 35)

    for category, amount in budgets:
        print(f"{category.title():<20}{amount:>15,.2f}")


def check_budget_warning(category):
    month = date.today().strftime("%Y-%m")

    budget = get_monthly_budget(category)

    if budget is None:
        return

    spent = get_category_month_total(category, month)

    budget_value = float(budget)
    spent_value = float(spent)

    percentage = spent_value / budget_value * 100

    if percentage > 100:
        exceeded = spent_value - budget_value

        print(
            f"✘ {category.title()} budget exceeded by "
            f"₹{exceeded:,.2f} "
            f"(₹{spent_value:,.2f} / ₹{budget_value:,.2f})"
        )

    elif percentage >= 80:
        print(
            f"⚠ {category.title()}: "
            f"₹{spent_value:,.2f} of "
            f"₹{budget_value:,.2f} used "
            f"({percentage:.0f}%)"
        )
        

def export_expenses_command(month):
    month = validate_month(month)
    initialize_db()

    expenses = export_expenses_by_month(month)

    if not expenses:
        print(f"No expenses found for {month}.")
        return

    filename = f"expenses_{month}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Amount",
            "Category",
            "Note",
            "Spent On",
            "Created At"
        ])

        writer.writerows(expenses)

    print(f"Expenses exported successfully to {filename}")


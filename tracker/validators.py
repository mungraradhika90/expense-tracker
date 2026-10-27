
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


CATEGORIES = [
    "food",
    "travel",
    "rent",
    "bills",
    "shopping",
    "health",
    "entertainment",
    "other",
]


def validate_amount(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Amount must be a valid number.")

    if not amount.is_finite():
        raise ValueError("Amount must be a finite number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount.as_tuple().exponent < -2:
        raise ValueError("Amount can have at most 2 decimal places.")

    return amount


def validate_category(value):
    category = value.strip().lower()

    if category not in CATEGORIES:
        raise ValueError(
            "Invalid category. Choose: " + ", ".join(CATEGORIES)
        )

    return category


def validate_date(value):
    try:
        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD format.")

    if parsed_date.isoformat() != value:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    if parsed_date > date.today():
        raise ValueError("Date cannot be in the future.")

    return parsed_date


def validate_month(value):
    try:
        parsed_month = datetime.strptime(value, "%Y-%m")
    except (ValueError, TypeError):
        raise ValueError("Month must be in YYYY-MM format.")

    if parsed_month.strftime("%Y-%m") != value:
        raise ValueError("Month must be in YYYY-MM format.")

    return value


def validate_note(value):
    if value is None:
        return ""

    note = value.strip()

    if len(note) > 100:
        raise ValueError("Note cannot exceed 100 characters.")

    return note

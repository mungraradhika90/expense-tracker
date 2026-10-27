
import unittest
from datetime import date

from tracker.validators import (
    validate_amount,
    validate_category,
    validate_month,
    validate_note,
    validate_date
)


class TestValidators(unittest.TestCase):

    def test_valid_amount(self):
        self.assertEqual(validate_amount("150.50"), 150.50)

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            validate_amount("0")

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            validate_amount("-50")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("invalid")

    def test_category_lowercase(self):
        self.assertEqual(validate_category("FOOD"), "food")

    def test_valid_month(self):
        self.assertEqual(validate_month("2026-10"), "2026-10")

    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            validate_month("2026-1")

    def test_note_too_long(self):
        with self.assertRaises(ValueError):
            validate_note("a" * 101)

    def test_valid_date(self):
        self.assertEqual(
            validate_date("2026-10-27"),
            date(2026, 10, 27)
        )

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            validate_date("2026-13-27")

    def test_future_date(self):
        with self.assertRaises(ValueError):
            validate_date("2099-01-01")


if __name__ == "__main__":
    unittest.main()

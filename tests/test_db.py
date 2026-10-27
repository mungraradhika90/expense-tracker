# # from tracker.db import initialize_db, add_expense, get_expenses

# # # Step 1: Create table if needed
# # initialize_db()

# # # Step 2: Add one expense
# # add_expense(150.50, "Food", "Lunch", "2026-10-22")

# # # Step 3: Display all expenses
# # expenses = get_expenses()

# # for expense in expenses:
# #     print(expense)



# import tempfile
# import unittest
# from pathlib import Path

# from tracker.db import initialize_db, add_expense, get_expenses


# class TestExpenseDatabase(unittest.TestCase):

#     def test_add_and_get_expense(self):
#         with tempfile.TemporaryDirectory() as temp_dir:
#             test_db = Path(temp_dir) / "test_expense.db"

#             initialize_db(test_db)

#             add_expense(
#                 150.50,
#                 "Food",
#                 "Lunch",
#                 "2026-10-22",
#                 db_path=test_db
#             )

#             expenses = get_expenses(test_db)

#             self.assertEqual(len(expenses), 1)
#             self.assertEqual(expenses[0][1], 150.50)
#             self.assertEqual(expenses[0][2], "Food")
#             self.assertEqual(expenses[0][3], "Lunch")

# if __name__ == "__main__":
#     unittest.main()


import unittest
from datetime import date

from tracker.db import (
    initialize_db,
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
)


class TestExpenseDB(unittest.TestCase):

    def setUp(self):
        initialize_db()

    def test_add_and_get_expense(self):
        add_expense(
            150.50,
            "food",
            "test lunch",
            date.today(),
        )

        expenses = get_expenses()

        self.assertTrue(
            any(
                expense[1] == 150.50
                and expense[2] == "food"
                and expense[3] == "test lunch"
                for expense in expenses
            )
        )

    def test_update_expense(self):
        add_expense(
            100,
            "travel",
            "old note",
            date.today(),
        )

        expenses = get_expenses()
        expense_id = expenses[-1][0]

        updated = update_expense(
            expense_id,
            200,
            "travel",
            "updated note",
            date.today(),
        )

        self.assertTrue(updated)

        expenses = get_expenses()
        updated_expense = next(
            expense for expense in expenses
            if expense[0] == expense_id
        )

        self.assertEqual(updated_expense[1], 200)
        self.assertEqual(updated_expense[3], "updated note")

        delete_expense(expense_id)

    def test_delete_expense(self):
        add_expense(
            75,
            "food",
            "delete test",
            date.today(),
        )

        expenses = get_expenses()
        expense_id = expenses[-1][0]

        deleted = delete_expense(expense_id)

        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()

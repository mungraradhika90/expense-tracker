import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="expense",
        user="postgres",
        password="admin123",
        host="localhost",
        port="5432"
    )


def initialize_db():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
                    category VARCHAR(20) NOT NULL,
                    note VARCHAR(100) DEFAULT '',
                    spent_on DATE NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets(
                    category VARCHAR(20) PRIMARY KEY,
                    monthly_limit NUMERIC(10,2) NOT NULL
                      CHECK (monthly_limit > 0)
                )
            """)
        conn.commit()
    finally:
        conn.close()
# print(initialize_db() , "table created")

def add_expense(amount, category, note, spent_on):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO expenses (amount, category, note, spent_on)
                VALUES (%s, %s, %s, %s)
            """, (amount, category, note, spent_on))
        conn.commit()
    finally:
        conn.close()


def get_expenses():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, amount, category, note, spent_on, created_at
                FROM expenses
                ORDER BY id
            """)
            return cursor.fetchall()
    finally:
        conn.close()


def update_expense(expense_id, amount, category, note, spent_on):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE expenses
                SET amount = %s, category = %s, note = %s, spent_on = %s
                WHERE id = %s
            """, (amount, category, note, spent_on, expense_id))

            updated = cursor.rowcount > 0

        conn.commit()
        return updated
    finally:
        conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM expenses WHERE id = %s",
                (expense_id,)
            )
            deleted = cursor.rowcount > 0

        conn.commit()
        return deleted
    finally:
        conn.close()


def get_expenses_by_month(month):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, amount, category, note, spent_on, created_at
                FROM expenses
                WHERE TO_CHAR(created_at, 'YYYY-MM') = %s
                ORDER BY created_at, id
            """, (month,))
            return cursor.fetchall()
    finally:
        conn.close()


def get_monthly_summary(month):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT category, SUM(amount)
                FROM expenses
                WHERE TO_CHAR(created_at, 'YYYY-MM') = %s
                GROUP BY category
                ORDER BY SUM(amount) DESC
            """, (month,))

            return cursor.fetchall()

    finally:
        conn.close()

        

def set_monthly_budget(category, amount):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO budgets (category, monthly_limit)
                VALUES (%s, %s)
                ON CONFLICT (category)
                DO UPDATE SET monthly_limit = EXCLUDED.monthly_limit
            """, (category, amount))


def get_monthly_budget(category):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT monthly_limit
                FROM budgets
                WHERE category = %s
            """, (category,))

            result = cursor.fetchone()

            if result is None:
                return None

            return result[0]

def get_all_budgets():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT category, monthly_limit
                FROM budgets
                ORDER BY category
            """)

            return cursor.fetchall()
        

def get_category_month_total(category, month):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE category = %s
                  AND TO_CHAR(created_at, 'YYYY-MM') = %s
            """, (category, month))

            return cursor.fetchone()[0]


def get_highest_expense(month):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT amount, category, spent_on, created_at
                FROM expenses
                WHERE TO_CHAR(created_at, 'YYYY-MM') = %s
                ORDER BY amount DESC
                LIMIT 1
            """, (month,))

            return cursor.fetchone()

    finally:
        conn.close()

def get_monthly_total(month):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE TO_CHAR(created_at, 'YYYY-MM') = %s
            """, (month,))

            return cursor.fetchone()[0]

    finally:
        conn.close()


def export_expenses_by_month(month):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, amount, category, note, spent_on, created_at
                FROM expenses
                WHERE TO_CHAR(created_at, 'YYYY-MM') = %s
                ORDER BY created_at
            """, (month,))
            return cursor.fetchall()
    finally:
        conn.close()




        


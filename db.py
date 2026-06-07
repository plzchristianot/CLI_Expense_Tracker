import sqlite3
from models import Expense


def get_db_connection():
    """Creates the connection safely"""
    conn = sqlite3.connect("sqlite3.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"Something went wrong with the DB: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()


def fetch_all_expenses() -> List[Expense]:
    """Fetch all expenses from the database and return the data in a list of Expense objects"""
    query = "SELECT id, amount, category, description, date FROM expenses;"
    expenses_list = []

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            expense_obj = Expense(
                id=row["id"],
                amount=row["amount"],
                category=row["category"],
                description=row["description"],
                date=row["date"],
            )
            expenses_list.append(expense_obj)

    return expenses_list

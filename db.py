import sqlite3
from contextlib import contextmanager
from typing import List

from models import Expense


class ExpenseRepository:
    def __init__(self, db_name: str = "sqlite3.db"):
        self.db_name = db_name
        self.init_database()

    @contextmanager
    def _get_db_connection(self):
        """Creates the connection safely"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except sqlite3.Error as e:
            print(f"Something went wrong with the DB: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self) -> None:
        """Crea la tabla de gastos si no existe."""
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT DEFAULT (datetime('now', 'localtime'))
        );
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def save(self, expense: Expense) -> None:
        """Persiste un objeto Expense en la base de datos."""
        query = """
        INSERT INTO expenses (amount, category, description)
        VALUES (?, ?, ?);
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (expense.amount, expense.category, expense.description)
            )
            conn.commit()

    def fetch_all_expenses(self) -> List[Expense]:
        """Fetch all expenses from the database and return the data in a list of Expense objects"""
        query = "SELECT id, amount, category, description, date FROM expenses;"
        expenses_list = []

        with self._get_db_connection() as conn:
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

    def fetch_expenses_by_category(self, category: str) -> List[Expense]:
        """Fetch expenses filtering by category selected"""
        query = """SELECT id, amount, category, description, date FROM expenses
                    WHERE category=?;"""
        expenses_list = []

        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (category,))
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

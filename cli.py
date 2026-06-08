import sys

from db import ExpenseRepository
from models import Expense


class ExpenseTrackerCLI:
    def __init__(self):
        self.repo = ExpenseRepository()

    def showMenu(self):
        print("*" * 40)
        print("  Welcome to this CLI Expense Tracker!")
        print("*" * 40 + "\n")
        print("1. Register a new expense")
        print("2. Show all expenses")
        print("3. Show expenses by category")
        print("4. Delete an expense from the database")
        print("5. Exit")

    def main(self):
        """Initializes the app"""
        while True:
            self.showMenu()
            option = input("Select one option (1-4): ")

            if option == "1":
                self._registerExpense()
            elif option == "2":
                self._showAllExpenses()
            elif option == "3":
                self._showExpensesByCategory()
            elif option == "4":
                self._removeExpense()
            elif option == "5":
                sys.exit()
            else:
                print("No valid option selected!\n")

    def _registerExpense(self) -> None:
        """Register a new expense with category and description"""
        print("\nRegister a new expense")
        try:
            amount = float(input("Enter an amount $: "))
            category = input("Enter a category: ").strip()
            description = input("Enter a description: ").strip()

            description = description if description else None

            new_Expense = Expense(
                amount=amount, category=category, description=description
            )

            self.repo.save(new_Expense)
            print("Expense saved successfully!")
        except ValueError:
            print("\n Error: the amount must be a valid number")

    def _showAllExpenses(self) -> None:
        """Retrieve all registries in DB and show them"""
        expenses = self.repo.fetch_all_expenses()

        if not expenses:
            print("There is no expenses registered yet\n")
            return

        print("\nThese are all the expenses registered")

        for e in expenses:
            print(
                f"ID:{e.id} | Amount {e.amount} | Date: {e.date} | Category: {e.category} | Description: {e.description or 'NA'}"
            )

    def _showExpensesByCategory(self) -> None:
        """Retrieve expenses and filter them by category"""
        category = input("Enter a category to filter: ")
        expenses = self.repo.fetch_expenses_by_category(category=category)

        if not expenses:
            print(f"There is no expenses with this category: {category}\n")
            return

        for e in expenses:
            print(
                f"ID:{e.id} | Amount {e.amount} | Date: {e.date} | Category: {e.category} | Description: {e.description or 'NA'}"
            )

    def _removeExpense(self) -> None:
        """Remove a selected expense from DB"""
        self._showAllExpenses()
        try:
            id = int(input("Enter the expense ID to remove from DB: "))
            confirmation = input(
                f"Are you sure you want to remove this registry {id}? (s/n)"
            )

            if confirmation == "s":
                expense_deleted = self.repo.remove_expense(id=id)
                if expense_deleted:
                    print(f"Expense with ID{id} deleted successfully")
                else:
                    print(f"There is no expense with ID: {id}")
            else:
                print("\nOperation cancelled")

        except ValueError:
            print("Error: Please enter a valid expense number")


if __name__ == "__main__":
    app = ExpenseTrackerCLI()
    app.main()

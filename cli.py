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
        print("4. Exit")

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

    def _showAllExpenses(self):
        """Retrieve all registries in DB and show them"""
        print("This are all the expenses registered")
        expenses = self.repo.fetch_all_expenses()

        if not expenses:
            print("There is no expenses registered yet\n")
            return

        for e in expenses:
            print(
                f"ID:{e.id} | Amount {e.amount} | Date: {e.date} | Category: {e.category} | Description: {e.description or 'NA'}"
            )

    def _showExpensesByCategory(self):
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


if __name__ == "__main__":
    app = ExpenseTrackerCLI()
    app.main()

import json
import os
from datetime import datetime

class Transaction:
    """Represents a single financial transaction (Income or Expense)."""
    def __init__(self, t_type, amount, category, description, date=None):
        self.t_type = t_type  # 'Income' or 'Expense'
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "t_type": self.t_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

class ExpenseTracker:
    """Manages transactions, file persistence, and basic analytics."""
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.transactions = []
        self.budgets = {}
        self.load_data()

    def load_data(self):
        """Loads transaction data from a local JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.transactions = [Transaction(**t) for t in data.get("transactions", [])]
                    self.budgets = data.get("budgets", {})
            except Exception as e:
                print(f"Error loading data: {e}. Starting with empty records.")

    def save_data(self):
        """Saves transaction and budget data to a local JSON file."""
        try:
            data = {
                "transactions": [t.to_dict() for t in self.transactions],
                "budgets": self.budgets
            }
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_transaction(self, t_type):
        """Adds a new income or expense transaction with validation."""
        print(f"\n--- Add {t_type} ---")
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
            
            category = input("Enter category (e.g., Food, Rent, Salary): ").strip().capitalize()
            description = input("Enter brief description: ").strip()
            
            date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_str:
                # Validate date format
                datetime.strptime(date_str, "%Y-%m-%d")
                tx_date = date_str
            else:
                tx_date = None

            new_tx = Transaction(t_type, amount, category, description, tx_date)
            self.transactions.append(new_tx)
            self.save_data()
            print(f"Success: {t_type} added successfully!")

            # Check budget if it's an expense
            if t_type == "Expense" and category in self.budgets:
                total_spent = sum(t.amount for t in self.transactions if t.t_type == "Expense" and t.category == category)
                if total_spent > self.budgets[category]:
                    print(f"⚠️ Budget Alert: You have exceeded your budget for '{category}'! Budget: {self.budgets[category]}, Spent: {total_spent}")

        except ValueError as ve:
            print(f"Invalid input format: {ve}. Please try again.")

    def view_transactions(self):
        """Displays all recorded transactions in a clean format."""
        if not self.transactions:
            print("\nNo transactions recorded yet.")
            return

        print("\n" + "="*70)
        print(f"{'Date':<12} | {'Type':<8} | {'Category':<12} | {'Amount':<10} | {'Description'}")
        print("="*70)
        for t in self.transactions:
            print(f"{t.date:<12} | {t.t_type:<8} | {t.category:<12} | {t.amount:<10.2f} | {t.description}")
        print("="*70)

    def set_budget(self):
        """Sets a monthly budget limit for a specific category."""
        print("\n--- Set Category Budget ---")
        category = input("Enter category name: ").strip().capitalize()
        try:
            limit = float(input(f"Enter budget limit for {category}: "))
            if limit < 0:
                print("Budget limit cannot be negative.")
                return
            self.budgets[category] = limit
            self.save_data()
            print(f"Budget of {limit} set for category '{category}'.")
        except ValueError:
            print("Please enter a valid numerical amount.")

    def show_summary(self):
        """Displays financial summary including total income, expense, net balance, and budget statuses."""
        total_income = sum(t.amount for t in self.transactions if t.t_type == "Income")
        total_expense = sum(t.amount for t in self.transactions if t.t_type == "Expense")
        net_balance = total_income - total_expense

        print("\n" + "--- Financial Summary ---")
        print(f"Total Income   : {total_income:.2f}")
        print(f"Total Expenses : {total_expense:.2f}")
        print(f"Net Balance    : {net_balance:.2f}")

        if self.budgets:
            print("\n--- Budget Status ---")
            for cat, limit in self.budgets.items():
                spent = sum(t.amount for t in self.transactions if t.t_type == "Expense" and t.category == cat)
                status = f"Spent {spent:.2f} of {limit:.2f}"
                if spent > limit:
                    status += " (OVER BUDGET!)"
                else:
                    status += f" (Remaining: {limit - spent:.2f})"
                print(f"- {cat}: {status}")

def main():
    tracker = ExpenseTracker()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Set Category Budget")
        print("5. View Financial Summary & Budgets")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == '1':
            tracker.add_transaction("Income")
        elif choice == '2':
            tracker.add_transaction("Expense")
        elif choice == '3':
            tracker.view_transactions()
        elif choice == '4':
            tracker.set_budget()
        elif choice == '5':
            tracker.show_summary()
        elif choice == '6':
            print("\nThank you for using Personal Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
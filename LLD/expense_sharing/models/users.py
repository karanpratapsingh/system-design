from typing import Dict


class User:
    user_id: str
    name: str
    email: str
    user_balance_mapping: Dict[str, int]
    expenses = []

    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.user_balance_mapping = {}
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def show_expense(self):
        formatted_output = []
        for user_id, amount in self.user_balance_mapping.items():
            if amount < 0:
                formatted_output.append(f'{self.user_id} owes {user_id}: {-amount}')
            elif amount > 0:
                formatted_output.append(f'{user_id} owes {self.user_id}: {amount}')
        if formatted_output:
            print('\n'.join(formatted_output))
        else:
            print('No balances')
        print()

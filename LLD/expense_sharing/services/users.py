from typing import Dict

from expense_sharing.models import users as users_models
from expense_sharing import exceptions


class UserService:
    users: Dict[str, users_models.User]

    def __init__(self):
        self.users = {}

    def get_user(self, user_id):
        return self.users.get(user_id)

    def add_user(self, user_id, name='', email=''):
        if user_id in self.users:
            raise exceptions.UserAlreadyExist()
        user = users_models.User(user_id, name, email)
        self.users[user.user_id] = user
        return user

    def get_or_add_user(self, user_id, name='', email=''):
        user = self.get_user(user_id)
        if not user:
            user = self.add_user(user_id, name, email)
        return user

    def show_expense(self):
        formatted_output = []
        for user in self.users.values():
            user_output = []
            for user_id, amount in user.user_balance_mapping.items():
                if amount < 0:
                    user_output.append(f'{user.user_id} owes {user_id}: {-amount}')
                elif amount > 0:
                    user_output.append(f'{user_id} owes {user.user_id}: {amount}')
            if user_output:
                formatted_output.append(f'{user.user_id} Expense data')
                formatted_output.extend(user_output)
        if formatted_output:
            print('\n'.join(formatted_output))
        else:
            print('No balances')
        print()


user_service = UserService()

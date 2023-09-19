from typing import List, Dict

from expense_sharing.models import users as users_models


class Expense:
    total_amount: int
    paid_by: users_models.User
    user_shares: Dict[users_models.User, int]

    def __init__(self, paid_by: users_models.User, total_amount: int, user_shares):
        self.paid_by = paid_by
        self.total_amount = total_amount
        self.user_shares = user_shares

    def update_user_calculation(self):
        """
        Update each user's user-balance-mapping to update consolidated data
        """
        for user, amount in self.user_shares.items():
            user.add_expense(self)
            if user != self.paid_by:
                # Update  paid by user mapping
                if user.user_id in self.paid_by.user_balance_mapping:
                    self.paid_by.user_balance_mapping[user.user_id] += amount
                else:
                    self.paid_by.user_balance_mapping[user.user_id] = amount

                # Update other participants mapping
                if self.paid_by.user_id in user.user_balance_mapping:
                    user.user_balance_mapping[self.paid_by.user_id] -= amount
                else:
                    user.user_balance_mapping[self.paid_by.user_id] = -amount

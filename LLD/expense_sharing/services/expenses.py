from typing import List

from expense_sharing import exceptions
from expense_sharing.models import expenses as expense_models
from expense_sharing.services.users import user_service

EXACT = 'EXACT'
EQUAL = 'EQUAL'


class ExpenseService:

    @staticmethod
    def add_equal_expense(paid_by, total_amount, participants):
        users_shares = {}
        total_participants = len(participants)
        # Calculate share of each user
        for index in range(total_participants):
            user = user_service.get_or_add_user(participants[index])
            users_shares[user] = total_amount / total_participants

        expense = expense_models.Expense(
            user_service.get_or_add_user(paid_by),
            total_amount,
            users_shares
        )
        expense.update_user_calculation()

    @staticmethod
    def add_exact_expense(paid_by, total_amount, participants, shares: List[int]):
        users_shares = {}
        total_participants = len(participants)

        if total_amount == sum(shares):
            for index in range(total_participants):
                user = user_service.get_or_add_user(participants[index])
                users_shares[user] = shares[index]
        else:
            raise exceptions.InValidAmount()

        expense = expense_models.Expense(
            user_service.get_or_add_user(paid_by),
            total_amount,
            users_shares
        )
        expense.update_user_calculation()


expense_service = ExpenseService()

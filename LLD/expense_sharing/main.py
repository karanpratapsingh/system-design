# Python3.7

from expense_sharing.services.users import user_service
from expense_sharing.services.expenses import expense_service


user_service.show_expense()
user_service.get_or_add_user('user1').show_expense()
expense_service.add_equal_expense('user1', 1000, ['user1', 'user2', 'user3', 'user4'])
user_service.get_or_add_user('user4').show_expense()
user_service.get_or_add_user('user1').show_expense()
expense_service.add_exact_expense('user1', 1250, ['user2', 'user3'], [370, 880])
user_service.show_expense()
# user_service.get_or_add_user('user1').show_expense()
# user_service.show_expense()

class InValidAmount(Exception):
    message = 'Total amount and user shares are not matching'


class UserAlreadyExist(Exception):
    message = 'User already exists'

class InvalidUserIdError(Exception):
    def __init__(self):
        self.answer = 'Invalid User Id'


class InvalidPasswordError(Exception):
    def __init__(self):
        self.answer = 'Invalid Password'


class UserNotFoundError(Exception):
    def __init__(self):
        self.answer = 'User Not Found'

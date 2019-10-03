class InvalidUserIdError(Exception):
    def __init__(self):
        self.answer = 'Invalid User Id'

    def __str__(self):
        return self.answer


class InvalidPasswordError(Exception):
    def __init__(self):
        self.answer = 'Invalid Password'

    def __str__(self):
        return self.answer


class UserNotFoundError(Exception):
    def __init__(self):
        self.answer = 'User Not Found'

    def __str__(self):
        return self.answer


class InvalidUserOrPassword(Exception):
    def __init__(self):
        self.answer = 'Invalid User or Password'

    def __str__(self):
        return self.answer

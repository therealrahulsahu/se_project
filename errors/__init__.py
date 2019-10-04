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


class InvalidEmailError(Exception):
    def __init__(self):
        self.answer = 'Invalid Mail Address'

    def __str__(self):
        return self.answer


class TableNoError(Exception):
    def __init__(self):
        self.answer = 'Invalid Table No.'

    def __str__(self):
        return self.answer


class InvalidPhoneError(Exception):
    def __init__(self):
        self.answer = 'Invalid Phone No.'

    def __str__(self):
        return self.answer


class InvalidNameError(Exception):
    def __init__(self):
        self.answer = 'Invalid Name'

    def __str__(self):
        return self.answer


class TableAlreadyOccupiedError(Exception):
    def __init__(self):
        self.answer = 'Table Already Occupied'

    def __str__(self):
        return self.answer


class OrderNotCreatedSuccessfullyError(Exception):
    def __init__(self):
        self.answer = 'Order Not Created Successfully'

    def __str__(self):
        return self.answer


class CustomerAlreadyInError(Exception):
    def __init__(self):
        self.answer = 'Customer Already Inside'

    def __str__(self):
        return self.answer

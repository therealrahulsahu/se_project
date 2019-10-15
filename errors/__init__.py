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
    def __init__(self, customer_id, name):
        self.answer = 'Customer Already Inside'
        self.customer_id = customer_id
        self.name = name

    def __str__(self):
        return self.answer


class InvalidBoolError(Exception):
    def __init__(self):
        self.answer = 'Invalid Boolean Condition'

    def __str__(self):
        return self.answer


class InvalidRegionError(Exception):
    def __init__(self):
        self.answer = 'Invalid Region'

    def __str__(self):
        return self.answer


class InvalidTypeError(Exception):
    def __init__(self):
        self.answer = 'Invalid Type'

    def __str__(self):
        return self.answer


class InvalidPriceError(Exception):
    def __init__(self):
        self.answer = 'Invalid Price'

    def __str__(self):
        return self.answer


class FoodAlreadyAvailableError(Exception):
    def __init__(self):
        self.answer = 'Food Already Available'

    def __str__(self):
        return self.answer


class FoodNotFoundError(Exception):
    def __init__(self):
        self.answer = 'No Food Found'

    def __str__(self):
        return self.answer


class ChefNotFoundError(Exception):
    def __init__(self):
        self.answer = 'No Chef Found'

    def __str__(self):
        return self.answer


class ChefAlreadyExistsError(Exception):
    def __init__(self):
        self.answer = 'Chef Already Exists'

    def __str__(self):
        return self.answer


class PasswordNotMatchError(Exception):
    def __init__(self):
        self.answer = 'Password Does Not Match'

    def __str__(self):
        return self.answer


class NoFoodSelectedError(Exception):
    def __init__(self):
        self.answer = 'No Food Selected'

    def __str__(self):
        return self.answer


class CantRemoveOrderPreparingError(Exception):
    def __init__(self):
        self.answer = 'Can\'t Remove - Order is Now Taken'

    def __str__(self):
        return self.answer


class NoOrdersFoundError(Exception):
    def __init__(self):
        self.answer = 'No Orders Found'

    def __str__(self):
        return self.answer


class RefreshError(Exception):
    def __init__(self):
        self.answer = 'Refresh Expired'

    def __str__(self):
        return self.answer


class SomeOrdersPreparingError(Exception):
    def __init__(self):
        self.answer = 'Some Orders are Preparing'

    def __str__(self):
        return self.answer


class CustomerNotDoneYetError(Exception):
    def __init__(self):
        self.answer = 'Customer Not Done Yet'

    def __str__(self):
        return self.answer


class InvalidTimeEntryError(Exception):
    def __init__(self):
        self.answer = 'Invalid Time Entry'

    def __str__(self):
        return self.answer

class UserNotFoundException(Exception):
    """Raised when user with specified email is not found"""

    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class InvalidEmailException(Exception):
    """Raised when an invalid email is passed"""

    def __init__(self, message="Invalid email"):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordException(Exception):
    """Raised when an invalid password is passed"""

    def __init__(self, message="Invalid password"):
        self.message = message
        super().__init__(self.message)

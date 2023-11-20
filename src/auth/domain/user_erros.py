class UserDatabaseError(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "User Database error"


class UserNotFound(Exception):
    """Raised when a consolidated portfolio is not found."""

    def __init__(self, message="User Not Found."):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class UsernameAlreadyRegistered(Exception):
    """Raised when a consolidated portfolio is not found."""

    def __init__(self, message="Username is already registered."):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class UserUnexpectedError(Exception):
    """Raised for unexpected errors in consolidated portfolio processing."""

    def __str__(self):
        return "User Unexpected error"

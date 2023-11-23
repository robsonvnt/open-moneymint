class AccountError(Exception):
    """Base class for account-related errors."""
    pass


class AccountAlreadyExists(AccountError):
    """Raised when a account already exists."""

    def __str__(self):
        return "Account already exists"


class AccountNotFound(AccountError):
    """Raised when a account is not found."""

    def __str__(self):
        return "Account not found"


class AccountDatabaseError(AccountError):
    """Raised for general database errors in accounts."""

    def __str__(self):
        return "Database error"


class AccountUnexpectedError(AccountError):
    """Raised for unexpected errors in account processing."""

    def __str__(self):
        return "Unexpected error"


class AccountOperationNotPermittedError(AccountError):
    """Raised when an operation on a account is not permitted."""

    def __str__(self):
        return "Operation not permitted"

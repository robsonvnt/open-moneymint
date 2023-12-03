class ConsolidatedAccountError(Exception):
    """Base class for account-related errors."""
    pass


class ConsolidatedAccountAlreadyExists(ConsolidatedAccountError):
    """Raised when a consolidated account already exists."""

    def __str__(self):
        return "Account already exists"


class ConsolidatedAccountNotFound(ConsolidatedAccountError):
    """Raised when a consolidated account is not found."""

    def __str__(self):
        return "Account not found"


class ConsolidatedAccountDatabaseError(ConsolidatedAccountError):
    """Raised for general database errors in accounts."""

    def __str__(self):
        return "Database error"


class ConsolidatedAccountUnexpectedError(ConsolidatedAccountError):
    """Raised for unexpected errors in consolidated account processing."""

    def __str__(self):
        return "Unexpected error"


class ConsolidatedAccountOperationNotPermittedError(ConsolidatedAccountError):
    """Raised when an operation on a consolidated account is not permitted."""

    def __str__(self):
        return "Operation not permitted"

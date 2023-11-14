class InvestmentError(Exception):
    """Base class for investment-related errors."""
    pass


class AlreadyExistsError(InvestmentError):
    """Raised when an investment already exists."""

    def __str__(self):
        return "Investment already exists"


class InvestmentNotFound(InvestmentError):
    """Raised when an investment is not found."""

    def __str__(self):
        return "Investment not found"


class ColumnDoesNotExistError(InvestmentError):
    """Raised when a specified column does not exist."""

    def __str__(self):
        return "Column does not exist"


class DatabaseError(InvestmentError):
    """Raised for general database errors."""

    def __str__(self):
        return "Database error"


class UnexpectedError(InvestmentError):
    """Raised for unexpected errors."""

    def __str__(self):
        return "Unexpected error"


class NoAssetsFound(InvestmentError):
    """Raised when no assets are found."""

    def __str__(self):
        return "No Assets Found error"


class OperationNotPermittedError(InvestmentError):
    """Raised when an operation is not permitted."""

    def __str__(self):
        return "Operation not permitted"

class AccountConsolidationError(Exception):
    """Base class for consolidation-related errors."""
    pass


class AccountConsolidationAlreadyExists(AccountConsolidationError):
    """Raised when a consolidation already exists."""

    def __str__(self):
        return "AccountConsolidation already exists"


class AccountConsolidationNotFound(AccountConsolidationError):
    """Raised when a consolidation is not found."""

    def __str__(self):
        return "AccountConsolidation not found"


class AccountDatabaseConsolidationError(AccountConsolidationError):
    """Raised for general database errors in consolidation."""

    def __str__(self):
        return "Database error"


class AccountUnexpectedConsolidationError(AccountConsolidationError):
    """Raised for unexpected errors in consolidation processing."""

    def __str__(self):
        return "Unexpected error"


class AccountOperationNotPermittedConsolidationError(AccountConsolidationError):
    """Raised when an operation on a consolidation is not permitted."""

    def __str__(self):
        return "Operation not permitted"

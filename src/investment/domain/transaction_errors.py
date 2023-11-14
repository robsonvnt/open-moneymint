class TransactionError(Exception):
    """Base class for transaction-related errors."""
    pass


class TransactionNotFound(TransactionError):
    """Raised when a transaction is not found."""

    def __str__(self):
        return "Transaction not found"


class TransactionDatabaseError(TransactionError):
    """Raised for general database errors in transactions."""

    def __str__(self):
        return "Database error"


class TransactionUnexpectedError(TransactionError):
    """Raised for unexpected errors in transaction processing."""

    def __str__(self):
        return "Unexpected error"


class TransactionOperationNotPermittedError(TransactionError):
    """Raised when an operation on a transaction is not permitted."""

    def __str__(self):
        return "Operation not permitted"


class TransactionInvalidType(TransactionError):
    """Raised when a transaction type is not appropriate for the specific investment."""

    def __str__(self):
        return "The transaction type is invalid for this specific investment. Please ensure the transaction type aligns with the investment's requirements."

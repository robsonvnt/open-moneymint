class FinancialTransactionError(Exception):
    """Base class for financial transaction-related errors."""
    pass


class FinancialTransactionAlreadyExists(FinancialTransactionError):
    """Raised when a financial transaction already exists."""

    def __str__(self):
        return "Financial transaction already exists"


class FinancialTransactionNotFound(FinancialTransactionError):
    """Raised when a financial transaction is not found."""

    def __str__(self):
        return "Financial transaction not found"


class FinancialTransactionDatabaseError(FinancialTransactionError):
    """Raised for general database errors in financial transactions."""

    def __str__(self):
        return "Database error in financial transactions"


class FinancialTransactionUnexpectedError(FinancialTransactionError):
    """Raised for unexpected errors in financial transaction processing."""

    def __str__(self):
        return "Unexpected error in financial transaction processing"


class FinancialTransactionOperationNotPermittedError(FinancialTransactionError):
    """Raised when an operation on a financial transaction is not permitted."""

    def __init__(self, message="Operation not permitted on financial transaction"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

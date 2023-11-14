class ConsolidatedPortfolioDatabaseError(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "Database error"


class ConsolidatedPortfolioNotFound(Exception):
    """Raised when a consolidated portfolio is not found."""

    def __str__(self):
        return "ConsolidatedPortfolio Not Found."


class ConsolidatedPortfolioUnexpectedError(Exception):
    """Raised for unexpected errors in consolidated portfolio processing."""

    def __str__(self):
        return "Unexpected error"

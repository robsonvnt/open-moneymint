class PortfolioError(Exception):
    """Base class for portfolio-related errors."""
    pass


class PortfolioAlreadyExists(PortfolioError):
    """Raised when a portfolio already exists."""

    def __str__(self):
        return "Portfolio already exists"


class PortfolioNotFound(PortfolioError):
    """Raised when a portfolio is not found."""

    def __str__(self):
        return "Portfolio not found"


class PortfolioDatabaseError(PortfolioError):
    """Raised for general database errors in portfolios."""

    def __str__(self):
        return "Database error"


class PortfolioUnexpectedError(PortfolioError):
    """Raised for unexpected errors in portfolio processing."""

    def __str__(self):
        return "Unexpected error"


class PortfolioOperationNotPermittedError(PortfolioError):
    """Raised when an operation on a portfolio is not permitted."""

    def __str__(self):
        return "Operation not permitted"

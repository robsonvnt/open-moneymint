class ExpiredToken(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "Expired Token error"


class InvalidToken(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "Invalid Token error"


class SecretKeyNotSet(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "SECRET_KEY env variable not set"



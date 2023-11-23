class CategoryError(Exception):
    """Base class for category-related errors."""
    pass


class CategoryAlreadyExists(CategoryError):
    """Raised when a category already exists."""

    def __str__(self):
        return "Category already exists"


class CategoryNotFound(CategoryError):
    """Raised when a category is not found."""

    def __str__(self):
        return "Category not found"


class CategoryDatabaseError(CategoryError):
    """Raised for general database errors in categorys."""

    def __str__(self):
        return "Database error"


class CategoryUnexpectedError(CategoryError):
    """Raised for unexpected errors in category processing."""

    def __str__(self):
        return "Unexpected error"


class CategoryOperationNotPermittedError(CategoryError):
    """Raised when an operation on a category is not permitted."""

    def __init__(self, message="Operation not permitted"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

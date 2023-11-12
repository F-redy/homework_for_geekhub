class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


class UserExistsError(Exception):
    """Exception raised for attempts to register an existing user."""
    pass


class UserNotFoundError(Exception):
    """Exception raised when a user is not found during authentication."""


class IncorrectPasswordError(Exception):
    """Exception raised when an incorrect password is provided during authentication."""

"""Exception classes"""

class DomainError(Exception):
    """Base class for all domain-related errors."""
    pass


class MediaAlreadyExistsError(DomainError):
    """Raised when trying to add a media title that already exists."""
    pass


class MediaNotFoundError(DomainError):
    """Raised when media with given ID does not exist."""
    pass


class MediaAlreadySoldOut(DomainError):
    """Raised when Media.quantity = 0"""
    pass


class InvalidValueError(DomainError):
    """Raised when Media.price is changed to negative value"""
    pass

class InvalidKeyError(DomainError):
    """Raised when provided key is invalid for the query"""
    pass
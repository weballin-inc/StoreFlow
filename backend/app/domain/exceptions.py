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
    """Raised when Media.Amount = 0"""
    pass
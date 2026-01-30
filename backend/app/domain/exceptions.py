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

class CopyNotFoundError(DomainError):
    """Raised when copy with given ID does not exist."""
    pass

class CopyAlreadySoldError(DomainError):
    """Raised when copy with given ID has already status SOLD"""
    pass


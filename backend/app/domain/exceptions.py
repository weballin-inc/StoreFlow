class DomainError(Exception):
    """Base class for all domain-related errors."""
    pass

class MediaAlreadyExistsError(DomainError):
    """Raised when trying to add a media title that already exists."""
    pass
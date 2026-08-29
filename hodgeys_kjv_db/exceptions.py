class KJVError(Exception):
    """Base exception for all errors raised by the KJV library."""
    pass

class KJVIndexError(KJVError, IndexError):
    """Raised when a queried Testament, Book, Chapter, or Verse index does not exist."""
    pass
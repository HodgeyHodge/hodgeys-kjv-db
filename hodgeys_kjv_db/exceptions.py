class KJVError(Exception):
    """
    Base custom index error exception from which the others derive
    """
    pass

class KJVIndexError(KJVError):
    """
    Raise when the bible doesn't contain the testament queried
    """
    pass
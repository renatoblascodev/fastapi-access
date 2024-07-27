class DatabaseException(Exception):
    """Raise exception for database exception"""


class EntityNotFound(DatabaseException):
    """Raise exception when entity not found"""


class IntegrityConstraintViolation(DatabaseException):
    """Raise exception when violates integrity constraint"""

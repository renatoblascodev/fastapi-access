from enum import Enum, unique


@unique
class UserRole(Enum):
    """User Role enum"""

    ADMINISTRATOR = "ADMINISTRATOR"
    OWNER = "OWNER"
    OPERATOR_WRITE = "OPERATOR_WRITE"
    OPERATOR_READ = "OPERATOR_READ"

    def __str__(self):
        return self.name


@unique
class UserOrganizationRole(Enum):
    """User Invite Role enum"""

    OPERATOR_WRITE = "OPERATOR_WRITE"
    OPERATOR_READ = "OPERATOR_READ"

    def __str__(self):
        return self.name


@unique
class UserStatus(Enum):
    """User Status enum"""

    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    def __str__(self):
        return self.name

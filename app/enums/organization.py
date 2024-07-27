from enum import Enum, unique


@unique
class OrganizationStatus(Enum):
    """Organization Status enum"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    def __str__(self):
        return self.name


@unique
class OrganizationProvider(Enum):
    """Providers enum"""

    AWS = "AWS"
    AZR = "AZR"
    GCP = "GCP"

    def __str__(self):
        return self.name

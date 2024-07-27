from enum import Enum, unique


@unique
class VoucherStatus(Enum):
    """Voucher Status enum"""

    IN_USE = "IN_USE"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    def __str__(self):
        return self.name


@unique
class PaymentMethod(Enum):
    """Payment Method enum"""

    VOUCHER = "VOUCHER"

    def __str__(self):
        return self.name


@unique
class PaymentStatus(Enum):
    """Payment Status enum"""

    OPEN = "OPEN"
    DONE = "DONE"

    def __str__(self):
        return self.name

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    COMPANY_ADMIN = "COMPANY_ADMIN"

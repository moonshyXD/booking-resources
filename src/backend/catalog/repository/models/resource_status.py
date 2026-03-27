import enum


class ResourceStatus(str, enum.Enum):
    FREE = "FREE"
    FULL = "FULL"
    MAINTENANCE = "MAINTENANCE"
    DELETED = "DELETED"

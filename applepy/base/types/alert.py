from enum import Enum


class AlertStyle(Enum):
    warning = 0
    informational = 1
    critical = 2


class AlertResponse(Enum):
    ok = 1000
    yes = 1000
    cancel = 1001
    no = 1001

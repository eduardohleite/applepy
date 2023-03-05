from typing import NamedTuple, Callable, Optional
from enum import Enum


class AlertStyle(Enum):
    warning = 0
    informational = 1
    critical = 2


class AlertResponse(Enum):
    ack = 0
    ok = 1000
    yes = 1000
    cancel = 1001
    no = 1001


class DialogResponse(Enum):
    cancel = 0
    continue_ = 1
    stop = 2
    abort = 3


class AlertActionStyle(Enum):
    default = 0
    cancel = 1
    destructive = 2


class AlertAction(NamedTuple):
    title: str
    style: AlertActionStyle
    action: Optional[Callable]

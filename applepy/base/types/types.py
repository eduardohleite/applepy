from typing import NamedTuple
from dataclasses import dataclass

from ..binding import BindableMixin


class Padding(NamedTuple):
    bottom: float
    left: float
    right: float
    top: float


@dataclass
class Point(BindableMixin):
    x: int
    y: int


@dataclass
class Size(BindableMixin):
    width: int
    height: int

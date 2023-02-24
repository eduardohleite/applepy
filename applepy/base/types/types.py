from dataclasses import dataclass

from ..binding import BindableMixin


@dataclass
class Padding(BindableMixin):
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

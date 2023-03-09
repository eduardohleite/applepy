from dataclasses import dataclass
from enum import Enum

from ..binding import BindableMixin


@dataclass
class Padding(BindableMixin):
    bottom: float
    left: float
    right: float
    top: float


@dataclass
class Point(BindableMixin):
    x: float
    y: float


@dataclass
class Size(BindableMixin):
    width: float
    height: float


class BoxType(BindableMixin, Enum):
    primary = 0
    separator = 2
    custom = 4


class BorderType(BindableMixin, Enum):
    no_border = 0
    line = 1
    bezel = 2
    groove = 3


class TitlePosition(BindableMixin, Enum):
    no_title = 0
    above_top = 1
    at_top = 2
    below_top = 3
    above_bottom = 4
    at_bottom = 5
    below_bottom = 6

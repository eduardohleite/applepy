from enum import Enum

from ..binding import BindableMixin


class Alignment(BindableMixin, Enum):
    left = 1
    right = 2
    top = 3
    bottom = 4
    leading = 5
    trailing = 6
    width = 7
    height = 8
    center_x = 9
    center_y = 10
    last_baseline = 11
    first_baseline = 12
    left_marging = 13
    right_margin = 14


class StackOrientation(BindableMixin, Enum):
    horizontal = 0
    vertical = 1


class StackDistribution(BindableMixin, Enum):
    equal_centering = 4
    equal_spacing = 3
    fill = 0
    fill_equally = 1
    fill_proportionally = 2
    gravity_areas = -1

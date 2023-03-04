from enum import Enum

from ..binding import BindableMixin


class Alignment(BindableMixin, Enum):
    macos_left = 1
    macos_right = 2
    macos_top = 3
    macos_bottom = 4
    macos_leading = 5
    macos_trailing = 6
    macos_width = 7
    macos_height = 8
    macos_center_x = 9
    macos_center_y = 10
    macos_last_baseline = 11
    macos_first_baseline = 12
    macos_left_marging = 13
    macos_right_margin = 14

    ios_fill = 0
    ios_center = 3
    ios_leading = 1
    ios_trailing = 4
    ios_top = ios_leading
    ios_bottom = ios_trailing
    ios_first_baseline = 2
    ios_last_baseline = 5


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

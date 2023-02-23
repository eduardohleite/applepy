from enum import Enum
from typing import NamedTuple

from .base.app import App, StatusBarApp, get_current_app
from .base.scene import Scene
from .base.view import View, StackedView, PartialView
from .base.types import Color, Padding, Image, Size, Point

from .base.binding import (
    bindable,
    Signal,
    Binding,
    BindingExpression,
    AbstractBinding,
    BindableMixin
)


class Alignment(Enum):
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

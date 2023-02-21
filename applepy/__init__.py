from abc import ABC
from typing import NamedTuple

from .base.app import App, get_current_app
from .base.scene import Scene
from .base.view import View, StackedView
from .base.types import Color

from .base.binding import (
    bindable,
    Signal,
    Binding,
    BindingExpression,
    AbstractBinding,
    BindableMixin
)


class Point(NamedTuple):
    x: int
    y: int


class Size(NamedTuple):
    width: int
    height: int

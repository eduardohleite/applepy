from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Union, Tuple

from .app import get_current_app
from .mixins import StackMixin, Modifiable, ChildMixin
from ..base.binding import AbstractBinding, bindable
from ..base.transform_mixins import Width, Height
from ..backend import _MACOS, _IOS

if _MACOS:
    from ..backend.app_kit import NSView, UIView

if _IOS:
    from ..backend.ui_kit import NSView, UIView


class View(ABC,
           Modifiable,
           ChildMixin,
           Width,
           Height):
    @bindable(str)
    def tooltip(self) -> Optional[str]:
        # does iOS have tooltip?
        return self._tooltip

    @tooltip.setter
    def tooltip(self, val: Optional[str]) -> None:
        self._tooltip = val
        self.ns_object.toolTip = val

    def __init__(self, valid_parent_types: Optional[Tuple[type]]=None) -> None:
        self.parent = get_current_app().get()
        self._modifiers: List[Callable] = []

        self._tooltip = None
        self._grab_constraint = None
        self._activated_constraints = None

        if not valid_parent_types:
            from ..base.scene import Scene
            valid_parent_types = (View, StackedView, Scene)

        Modifiable.__init__(self)
        ChildMixin.__init__(self, valid_parent_types)
        Width.__init__(self)
        Height.__init__(self)

        # register itself in parent's stack
        # TODO: is there a better way to not stack a view with a custom body?
        content = self.body()
        if not self.parent.is_stacked(content):
            self.parent.stack(content)

    def body(self):
        return self

    @abstractmethod
    def parse(self):
        return Modifiable.parse(self)

    @abstractmethod
    def get_ns_object(self) -> Union[NSView, UIView]:
        pass

    @property
    def ns_object(self) -> Union[NSView, UIView]:
        return self.get_ns_object()

    def _on_tooltip_changed(self, signal, sender, event):
        self.tooltip = self.bound_tooltip.value

    def set_tooltip(self, tooltip: Union[Optional[str], AbstractBinding]=None):
        def __modifier():
            if isinstance(tooltip, AbstractBinding):
                self.bound_tooltip = tooltip
                self.bound_tooltip.on_changed.connect(self._on_tooltip_changed)
                self.tooltip = tooltip.value
            else:
                self.tooltip = tooltip

        self._modifiers.append(__modifier)

        return self


class StackedView(View, StackMixin):
    def __init__(self, valid_parent_types: Optional[Tuple[type]]=None) -> None:
        View.__init__(self, valid_parent_types)
        StackMixin.__init__(self)

    def parse(self):
        View.parse(self)

        while self._stack:
            el = self.pop_first()
            el.parse()

    def __enter__(self):
        # register itself in the App's stack
        get_current_app().stack(self)
        return self

    def __exit__(self, type, value, traceback):
        # unregister itself in the App's stack
        get_current_app().pop()


class PartialView(View):
    def __init__(self) -> None:
        super().__init__()

    def get_ns_object(self):
        return super().get_ns_object()

    def parse(self):
        return super().parse()

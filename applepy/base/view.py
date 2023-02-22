from abc import ABC, abstractmethod
from typing import Callable, List

from .app import get_current_app
from .mixins import StackMixin, Modifiable
from ..backend.app_kit import NSView


class View(ABC):
    def __init__(self) -> None:
        self.parent = get_current_app().get()
        self._modifiers: List[Callable] = []

        # register itself in parent's stack
        # TODO: is there a better way to not stack a view with a custom body?
        content = self.body()
        if self.parent.is_stacked(content):
            print('double stack')
        else:
            self.parent.stack(content)

    def body(self):
        return self

    @abstractmethod
    def parse(self):
        for modifier in self._modifiers:
            modifier()

    @abstractmethod
    def get_ns_object(self) -> NSView:
        pass

    @property
    def ns_object(self) -> NSView:
        return self.get_ns_object()


class StackedView(View, StackMixin):
    def __init__(self) -> None:
        View.__init__(self)
        StackMixin.__init__(self)

    def parse(self):
        while self._stack:
            el = self.pop()
            #el.body().parse()
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

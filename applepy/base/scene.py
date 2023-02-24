from abc import ABC, abstractmethod
from typing import Optional, Union, Tuple

from .view import View
from .mixins import StackMixin, ChildMixin
from .app import get_current_app


class Scene(ABC, StackMixin, ChildMixin):
    def __init__(self, valid_parent_types: Optional[Tuple[type]]=None) -> None:
        StackMixin.__init__(self)
        ChildMixin.__init__(self, valid_parent_types)

    @abstractmethod
    def body(self):
        return self

    @abstractmethod
    def get_ns_object(self):
        pass

    @abstractmethod
    def parse(self):
        while self._stack:
            el: Union[Scene, View] = self.pop_first()
            el.body().parse()

    @property
    def ns_object(self):
        return self.get_ns_object()

    def __enter__(self):
        # register itself in the App's stack
        get_current_app().stack(self)
        return self

    def __exit__(self, type, value, traceback):
        pass
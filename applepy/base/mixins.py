from typing import Optional, Tuple, List, Callable

from .errors import UnsuportedParentError
from .app import get_current_app, StackMixin


class Modifiable:
    def __init__(self) -> None:
        self._modifiers: List[Callable] = []

    def parse(self):
        for modifier in self._modifiers:
            modifier()


class ChildMixin:
    def __init__(self, valid_parent_types: Optional[Tuple[type]]=None) -> None:
        self.parent = get_current_app().get()
        
        if valid_parent_types:
            if not isinstance(self.parent, valid_parent_types):
                raise UnsuportedParentError(type(self), type(self.parent))

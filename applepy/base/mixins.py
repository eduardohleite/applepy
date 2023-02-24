from typing import Optional, Tuple, List, Callable
from inspect import getmembers

from .errors import UnsuportedParentError
from .app import get_current_app, StackMixin
from .utils import Attachable


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


class AttachableMixin(ChildMixin):
    def parse(self):
        attachable = getmembers(type(self.parent), lambda x: isinstance(x, Attachable) and x.type_ == type(self))
        if any(attachable):
            if len(attachable) > 1:
                raise Exception('More than one attachable found for a single attachment type.')

            name, _ = attachable[0]

            if getattr(self.parent, name):
                raise Exception(f'Attachable {name} is already attached.')

            setattr(self.parent, name, self)

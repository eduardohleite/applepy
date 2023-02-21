from enum import Enum

from ... import StackedView
from ...backend.app_kit import NSStackView, ObjCInstance
from ...base.app import get_current_app


class StackOrientation(Enum):
    Horizontal = 0
    Vertical = 1


class StackView(StackedView):
    def __init__(self, *, orientation: StackOrientation) -> None:
        super().__init__()
        self.orientation = orientation

    def get_ns_object(self) -> NSStackView:
        return self._stack_view

    def parse(self):
        self._stack_view = NSStackView.alloc().init()
        self._stack_view.orientation = self.orientation.value

        if isinstance(self.parent, StackView):
            self.parent.ns_object.addArrangedSubview_(self.ns_object)
        else:
            self.parent.ns_object.contentView = self.ns_object

        super().parse()
    
        return self


class HorizontalStack(StackView):
    def __init__(self) -> None:
        super().__init__(orientation=StackOrientation.Horizontal)


class VerticalStack(StackView):
    def __init__(self) -> None:
        super().__init__(orientation=StackOrientation.Vertical)

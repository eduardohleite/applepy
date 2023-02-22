from enum import Enum

from ... import StackedView
from ...backend.app_kit import NSStackView
from ...base.mixins import Modifiable
from ...base.transform_mixins import (
    BackgroundColor,
    LayoutSpacing,
    LayoutPadding
)


class StackOrientation(Enum):
    Horizontal = 0
    Vertical = 1


class StackView(StackedView,
                Modifiable,
                BackgroundColor,
                LayoutSpacing,
                LayoutPadding):
    def __init__(self, *, orientation: StackOrientation) -> None:
        StackedView.__init__(self)
        Modifiable.__init__(self)
        BackgroundColor.__init__(self)
        LayoutPadding.__init__(self)
        LayoutSpacing.__init__(self)

        self.orientation = orientation

    def get_ns_object(self) -> NSStackView:
        return self._stack_view

    def parse(self):
        self._stack_view = NSStackView.alloc().init()
        self._stack_view.orientation = self.orientation.value

        # alignment
        self._stack_view.alignment = 1 # NSLayoutAttributeLeft

        if isinstance(self.parent, StackView):
            self.parent.ns_object.addArrangedSubview_(self.ns_object)
        else:
            self.parent.ns_object.contentView = self.ns_object

        StackedView.parse(self)
        Modifiable.parse(self)
    
        return self


class HorizontalStack(StackView):
    def __init__(self) -> None:
        super().__init__(orientation=StackOrientation.Horizontal)


class VerticalStack(StackView):
    def __init__(self) -> None:
        super().__init__(orientation=StackOrientation.Vertical)

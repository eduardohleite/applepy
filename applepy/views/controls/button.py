from typing import Callable, Optional

from ... import Color
from ...base.view import View
from ...backend.app_kit import NSButton, NSControl
from ...base.app import get_current_app
from .control import Control


class Button(Control):
    def __init__(self, *, title: str, action:Optional[Callable]=None) -> None:
        super().__init__()
        self.title = title
        self.action = action

    def get_ns_object(self) -> NSButton:
        return self._button

    def parse(self):
        self._button = NSButton.buttonWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        super().parse()

        return self

    def color(self, color: Color):
        def __modifier():
            self._button.bezelColor = color.value

        self._modifiers.append(__modifier)

        return self


class Checkbox(Button):
    def parse(self):
        self._button = NSButton.checkboxWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        Control.parse(self)

        return self

    def is_checked(self, checked: bool):
        def __modifier():
            self._button.state = 1 if checked else 0

        self._modifiers.append(__modifier)

        return self
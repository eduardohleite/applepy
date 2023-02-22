from typing import Callable, Optional

from ... import Color
from ...base.transform_mixins import (
    TitledControl, BezelColor, ControlWithState
)
from ...base.view import View
from ...backend.app_kit import NSButton
from ...base.app import get_current_app
from .control import Control


class Button(Control,
             TitledControl,
             BezelColor):
    def __init__(self, *, title: str, action: Optional[Callable]=None) -> None:
        Control.__init__(self)
        TitledControl.__init__(self, title)
        BezelColor.__init__(self)

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


class Checkbox(Button,
               ControlWithState):

    def __init__(self, *, title: str, action: Optional[Callable] = None) -> None:
        Button.__init__(self, title=title, action=action)
        ControlWithState.__init__(self)

    def parse(self):
        self._button = NSButton.checkboxWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        Control.parse(self)

        return self

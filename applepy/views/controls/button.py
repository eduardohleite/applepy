from typing import Callable, Optional

from ...base.transform_mixins import (
    TitledControl,
    BezelColor,
    ControlWithState,
    KeyBindable
)
from ...backend.app_kit import NSButton
from ...base.app import get_current_app
from ...base.utils import try_call
from .control import Control


class Button(Control,
             TitledControl,
             BezelColor,
             KeyBindable):
    def __init__(self, *, title: str,
                          action: Optional[Callable]=None,
                          key_equivalent: Optional[str]=None) -> None:
        Control.__init__(self)
        TitledControl.__init__(self, title)
        BezelColor.__init__(self)
        KeyBindable.__init__(self, key_equivalent)

        self.action = action

    def get_ns_object(self) -> NSButton:
        return self._button

    def parse(self) -> Control:
        self._button = NSButton.buttonWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        Control.parse(self)
        TitledControl.parse(self)
        BezelColor.parse(self)
        KeyBindable.parse(self)

        return self


class Checkbox(Button,
               ControlWithState):

    def __init__(self, *, title: str, action: Optional[Callable] = None) -> None:
        Button.__init__(self, title=title, action=action)
        ControlWithState.__init__(self)

    def parse(self):
        self._button = NSButton.checkboxWithTitle_target_action_(self.title, None, None)

        def __button_state():
            self.state = self._button.state
            try_call(self.action)

        self._button.setAction_(
            get_current_app().register_action(self._button, __button_state)
        )

        Control.parse(self)
        ControlWithState.parse(self)

        return self

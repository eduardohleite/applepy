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

    """ Control that generates a native MacOS PushButton. """

    def __init__(self, *, title: str,
                          action: Optional[Callable]=None,
                          key_equivalent: Optional[str]=None) -> None:
        """
        Add a new `Button` view, which creates a MacOS standard, text based, Push Button.

        Example:
        >>> Button(title='Push me')

        An action and a key shortcut can also be set in the initializers:

        >>> Button(title='Quit',
                   key_equivalent='q',
                   action=self.quit)

        Args:
            title (str): The button's title.
            action (Optional[Callable], optional): The action to be executed when the button is clicked. Defaults to None.
            key_equivalent (Optional[str], optional): The button's key shortcut. Defaults to None.
        """
        Control.__init__(self)
        TitledControl.__init__(self, title)
        BezelColor.__init__(self)
        KeyBindable.__init__(self, key_equivalent)

        self.action = action

    def get_ns_object(self) -> NSButton:
        """
        The button's NSButton instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSButton: the syack view's NSButton instance.
        """
        return self._button

    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Button: self
        """
        self._button = NSButton.buttonWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        Control.parse(self)
        TitledControl.parse(self, TitledControl)
        BezelColor.parse(self, BezelColor)
        KeyBindable.parse(self, KeyBindable)

        return self


class Checkbox(Button,
               ControlWithState):

    """ Control that generates a native MacOS check box style button. """

    def __init__(self, *, title: str, action: Optional[Callable] = None) -> None:
        """
        Add a new `Checkbox` view, which creates a MacOS native checkbox style button.

        Example:
        >>> Checkbox(title='Push me')

        An action and can also be set in the initializers:

        >>> Checkbox(title='Quit',
                     action=self.quit)

        The `checked` state can be managed through the `state` modifier.

        >>> Checkbox(title='is visible') \
                .set_state(Binding(Window.visible, w))

        Args:
            title (str): The checkbox's title.
            action (Optional[Callable], optional): The action to be executed when the checkbox is clicked. Defaults to None.
        """
        Button.__init__(self, title=title, action=action)
        ControlWithState.__init__(self)

    def parse(self):
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Checkbox: self
        """
        self._button = NSButton.checkboxWithTitle_target_action_(self.title, None, None)

        def __button_state():
            self.state = self._button.state
            try_call(self.action)

        self._button.setAction_(
            get_current_app().register_action(self._button, __button_state)
        )

        Control.parse(self)
        ControlWithState.parse(self, ControlWithState)

        return self

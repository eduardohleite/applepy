from typing import Callable, Optional, Union

from ...base.transform_mixins import (
    TitledControl,
    BezelColor,
    ControlWithState,
    KeyBindable,
    ImageControl
)
from ...backend.app_kit import NSButton
from ...base.binding import AbstractBinding
from ...base.app import get_current_app
from ...base.utils import try_call
from ...base.types import Image, ImagePosition
from .control import Control


class Button(Control,
             TitledControl,
             BezelColor,
             KeyBindable):

    """ Control that generates a native MacOS PushButton. """

    def __init__(self, *, title: Union[str, AbstractBinding],
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
            NSButton: the button's NSButton instance.
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

    def __init__(self, *, title: Union[str, AbstractBinding],
                          action: Optional[Callable] = None) -> None:
        """
        Add a new `Checkbox` view, which creates a MacOS native checkbox style button.

        Example:
        >>> Checkbox(title='Push me')

        An action can also be set in the initializers:
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

    def parse(self) -> Button:
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


class ImageButton(Button,
                  ImageControl):

    """ Control that generates a native MacOS PushButton with an image """

    def __init__(self, *, title: Union[str, AbstractBinding],
                          image: Union[Image, AbstractBinding],
                          image_position: Union[ImagePosition, AbstractBinding]=ImagePosition.image_left,
                          action: Optional[Callable]=None,
                          key_equivalent: Optional[str]=None) -> None:
        """
        Add a new `Button` view, which creates a MacOS native Push Button with an image.
        The following example will show a button with an icon on the left and the text 'Ok' on the right:
        >>> ImageButton(title='Ok', image=Image.from_system('NSMenuOnStateTemplate'))

        The next example will show the image only:
        >>> ImageButton(title='', image=Image.from_system('NSMenuOnStateTemplate'), image_position=ImagePosition=image_only)

        The last example will show the image on the right and the text on the left:
        >>> ImageButton(title='Cool button',
                        image=Image.from_system('NSUserAccounts'),
                        image_position=ImagePosition.image_right)

        Args:
            title (Union[str, AbstractBinding]): The button's title.
            image (Union[Image, AbstractBinding]): The button's image.
            image_position (Union[ImagePosition, AbstractBinding], optional): The position of the button's image. Defaults to ImagePosition.image_left.
            action (Optional[Callable], optional): The action to be executed when the button is clicked. Defaults to None.
            key_equivalent (Optional[str], optional): The button's key shortcut. Defaults to None.
        """    
        Button.__init__(self, title=title, action=action, key_equivalent=key_equivalent)
        ImageControl.__init__(self, image=image, image_position=image_position)

    def parse(self) -> Button:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            ImageButton: self
        """
        Button.parse(self)
        ImageControl.parse(self, ImageControl)

        return self


class RadioButton(Button, ControlWithState):
    """ Control that generates a native MacOS Radio button. """

    def __init__(self, *, title: Union[str, AbstractBinding],
                          action: Optional[Callable] = None,
                          key_equivalent: Optional[str] = None) -> None:
        """
        Add a new `RadioButton` view, which creates a MacOS native Radio Button.

        Example:
        >>> RadioButton(title='Yes')

        An action can also be set in the initializers:
        >>> RatioButton(title='Yes',
                        action=self.say_yes)

        The `checked` state can be managed through the `state` modifier.
        >>> RatioButton(title='is visible') \
                .set_state(Binding(Window.visible, w))

        To make the `RadioButton` part of a group, place them as children of the same
        stack view and give them an action:
        >>> with HorizontalStack():
                with VerticalStack():
                    Label(text='What do you say?')
                    RadioButton(title='Yes', action=self.yes_no)
                    RadioButton(title='No', action=self.yes_no)

                with VerticalStack():
                    Label(text='What do I say?')
                    RadioButton(title='Stop', action=self.stop_gogogo)
                    RadioButton(title='Go, go, go', action=self.stop_gogogo)


        Args:
            title (Union[str, AbstractBinding]): The radio button's title.
            action (Optional[Callable], optional): The action to be executed when the radio button is clicked. Defaults to None.
            key_equivalent (Optional[str], optional): The radio button's key shortcut. Defaults to None.
        """        
        Button.__init__(self, title=title, action=action, key_equivalent=key_equivalent)
        ControlWithState.__init__(self)

    def parse(self) -> Button:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            RadioButton: self
        """
        self._button = NSButton.radioButtonWithTitle_target_action_(self.title, None, None)

        if self.action:
            self._button.setAction_(
                get_current_app().register_action(self._button, self.action)
            )

        Control.parse(self)
        TitledControl.parse(self, TitledControl)
        BezelColor.parse(self, BezelColor)
        KeyBindable.parse(self, KeyBindable)
        ControlWithState.parse(self, ControlWithState)

        return self

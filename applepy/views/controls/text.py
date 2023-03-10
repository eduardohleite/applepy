from typing import Union, Optional, Callable
from uuid import uuid4

from ...backend import _MACOS, _IOS
from .control import Control
from ...base.utils import try_call
from ...base.types import Color
from ...base.transform_mixins import (
    Placeholder,
    TextColor,
    TextControl,
    BackgroundColor
)
from ... import AbstractBinding, bindable

if _MACOS:
    from ...backend.app_kit import (
        NSTextField,
        UILabel,
        UITextField,
        NSObject,
        objc_method
    )

if _IOS:
    from ...backend.ui_kit import (
        NSTextField,
        UILabel,
        UITextField,
        NSObject,
        objc_method
    )


class Label(Control,
            TextColor,
            TextControl):

    """ Control that generates a native MacOS Label. """

    def __init__(self, *, text: Union[str, AbstractBinding]) -> None:
        """
        Add a new `Label` view, which creates a MacOS native label.

        Example:
        >>> Label(text='hello')

        To change the text color, use the `text_color` modifier:
        >>> with HorizontalStack():
                chk = Checkbox(title='Should I stay or should I go?') \
                    .set_state(Binding(MyApp.i_should_go, self))
                Label(text=Binding(Checkbox.state, chk).transform(lambda x: 'go' if x else 'stay')) \
                    .set_text_color(Binding(Checkbox.state, chk)
                        .transform(lambda x: Color.system_green if x else Color.system_red))

        Args:
            text (Union[str, AbstractBinding]):The text to be displayed.
        """        
        Control.__init__(self)
        TextControl.__init__(self, text)
        TextColor.__init__(self)

        self._label = None

    def get_ns_object(self) -> NSTextField:
        """
        The label's NSTextField instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSTextField: the label's NSTextField instance.
        """
        return self._label

    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Label: self
        """
        if _MACOS:
            self._label = NSTextField.labelWithString_(self.text)

        if _IOS:
            self._label = UILabel.alloc().init()
            self._label.text = self.text

        Control.parse(self)
        TextControl.parse(self, TextControl)
        TextColor.parse(self, TextColor)

        return self


class TextField(Control,
                TextControl,
                Placeholder,
                BackgroundColor):
    """ Control that generate a native MacOS single line text edit box. """

    def __init__(self, *, text: Union[str, AbstractBinding],
                          on_text_changed: Optional[Callable]=None) -> None:
        """
        Add a new `TextField` view, which creates a MacOS native single line text field editor.

        Example:
        >>> TextField(text='Hello')

        The `text` initializer supports two-way data binding. Also, you can set a placeholder text
        with the `placeholder` modifier:

        >>> TextField(text=Binding(Person.name, self.view_model.person)) \
                .set_placeholder("Person's name")
    
        Args:
            text (Union[str, AbstractBinding]): The text field's text
            on_text_changed (Optional[Callable], optional): Action to be executed when the text in the text field changes. Defaults to None.
        """        
        Control.__init__(self)
        Placeholder.__init__(self)
        TextControl.__init__(self, text)
        BackgroundColor.__init__(self)

        @objc_method
        def controlTextDidChange_(_self, notification):
            self.text = str(self._text_field.stringValue)
            if self.bound_text:
                self.bound_text.value = self._text

            try_call(on_text_changed)

        @objc_method
        def textField_shouldChangeCharactersIn_replacementString_(_self, field, current, new):
            try_call(on_text_changed)

        props = {}

        if _MACOS:
            props['controlTextDidChange_'] = controlTextDidChange_

        if _IOS:
            props['textField_shouldChangeCharactersIn_replacementString_'] = textField_shouldChangeCharactersIn_replacementString_
    
        _TextFieldDelegate = type(f'_TextFieldDelegate_{uuid4().hex[:8]}', (NSObject,), props)

        self._text_field = None
        self._controller = _TextFieldDelegate.alloc().init()

    def get_ns_object(self) -> NSTextField:
        """
        The text field's NSTextField instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSTextField: the text field's NSTextField instance.
        """
        return self._text_field

    def select_all(self) -> None:
        """
        Ends editing in the text field and, if it's selectable, selects the entire text content.
        If the text field isn't in a window's view hierarchy, this method has no effect.
        """        
        self._text_field.selectText_(None)

    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            TextField: self
        """
        if _MACOS:
            self._text_field = NSTextField.textFieldWithString_(self.text)

        if _IOS:
            self._text_field = UITextField.alloc().init()
            self._text_field.text = self.text

        self._text_field.delegate = self._controller
        
        Control.parse(self),
        TextControl.parse(self, TextControl)
        Placeholder.parse(self, Placeholder)

        return self

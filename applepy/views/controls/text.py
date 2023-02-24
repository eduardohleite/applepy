from typing import Union, Optional, Callable

from .control import Control
from ...backend.app_kit import NSTextField, NSObject, objc_method
from ... import AbstractBinding, bindable


class Label(Control):
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        if self._label:
            self._label.stringValue = value

    def __init__(self, *, text: Union[str, AbstractBinding]) -> None:
        super().__init__()

        self._label = None

        if isinstance(text, AbstractBinding):
            self.bound_text = text
            self.bound_text.on_changed.connect(self._on_text_changed)
            self.text = text.value
        else:
            self.text = text

    def _on_text_changed(self, signal, sender, event):
        self.text = self.bound_text.value

    def get_ns_object(self) -> NSTextField:
        return self._label

    def parse(self):
        self._label = NSTextField.labelWithString_(self.text)
        
        super().parse()

        return self


class TextField(Control):
    @bindable(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        if self._text_field:
            self._text_field.stringValue = value
        

    def __init__(self, *, text: Union[str, AbstractBinding],
                          on_text_changed: Optional[Callable]=None) -> None:
        super().__init__()

        class _Delegate(NSObject):
            @objc_method
            def controlTextDidChange_(_self, notification):
                self.text = str(self._text_field.stringValue)
                if self.bound_text:
                    self.bound_text.value = self._text

                if on_text_changed and callable(on_text_changed):
                    on_text_changed()

        self._text_field = None
        self.text = None
        self.bound_text = None

        self._controller = _Delegate.alloc().init()

        if isinstance(text, AbstractBinding):
            self.bound_text = text
            self.bound_text.on_changed.connect(self._on_text_changed)
            self.text = text.value
        else:
            self.text = text

    def _on_text_changed(self, signal, sender, event):
        self.text = self.bound_text.value

    def get_ns_object(self) -> NSTextField:
        return self._text_field

    def parse(self):
        self._text_field = NSTextField.textFieldWithString_(self.text)
        self._text_field.delegate = self._controller
        
        super().parse()

        return self

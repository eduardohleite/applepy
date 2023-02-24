from typing import Union, Optional

from ...base.types import Color
from ... import AbstractBinding, bindable
from .base import TransformMixin


class TitledControl(TransformMixin):
    @bindable(str)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, val: str) -> None:
        self._title = val
        TitledControl._set(self)

    def __init__(self, default_title: str='') -> None:
        self._title = default_title

    def _on_title_changed(self, signal, sender, event):
        self.title = self.bound_title.value

    def _set(self) -> None:
        self.ns_object.title = self.title

    def set_title(self, title: Union[str, AbstractBinding]):
        def __modifier():
            if isinstance(title, AbstractBinding):
                self.bound_title = title
                self.bound_title.on_changed.connect(self._on_title_changed)
                self.title = title.value
            else:
                self.title = title

        self._modifiers.append(__modifier)

        return self


class ControlWithState(TransformMixin):
    @bindable(int)
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, val: int) -> None:
        self._state = val
        ControlWithState._set(self)

    def __init__(self, default_state: int=0) -> None:
        self._state = default_state

    def _on_state_changed(self, signal, sender, event):
        self.state = self.bound_state.value

    def _set(self) -> None:
        self.ns_object.state = self._state

    def set_state(self, state: Union[int, AbstractBinding]):
        def __modifier():
            if isinstance(state, AbstractBinding):
                self.bound_state = state
                self.bound_state.on_changed.connect(self._on_state_changed)
                self.state = state.value
            else:
                self.state = state

        self._modifiers.append(__modifier)

        return self


class BezelColor(TransformMixin):
    @bindable(Color)
    def bezel_color(self) -> Color:
        return self._bezel_color

    @bezel_color.setter
    def bezel_color(self, val: Color) -> None:
        self._bezel_color = val
        BezelColor._set(self)

    def __init__(self) -> None:
        self._bezel_color = Color.control_color

    def _on_bezel_color_changed(self, signal, sender, event):
        self.bezel_color = self.bound_bezel_color.value

    def _set(self) -> None:
        self.ns_object.bezelColor = self.bezel_color

    def set_bezel_color(self, bezel_color: Union[Color, AbstractBinding]):
        def __modifier():
            if isinstance(bezel_color, AbstractBinding):
                self.bound_bezel_color = bezel_color
                self.bound_bezel_color.on_changed.connect(self._on_bezel_color_changed)
                self.bezel_color = bezel_color.value
            else:
                self.bezel_color = bezel_color

        self._modifiers.append(__modifier)

        return self


class KeyBindable(TransformMixin):
    @bindable(str)
    def key_equivalent(self) -> str:
        return self._key_equivalent

    @key_equivalent.setter
    def key_equivalent(self, val: str) -> None:
        self._key_equivalent = val
        self._set()

    def __init__(self, key_equivalent: Optional[str]=None) -> None:
        self._key_equivalent = key_equivalent

    def _on_key_equivalent_changed(self, signal, sender, event):
        self.key_equivalent = self.bound_key_equivalent.value

    def _set(self) -> None:
        self.ns_object.keyEquivalent = self.key_equivalent

    def set_key_equivalent(self, key_equivalent: Union[str, AbstractBinding]):
        def __modifier():
            if isinstance(key_equivalent, AbstractBinding):
                self.bound_key_equivalent = key_equivalent
                self.bound_key_equivalent.on_changed.connect(self._on_key_equivalent_changed)
                self.key_equivalent = key_equivalent.value
            else:
                self.key_equivalent = key_equivalent

        self._modifiers.append(__modifier)

        return self

from typing import Union

from ...base.types import Color
from ... import AbstractBinding


class TitledControl:
    @property
    def title(self) -> float:
        return self._title

    @title.setter
    def title(self, val: float) -> None:
        self._title = val
        self.ns_object.title = val

    def __init__(self, default_title: str='') -> None:
        self._title = default_title

    def _on_title_changed(self, signal, sender, event):
        self.title = self.bound_title.value

    def set_title(self, title: Union[float, AbstractBinding]):
        def __modifier():
            if isinstance(title, AbstractBinding):
                self.bound_title = title
                self.bound_title.on_changed.connect(self._on_title_changed)
                self.title = title.value
            else:
                self.title = title

        self._modifiers.append(__modifier)

        return self


class ControlWithState:
    # TODO: how to make it two-way bound?
    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, val: int) -> None:
        self._state = val
        self.ns_object.state = val

    def __init__(self, default_state: int=0) -> None:
        self._state = default_state

    def _on_state_changed(self, signal, sender, event):
        self.state = self.bound_state.value

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


class BezelColor:
    @property
    def bezel_color(self) -> Color:
        return self._bezel_color

    @bezel_color.setter
    def bezel_color(self, val: Color) -> None:
        self._bezel_color = val
        self.ns_object.bezelColor = val.value

    def __init__(self) -> None:
        self._bezel_color = Color.control_color

    def _on_bezel_color_changed(self, signal, sender, event):
        self.bezel_color = self.bound_bezel_color.value

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

from typing import Union

from ... import AbstractBinding, Color


class BackgroundColor:
    @property
    def background_color(self) -> Color:
        return self._background_color

    @background_color.setter
    def background_color(self, val: Color) -> None:
        self._background_color = val
        self.ns_object.backgroundColor = val.value

    def __init__(self) -> None:
        self._background_color = Color.black

    def _on_background_color_changed(self, signal, sender, event):
        self._background_color = self.bound_background_color.value

    def set_background_color(self, background_color: Union[Color, AbstractBinding]):
        def __modifier():
            if isinstance(background_color, AbstractBinding):
                self.bound_background_color = background_color
                self.bound_background_color.on_changed.connect(self._on_background_color_changed)
                self.background_color = background_color.value
            else:
                self.background_color = background_color

        self._modifiers.append(__modifier)

        return self


class AlphaValue:
    @property
    def alpha_value(self) -> float:
        return self._alpha_value

    @alpha_value.setter
    def alpha_value(self, val: float) -> None:
        self._alpha_value = val
        self.ns_object.alphaValue = val

    def __init__(self) -> None:
        self._alpha_value = 1.

    def _on_alpha_value_color_changed(self, signal, sender, event):
        self._alpha_value = self.bound_alpha_value.value

    def set_alpha_value(self, alpha_value: Union[float, AbstractBinding]):
        def __modifier():
            if isinstance(alpha_value, AbstractBinding):
                self.bound_alpha_value = alpha_value
                self.bound_alpha_value.on_changed.connect(self._on_alpha_value_changed)
                self.alpha_value = alpha_value.value
            else:
                self.alpha_value = alpha_value

        self._modifiers.append(__modifier)

        return self


class HasShadow:
    @property
    def has_shadow(self) -> bool:
        return self._has_shadow

    @has_shadow.setter
    def has_shadow(self, val: bool) -> None:
        self._has_shadow = val
        self.ns_object.hasShadow = val

    def __init__(self) -> None:
        self._has_shadow = 1.

    def _on_has_shadow_color_changed(self, signal, sender, event):
        self._has_shadow = self.bound_has_shadow.value

    def set_has_shadow(self, has_shadow: Union[bool, AbstractBinding]):
        def __modifier():
            if isinstance(has_shadow, AbstractBinding):
                self.bound_has_shadow = has_shadow
                self.bound_has_shadow.on_changed.connect(self._on_has_shadow_changed)
                self.has_shadow = has_shadow.value
            else:
                self.has_shadow = has_shadow

        self._modifiers.append(__modifier)

        return self

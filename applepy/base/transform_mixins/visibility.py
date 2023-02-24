from typing import Union

from ... import AbstractBinding


class Enable:
    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, val) -> None:
        self._enabled = val
        self.ns_object.enabled = val

    def __init__(self) -> None:
        self._enabled = True

    def _on_enabled_changed(self, signal, sender, event):
        self.enabled = self.bound_enabled.value

    def is_enabled(self, enabled: Union[bool, AbstractBinding]):
        def __modifier():
            if isinstance(enabled, AbstractBinding):
                self.bound_enabled = enabled
                self.bound_enabled.on_changed.connect(self._on_enabled_changed)
                self.enabled = enabled.value
            else:
                self.enabled = enabled

        self._modifiers.append(__modifier)

        return self


class Visible:
    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, val) -> None:
        self._visible = val
        self.ns_object.visible = val

    def __init__(self) -> None:
        self._visible = True

    def _on_visible_changed(self, signal, sender, event):
        self.visible = self.bound_visible.value

    def is_visible(self, visible: Union[bool, AbstractBinding]):
        def __modifier():
            if isinstance(visible, AbstractBinding):
                self.bound_visible = visible
                self.bound_visible.on_changed.connect(self._on_visible_changed)
                self.visible = visible.value
            else:
                self.visible = visible

        self._modifiers.append(__modifier)

        return self

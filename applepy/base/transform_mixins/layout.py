from typing import Union, Optional
from rubicon.objc.types import NSEdgeInsets

from ... import AbstractBinding, Padding


class LayoutSpacing:
    @property
    def spacing(self) -> float:
        return self._spacing

    @spacing.setter
    def spacing(self, val: float) -> None:
        self._spacing = val
        self.ns_object.spacing = val

    def __init__(self, default_spacing: float=10.) -> None:
        self._spacing = default_spacing

    def _on_spacing_changed(self, signal, sender, event):
        self._spacing = self.bound_spacing.value

    def set_spacing(self, spacing: Union[float, AbstractBinding]):
        def __modifier():
            if isinstance(spacing, AbstractBinding):
                self.bound_spacing = spacing
                self.bound_spacing.on_changed.connect(self._on_spacing_changed)
                self.spacing = spacing.value
            else:
                self.spacing = spacing

        self._modifiers.append(__modifier)

        return self


class LayoutPadding:
    @property
    def padding(self) -> Padding:
        return self._padding

    @padding.setter
    def padding(self, val: Padding) -> None:
        self._padding = val
        self.ns_object.edgeInsets = NSEdgeInsets(val.bottom,
                                                 val.left,
                                                 val.right,
                                                 val.top)

    def __init__(self, default_padding: Padding=Padding(0., 0., 0., 0.)) -> None:
        self._padding = default_padding

    def _on_padding_changed(self, signal, sender, event):
        self._padding = self.bound_padding.value

    def set_padding(self, padding: Optional[Union[Padding, AbstractBinding]]=Padding(10., 10., 10., 10.)):
        def __modifier():
            if isinstance(padding, AbstractBinding):
                self.bound_padding = padding
                self.bound_padding.on_changed.connect(self._on_padding_changed)
                self.padding = padding.value
            else:
                self.padding = padding

        self._modifiers.append(__modifier)

        return self

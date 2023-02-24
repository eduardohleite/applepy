from typing import Union, Optional
from rubicon.objc.types import NSEdgeInsets

from ... import AbstractBinding, Padding, Alignment
from ..binding import bindable
from .base import TransformMixin


class LayoutSpacing(TransformMixin):
    @bindable(float)
    def spacing(self) -> float:
        return self._spacing

    @spacing.setter
    def spacing(self, val: float) -> None:
        self._spacing = val
        LayoutSpacing._set(self)

    def __init__(self, default_spacing: float=10.) -> None:
        self._spacing = default_spacing

    def _on_spacing_changed(self, signal, sender, event):
        self._spacing = self.bound_spacing.value

    def _set(self) -> None:
        self.ns_object.spacing = self.spacing

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


class LayoutPadding(TransformMixin):
    @bindable(Padding)
    def padding(self) -> Padding:
        return self._padding

    @padding.setter
    def padding(self, val: Padding) -> None:
        self._padding = val
        LayoutPadding._set(self)

    def __init__(self, default_padding: Padding=Padding(0., 0., 0., 0.)) -> None:
        self._padding = default_padding

    def _on_padding_changed(self, signal, sender, event):
        self._padding = self.bound_padding.value

    def _set(self) -> None:
        self.ns_object.edgeInsets = NSEdgeInsets(self.padding.bottom,
                                                 self.padding.left,
                                                 self.padding.right,
                                                 self.padding.top)

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


class LayoutAlignment(TransformMixin):
    @bindable(Alignment)
    def alignment(self) -> Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, val: Alignment) -> None:
        self._alignment = val
        LayoutAlignment._set(self)

    def __init__(self, default_alignment: Alignment=Alignment.left) -> None:
        self._alignment = default_alignment

    def _on_alignment_changed(self, signal, sender, event):
        self._alignment = self.bound_alignment.value

    def _set(self) -> None:
        self.ns_object.alignment = self.alignment

    def set_alignment(self, alignment: Union[Alignment, AbstractBinding]):
        def __modifier():
            if isinstance(alignment, AbstractBinding):
                self.bound_alignment = alignment
                self.bound_alignment.on_changed.connect(self._on_alignment_changed)
                self.alignment = alignment.value
            else:
                self.alignment = alignment

        self._modifiers.append(__modifier)

        return self

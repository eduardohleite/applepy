from typing import Union

from ..binding import AbstractBinding, bindable


class Width:
    @bindable(int)
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, val: int) -> None:
        self._width = val
        self._set_width_constraint(val)

    def __init__(self) -> None:
        self._width = -1
        self._width_constraint = None

    def _set_width_constraint(self, val: int) -> None:
        if val > 0:
            if self._width_constraint:
                self._width_constraint.active = False

            self.ns_object.translatesAutoresizingMaskIntoConstraints = False
            self._width_constraint = self.ns_object.widthAnchor.constraintEqualToConstant(val)
            self._width_constraint.active = True
        else:
            self._width_constraint.active = False

    def _on_width_changed(self, signal, sender, event):
        self.width = self.bound_width.value

    def fixed_width(self, width: Union[int, AbstractBinding]):
        def __modifier():
            if isinstance(width, AbstractBinding):
                self.bound_width = width
                self.bound_width.on_changed.connect(self._on_width_changed)
                self.width = width.value
            else:
                self.width = width

        self._modifiers.append(__modifier)

        return self


class Height:
    @bindable(int)
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, val: int) -> None:
        self._height = val
        self._set_height_constraint(val)

    def __init__(self) -> None:
        self._height = -1
        self._height_constraint = None

    def _set_height_constraint(self, val: int) -> None:
        if val > 0:
            if self._height_constraint:
                self._height_constraint.active = False

            self.ns_object.translatesAutoresizingMaskIntoConstraints = False
            self._height_constraint = self.ns_object.heightAnchor.constraintEqualToConstant(val)
            self._height_constraint.active = True
        else:
            self._height_constraint.active = False

    def _on_height_changed(self, signal, sender, event):
        self.height = self.bound_height.value

    def fixed_height(self, height: Union[int, AbstractBinding]):
        def __modifier():
            if isinstance(height, AbstractBinding):
                self.bound_height = height
                self.bound_height.on_changed.connect(self._on_height_changed)
                self.height = height.value
            else:
                self.height = height

        self._modifiers.append(__modifier)

        return self
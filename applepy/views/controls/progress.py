from typing import Union

from ... import ProgressStyle
from ...base.binding import AbstractBinding, bindable
from ...backend.app_kit import NSProgressIndicator
from .control import Control


class ProgressIndicator(Control):
    """ Control that generates a native MacOS Progress Indicator. """

    @bindable(bool)
    def animating(self) -> bool:
        """
        Whether the ProgressIndicator is animating.

        Returns:
            bool: `True` if the ProgressIndicator is animating, `False` otherwise.
        """
        return self._animating

    @animating.setter
    def animating(self, val: bool) -> None:
        if self.ns_object:
            if val and not self._animating:
                self.ns_object.startAnimation_(None)
            elif not val and self._animating:
                self.ns_object.stopAnimation_(None)

        self._animating = val

    @bindable(float)
    def value(self) -> float:
        """
        The ProgressIndicator current value.

        Returns:
            float: the ProgressIndicator current value.
        """        
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        self._value = val
        if self.ns_object:
            self.ns_object.doubleValue = val

    def __init__(self,
                 *,
                 value: Union[float, AbstractBinding],
                 indeterminate: bool,
                 style: ProgressStyle,
                 display_when_stopped: bool=True,
                 min_value: float=0.,
                 max_value: float=100.) -> None:
        """
        Add a new `ProgressIndicator` view, which creates a MacOS native Progress Indicator control.
        For common use cases, use the shortcut classes `ProgressBar` and `Spinner`.

        Args:
            value (Union[float, AbstractBinding]): The current value of the ProgressIndicator.
            indeterminate (bool): Whether the ProgressIndicator should run indeterminately.
            style (ProgressStyle): The style of the ProgressIndicator
            display_when_stopped (bool, optional): Whether the ProgressIndicator should be visible when not running. Defaults to True.
            min_value (float, optional): The ProgressIndicator's minimum value. Defaults to 0.
            max_value (float, optional): The ProgressIndicator's maximum value. Defaults to 100.
        """
        super().__init__()
        self._progress_indicator = None

        self._animating = False
        self.min_value = min_value
        self.max_value = max_value
        self.indeterminate = indeterminate
        self.style = style
        self.display_when_stopped = display_when_stopped

        if isinstance(value, AbstractBinding):
            self.bound_value = value
            self.bound_value.on_changed.connect(self._on_value_changed)
            self._value = value.value
        else:
            self._value = value

    def _on_value_changed(self, signal, sender, event):
        self.value = self.bound_value.value

    def _on_animating_changed(self, signal, sender, event):
        self.animating = self.bound_animating.value

    def get_ns_object(self) -> NSProgressIndicator:
        """
        The progress indicator's NSProgressIndicator instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSProgressIndicator: the progress indicator's NSProgressIndicator instance.
        """
        return self._progress_indicator

    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            ProgressIndicator: self
        """
        self._progress_indicator = NSProgressIndicator.alloc().init()
        self._progress_indicator.minValue = self.min_value
        self._progress_indicator.maxValue = self.max_value
        self._progress_indicator.indeterminate = self.indeterminate
        self._progress_indicator.style = self.style.value
        self._progress_indicator.sizeToFit = True
        self._progress_indicator.displayedWhenStopped = self.display_when_stopped

        return super().parse()

    def is_running(self, running: Union[bool, AbstractBinding]) -> Control:
        """
        Modifier that can set or bind a flag indicating that the ProgressIndicator should be running.

        Args:
            running (Union[bool, AbstractBinding]): Flag or bing indicating whether the ProgressIndicator should be running.

        Returns:
            Control: self
        """
        def __modifier():
            if isinstance(running, AbstractBinding):
                self.bound_animating = running
                self.bound_animating.on_changed.connect(self._on_animating_changed)
                self.animating = running.value
            else:
                self.animating = running

        self._modifiers.append(__modifier)

        return self


class ProgressBar(ProgressIndicator):
    """ Control that generates a native MacOS ProgressIndicator with a ProgressBar style. """

    def __init__(self,
                 *,
                 value: Union[float, AbstractBinding],
                 indeterminate: bool=False,
                 display_when_stopped: bool = True,
                 min_value: float = 0.,
                 max_value: float = 100.) -> None:
        """
        Add a new `ProgressBar` view, which creates a MacOS native Progress Indicator control
        with a Progress Bar style.

        Example:
        >>> ProgressBar(value=Binding(ViewModel.value, self.view_model))

        Args:
            value (Union[float, AbstractBinding]): The current value of the ProgressIndicator.
            indeterminate (bool, optional): Whether the ProgressIndicator should run indeterminately. Defaults to False.
            display_when_stopped (bool, optional): Whether the ProgressIndicator should be visible when not running. Defaults to True.
            min_value (float, optional): The ProgressIndicator's minimum value. Defaults to 0.
            max_value (float, optional): The ProgressIndicator's maximum value. Defaults to 100.
        """
        super().__init__(value=value,
                         indeterminate=indeterminate,
                         style=ProgressStyle.bar,
                         display_when_stopped=display_when_stopped,
                         min_value=min_value,
                         max_value=max_value)

class Spinner(ProgressIndicator):
    """ Control that generates a native MacOS ProgressIndicator with a Spinner style. """

    def __init__(self,
                 *,
                 value: Union[float, AbstractBinding],
                 indeterminate: bool=True,
                 display_when_stopped: bool = False,
                 min_value: float = 0.,
                 max_value: float = 100.) -> None:
        """
        Add a new `Spinner` view, which creates a MacOS native Progress Indicator control
        with a Spinner style.

        Example:
        >>> Spinner(value=0) \
                .is_running(Binding(ViewModel.is_loading, self.vm))

        Args:
            value (Union[float, AbstractBinding]): The current value of the ProgressIndicator.
            indeterminate (bool, optional): Whether the ProgressIndicator should run indeterminately. Defaults to True.
            display_when_stopped (bool, optional): Whether the ProgressIndicator should be visible when not running. Defaults to False.
            min_value (float, optional): The ProgressIndicator's minimum value. Defaults to 0.
            max_value (float, optional): The ProgressIndicator's maximum value. Defaults to 100.
        """
        super().__init__(value=value,
                         indeterminate=indeterminate,
                         style=ProgressStyle.spinner,
                         display_when_stopped=display_when_stopped,
                         min_value=min_value,
                         max_value=max_value)
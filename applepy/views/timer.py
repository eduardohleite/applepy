from typing import Union, Optional, Callable
from threading import Timer as TimerThread

from .. import bindable, AbstractBinding
from ..base.utils import try_call


class Timer:
    """
    A non-visual component that creates a Timer.
    """

    @bindable(bool)
    def repeat(self) -> bool:
        """
        Whether timer should repeat once action is run.

        Returns:
            bool: `True` if timer should repeat indefinitely, `False` otherwise.
        """        
        return self._repeat

    @repeat.setter
    def repeat(self, val: bool) -> None:
        self._repeat = val

    @bindable(bool)
    def enabled(self) -> bool:
        """
        Whether timer should be running or stopped.

        Returns:
            bool: `True` if timer is running, `False` otherwise.
        """        
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool) -> None:
        # start / stop self._current_timer
        if self._enabled and not val:
            self._current_timer.cancel()
            self._current_timer = None
        elif not self._enabled and val:
            if not self._current_timer:
                self._set_timer()
            self._current_timer.start()

        self._enabled = val

    @bindable(float)
    def interval(self) -> float:
        """
        The interval for the timer to timeout in seconds.

        Returns:
            float: The interval for the timer to timeout in seconds.
        """        
        return self._interval

    @interval.setter
    def interval(self, val: float) -> None:
        self._interval = val

    def __init__(self, *, interval: Union[float, AbstractBinding],
                          repeat: Union[bool, AbstractBinding]=False,
                          enabled: Union[bool, AbstractBinding]=False,
                          action: Optional[Callable]=None) -> None:
        """
        Create a `Timer` non-visual component.
        Example:
        >>>Timer(interval=5., repeat=True, action=self.timer_timeout)

        Args:
            interval (Union[float, AbstractBinding]): The Timer's interfal.
            repeat (Union[bool, AbstractBinding], optional): Whether or not the Timer should repeat after timeout. Defaults to False.
            enabled (Union[bool, AbstractBinding], optional): Whether or not the Timer should be running. Defaults to False.
            action (Optional[Callable], optional): The action to be run when the Timer times out. Defaults to None.
        """        
        if isinstance(interval, AbstractBinding):
            self.bound_interval = interval
            self.bound_interval.on_changed.connect(self._on_interval_changed)
            self._interval = interval.value
        else:
            self._interval = interval

        if isinstance(repeat, AbstractBinding):
            self.bound_repeat = repeat
            self.bound_repeat.on_changed.connect(self._on_repeat_changed)
            self._repeat = repeat.value
        else:
            self._repeat = repeat

        if isinstance(enabled, AbstractBinding):
            self.bound_enabled = enabled
            self.bound_enabled.on_changed.connect(self._on_enabled_changed)
            self._enabled = enabled.value
        else:
            self._enabled = enabled

        self._action = action
        self._set_timer()

    def _set_timer(self) -> None:
        def __timeout():
            try_call(self._action)
            if self.repeat and self.enabled:
                self._set_timer()
            else:
                self._current_timer = None

        self._current_timer = TimerThread(self.interval, __timeout)
        if self.enabled:
            self._current_timer.start()

    def _on_repeat_changed(self) -> None:
        self.repeat = self.bound_repeat.value

    def _on_enabled_changed(self) -> None:
        self.enabled = self.bound_enabled.value

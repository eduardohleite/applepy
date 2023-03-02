from typing import Union, Optional, Callable
from uuid import uuid4
from ctypes import POINTER, c_double

from ... import View, Date
from ...backend.app_kit import (
    objc_id,
    objc_method,
    ObjCInstance,
    NSObject,
    NSDatePicker,
    NSDatePickerElementFlags
)
from ...base.binding import AbstractBinding, bindable
from ...base.utils import try_call
from .control import Control


class DatePicker(Control):
    """ Control that generates a native MacOS DatePicker. """

    @bindable(Date)
    def date(self) -> Date:
        """
        Date selected by the DatePicker.

        Returns:
            Date: date selected by the DatePicker.
        """        
        return self._date

    @date.setter
    def date(self, val: Date) -> None:
        self._date = val
        if self._date_picker:
            self._date_picker.dateValue = self._date.value

    def __init__(self, *, date: Union[Date, AbstractBinding],
                          show_date: bool=True,
                          show_time: bool=False,
                          show_calendar_overlay: bool=False,
                          min_date: Date=Date.min(),
                          max_date: Date=Date.max(),
                          on_date_changed: Optional[Callable]=None) -> None:
        """
        Add a new `DatePicker` view, which creates a MacOS native date picker control.

        Example:
        >>> DatePicker(date=Date.now())

        Args:
            date (Union[Date, AbstractBinding]): The date selected by the DatePicker.
            show_date (bool, optional): Whether the DatePicker displays the date. Defaults to True.
            show_time (bool, optional): Whether the DatePicker displays the time. Defaults to False.
            show_calendar_overlay (bool, optional): Whether the DatePicker displays the calendar overlay. Defaults to False.
            min_date (Date, optional): Minimum date selectable by the DatePicker. Defaults to Date.min().
            max_date (Date, optional): Maximum date selectable by the DatePicker. Defaults to Date.max().
            on_date_changed (Optional[Callable], optional): Action that is called when the date of the DatePicker has changed. Defaults to None.
        """        
        super().__init__()

        self.min_date = min_date
        self.max_date = max_date

        self._show_date = show_date
        self._show_time = show_time
        self._show_calendar_overlay = show_calendar_overlay

        if isinstance(date, AbstractBinding):
            self.bound_date = date
            self.bound_date.on_changed.connect(self._on_date_changed)
            self._date = date.value
        else:
            self.bound_date = None
            self._date = date

        @objc_method
        def datePickerCell_validateProposedDateValue_timeInterval_(_self, 
                                                                   datePickerCell,
                                                                   proposedDateValue: POINTER(objc_id),
                                                                   proposedTimeInterval: POINTER(c_double)):
            new_date_value = ObjCInstance(proposedDateValue.contents)
            self.date = Date.from_value(new_date_value)
            if self.bound_date:
                self.bound_date.value = Date.from_value(new_date_value)

            try_call(on_date_changed)

        _DatePickerDelegate = type(f'_DatePickerDelegate{uuid4().hex[:8]}', (NSObject,), {
            'datePickerCell_validateProposedDateValue_timeInterval_': datePickerCell_validateProposedDateValue_timeInterval_
        })

        self._date_picker = None
        self._controller = _DatePickerDelegate.alloc().init()

    def _on_date_changed(self, signal, sender, event):
        self.date = self.bound_date.value

    def get_ns_object(self) -> NSDatePicker:
        """
        The date picker's NSDatePicker instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSDatePicker: the date picker's NSDatePicker instance.
        """
        return self._date_picker

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            DatePicker: self
        """
        self._date_picker = NSDatePicker.alloc().init()
        self._date_picker.minDate = self.min_date.value
        self._date_picker.maxDate = self.max_date.value
        self._date_picker.dateValue = self.date.value
        self._date_picker.presentsCalendarOverlay = self._show_calendar_overlay

        mask = 0

        if self._show_date:
            mask |= NSDatePickerElementFlags.NSDatePickerElementFlagYearMonthDay.value

        if self._show_time:
            mask |= NSDatePickerElementFlags.NSDatePickerElementFlagHourMinuteSecond.value

        self._date_picker.datePickerElements = mask

        self._date_picker.delegate = self._controller

        Control.parse(self)

        return self

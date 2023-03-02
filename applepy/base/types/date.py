from datetime import datetime
from typing import Optional

from ...base.binding import BindableMixin
from ...backend.app_kit import NSDate


class Date(BindableMixin):
    def __init__(self, *, datetime_value: Optional[datetime]=None, value: Optional[NSDate] = None) -> None:
        if not datetime_value and not value:
            raise Exception('choose one')
        if datetime_value and value:
            raise Exception('choose only one')

        if datetime_value:
            self.datetime = datetime_value
        else:
            self.datetime = datetime.fromtimestamp(value.timeIntervalSince1970())

        self.value = NSDate.dateWithTimeIntervalSince1970_(self.datetime.timestamp())

    @classmethod
    def from_value(cls, value: NSDate):
        return cls(value=value)

    @classmethod
    def from_datetime(cls, value: datetime):
        return cls(datetime_value=NSDate.dateWithTimeIntervalSince1970_(value.timestamp()))

    @classmethod
    def now(cls):
        return cls(value=NSDate.date())

    @classmethod
    def min(cls):
        return cls(datetime_value=datetime.fromtimestamp(0))

    @classmethod
    def max(cls):
        return cls(value=NSDate.distantFuture())

    def __repr__(self) -> str:
        return str(self.value.description)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return False

        return  self.datetime == other.datetime

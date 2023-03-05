from datetime import datetime
from typing import Optional

from ...base.binding import BindableMixin
from ...backend import _MACOS, _IOS

if _MACOS:
    from ...backend.app_kit import NSDate, ObjCInstance

if _IOS:
    from ...backend.ui_kit import NSDate, ObjCInstance


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
        if isinstance(other, Date):
            return self.datetime == other.datetime
        elif isinstance(other, datetime):
            return self.datetime == other
        elif isinstance(other, ObjCInstance):
            return self.datetime == Date(other).datetime
        else:
            return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.datetime != other.datetime
        elif isinstance(other, datetime):
            return self.datetime != other
        elif isinstance(other, ObjCInstance):
            return self.datetime != Date(other).datetime
        else:
            return True

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.datetime > other.datetime
        elif isinstance(other, datetime):
            return self.datetime > other
        elif isinstance(other, ObjCInstance):
            return self.datetime > Date(other).datetime
        else:
            return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.datetime >= other.datetime
        elif isinstance(other, datetime):
            return self.datetime >= other
        elif isinstance(other, ObjCInstance):
            return self.datetime >= Date(other).datetime
        else:
            return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.datetime < other.datetime
        elif isinstance(other, datetime):
            return self.datetime < other
        elif isinstance(other, ObjCInstance):
            return self.datetime < Date(other).datetime
        else:
            return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, Date):
            return self.datetime <= other.datetime
        elif isinstance(other, datetime):
            return self.datetime <= other
        elif isinstance(other, ObjCInstance):
            return self.datetime <= Date(other).datetime
        else:
            return False

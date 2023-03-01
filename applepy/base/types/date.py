from datetime import datetime

from ...base.binding import BindableMixin
from ...backend.app_kit import NSDate


class Date(BindableMixin):
    def __init__(self, value: NSDate) -> None:
        self.value = value

    @classmethod
    def from_datetime(cls, value: datetime):
        return cls(NSDate.dateWithTimeIntervalSince1970_(value.timestamp()))

    @classmethod
    def now(cls):
        return cls(NSDate.date())

    @classmethod
    def min(cls):
        return cls(NSDate.distantPast())

    @classmethod
    def max(cls):
        return cls(NSDate.distantFuture())

    def __repr__(self) -> str:
        return str(self.value.description)

    def to_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.value.timeIntervalSince1970())


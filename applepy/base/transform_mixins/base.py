from abc import ABC, abstractmethod


class TransformMixin(ABC):
    @abstractmethod
    def _set(self) -> None:
        pass

    def parse(self, As_: type):
        As_._set(self)
        return self

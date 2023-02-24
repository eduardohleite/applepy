from abc import ABC, abstractmethod


class TransformMixin(ABC):
    @abstractmethod
    def _set(self) -> None:
        pass

    def parse(self):
        self._set()
        return self

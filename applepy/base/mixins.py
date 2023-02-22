from typing import List, Callable



class StackMixin:
    def __init__(self) -> None:
        self._stack: list = []

    def stack(self, child) -> None:
        self._stack.append(child)

    def pop(self):
        return self._stack.pop()

    def get(self):
        return self._stack[-1]

    def is_stacked(self, ptr):
        return ptr in self._stack


class Modifiable:
    def __init__(self) -> None:
        self._modifiers: List[Callable] = []

    def parse(self):
        for modifier in self._modifiers:
            modifier()

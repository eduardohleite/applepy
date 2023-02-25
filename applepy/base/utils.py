from typing import Optional, Callable, Any


def try_call(fn: Optional[Callable], *args, **kwargs) -> Any:
    if fn and callable(fn):
        return fn(*args, **kwargs)


class Attachable(property):
    def __init__(self, target, *args, **kwargs) -> None:
        from ..base.view import View

        self._target = target

        type_ = kwargs.get('type_')
        if not args and (not type_ or not isinstance(type_, type)
                         or not (issubclass(type_, View))):
            raise Exception('Invalid attachable type')

        if type_:
            self.type_ = type_
            del kwargs['type_']

        super().__init__(target, *args, **kwargs)

    def setter(self, __fset: Callable[[Any, Any], None]) -> property:
        res = super().setter(__fset)
        if self.type_:
            res.type_ = self.type_

        return res


def attachable(type_: type):
    def decorator(target, *args, **kwargs):
        kwargs['type_'] = type_
        return Attachable(target, *args, **kwargs)

    return decorator

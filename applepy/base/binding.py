from typing import Any, Callable, Tuple
from uuid import uuid4
from pydispatch import dispatcher
from abc import ABC, abstractmethod


class Signal:
    def __init__(self) -> None:
        self._id = uuid4().hex

    def emit(self, event=None) -> None:
        dispatcher.send(self._id, dispatcher.Anonymous, event=event)

    def connect(self, callback) -> None:
        dispatcher.connect(callback, sender=dispatcher.Anonymous, signal=self._id, weak=False)


class BindableMixin:
    bindable = None


class wrapped_int(int, BindableMixin):
    pass


class wrapped_float(float, BindableMixin):
    pass


class wrapped_str(str, BindableMixin):
    pass


class wrapped_bool(int, BindableMixin):
    pass


class Bindable(property):
    def __init__(self, target, *args, **kwargs) -> None:
        self._target = target

        type_ = kwargs.get('type_')
        if not args and (not type_ or not isinstance(type_, type)
                         or not (issubclass(type_, BindableMixin)
                             or type_ in [int, float, str, bool])):
            raise Exception('Invalid bindable type')

        if type_:
            self.type_ = type_
            del kwargs['type_']

        self.on_changed = Signal()
        super().__init__(target, *args, **kwargs)

    def __get__(self, *args, **kwargs) -> Any:
        res = super().__get__(*args, **kwargs)

        if isinstance(res, Bindable):
            return res

        if self.type_ == int:
            res = wrapped_int(res)
        elif self.type_ == float:
            res = wrapped_float(res)
        elif self.type_ == str:
            res = wrapped_str(res)
        elif self.type_ == bool:
            res = wrapped_bool(res)

        res.bindable = self

        return res

    def __set__(self, target, new_val, *args, **kwargs) -> None:
        super().__set__(target, new_val, *args, **kwargs)
        self.on_changed.emit(new_val)

    def setter(self, __fset: Callable[[Any, Any], None]) -> property:
        res = super().setter(__fset)
        res.type_ = self.type_
        return res


def bindable(type_: type):
    def decorator(target, *args, **kwargs):
        kwargs['type_'] = type_
        return Bindable(target, *args, **kwargs)

    return decorator


class AbstractBinding(ABC):
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def on_changed(self):
        pass


class Binding(AbstractBinding):
    def __init__(self, bindable: Bindable,
                       instance: Any) -> None:
        self.bindable = bindable
        self.instance = instance

        self.transforms = []

    def transform(self, transform: Callable):
        self.transforms.append(transform)
        return self

    @property
    def on_changed(self):
        return self.bindable.on_changed

    @property
    def value(self):
        new_value = self.bindable.fget(self.instance)

        for transform in self.transforms:
            if not callable(transform):
                raise Exception('bla')

            new_value = transform(new_value)

        return new_value

    @value.setter
    def value(self, new_val):
        cur_val = self.bindable.fget(self.instance)
        w_type = self.bindable.type_
        try:
            new_val = w_type(new_val)
        except ValueError:
            new_val = cur_val
        self.bindable.__set__(self.instance, new_val)


class BindingExpression(AbstractBinding):
    def __init__(self, expression: Callable, *args: Tuple[Bindable, Any]) -> None:
        if len(args) == 0:
            raise Exception('At least one bindable and one instance must be provided.')

        self.bindables = []
        self._on_changed = Signal()

        if not callable(expression):
            raise Exception('Must provide a callable expression.')

        self.expression = expression

        for arg in args:
            if type(arg) != tuple:
                raise Exception('Invalid argument. Must a tuple of bindable and instance.')

            bindable, _ = arg

            if type(bindable) != Bindable:
                raise Exception('Invalid argument. Must a tuple of bindable and instance.')

            bindable.on_changed.connect(self._on_property_in_expression_changed)

            self.bindables.append(arg)

    def _on_property_in_expression_changed(self, signal, sender, event):
        self.on_changed.emit()

    @property
    def value(self):
        arguments = [b.fget(i) for b, i in self.bindables]
        return self.expression(*arguments)

    @property
    def on_changed(self):
        return self._on_changed

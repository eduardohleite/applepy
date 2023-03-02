from typing import Any, Callable, Tuple
from uuid import uuid4
from pydispatch import dispatcher
from abc import ABC, abstractmethod

from .errors import (
    InvalidBindingTransformError,
    InvalidBindingExpressionError
)


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

        if res is None:
            return None

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
        cur_val = self.__get__(target, *args, **kwargs)
        if cur_val != new_val:
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
    """
    A value that can be watched using the Observable pattern.
    """
    def __init__(self, bindable: Bindable,
                       instance: Any) -> None:
        """
        Create a one-way or two-way binding between `@bindable` properties.
        By using a binding instead of a variable reference, when the value of
        the property changes, the bound value will also change.
        Example:
        >>> Button(title=Binding(ViewModel.button_title, self.vm))

        If the field needs to be transformed before binding, use a `transform` modifier.
        Note that transformed bindings will automatically become one-way bindings.
        Example:
        >>> Label(text=Binding(Person.gender, self.vm.person)
                .transform(lambda x: 'Male' if x == Gender.male else 'Female'))

        If the binding should be more complex, i.e. using more than a field in the transform
        expression, use a `BindingExpression` instead.

        Args:
            bindable (Bindable): `@bindable` property to bind to.
            instance (Any): Instance that contains the desided `@bindable` property.
        """
        self.bindable = bindable
        self.instance = instance

        self.transforms = []

    def transform(self, transform: Callable) -> AbstractBinding:
        """
        Transform the bound value before passing it over to the binding property.

        Args:
            transform (Callable): A function (or lambda expression) that modifies the bound value.

        Returns:
            Binding: self
        """        
        self.transforms.append(transform)
        return self

    @property
    def on_changed(self) -> Signal:
        """
        Signal that is triggered when the bound value has changed.

        Returns:
            Signal: The signal that is triggered when the bound value has changed.
        """        
        return self.bindable.on_changed

    @property
    def value(self) -> Any:
        """
        The new binding value after applying all transforms.

        Raises:
            Exception: _description_

        Returns:
            Any: The new binding value after applying all transforms.
        """        
        new_value = self.bindable.fget(self.instance)

        for transform in self.transforms:
            if not callable(transform):
                raise InvalidBindingTransformError()

            new_value = transform(new_value)

        return new_value

    @value.setter
    def value(self, new_val):
        cur_val = self.bindable.fget(self.instance)
        w_type = self.bindable.type_
        if not issubclass(w_type, BindableMixin):
            try:
                new_val = w_type(new_val)
            except ValueError:
                new_val = cur_val
        self.bindable.__set__(self.instance, new_val)


class BindingExpression(AbstractBinding):
    """
    One or more values that can be combined into a watchable expression using the Observable pattern.
    """

    def __init__(self, expression: Callable, *args: Tuple[Bindable, Any]) -> None:
        """
        Create a one-way or two-way binding between a `@bindable` property and an expression
        containing one or more `@bindable` properties.
        By using a binding expression instead of a variable reference, when the value of
        the property changes, the bound value will also change.
        Example:
        >>> Button(title='Ok') \
                .is_enabled(BindingExpression(lambda n, v: n is not None and v > 10,
                                                (ViewModel.name, self.vm),
                                                (ViewModel.value, self.vm)))

        If the binding should be simple, i.e. using just one field in the transform
        expression, use a `Binding` instead with a `transform` modifier.

        If the binding should be two-way, refactor it as to use a single `@bindable` property
        in the expression and use a `Binding` instead, without a `transform` modifier.

        Args:
            expression (Callable): expression to be evaluated after the binding.

        Raises:
            InvalidBindingExpressionError: At least one bindable and one instance must be provided.
            InvalidBindingExpressionError: Must provide a callable expression.
            InvalidBindingExpressionError: Invalid argument. Must a tuple of bindable and instance.
        """
        if len(args) == 0:
            raise InvalidBindingExpressionError('At least one bindable and one instance must be provided.')

        self.bindables = []
        self._on_changed = Signal()

        if not callable(expression):
            raise InvalidBindingExpressionError('Must provide a callable expression.')

        self.expression = expression

        for arg in args:
            if type(arg) != tuple:
                raise InvalidBindingExpressionError('Invalid argument. Must a tuple of bindable and instance.')

            bindable, _ = arg

            if type(bindable) != Bindable:
                raise InvalidBindingExpressionError('Invalid argument. Must a tuple of bindable and instance.')

            bindable.on_changed.connect(self._on_property_in_expression_changed)

            self.bindables.append(arg)

    def _on_property_in_expression_changed(self, signal, sender, event):
        self.on_changed.emit()

    @property
    def value(self) -> Any:
        """
        Value of the evaluated `Binding Expression`.

        Returns:
            Any: value of the evaluated `Binding Expression`.
        """        
        arguments = [b.fget(i) for b, i in self.bindables]
        return self.expression(*arguments)

    @property
    def on_changed(self) -> Signal:
        """
        Signal that is triggered when any of the bound `@bindable` properties change, so the
        expression result can be recalculated.

        Returns:
            Signal: Signal that is triggered when any of the bound `@bindable` properties change.
        """        
        return self._on_changed

class ApplepyException(Exception):
    pass


class ViewParsingError(ApplepyException):
    pass


class AddingMultipleChildrenToNonStackableViewError(ViewParsingError):
    def __init__(self) -> None:
        super().__init__('Only one child view can be added to a non-stackable view.')


class UnsuportedParentError(ViewParsingError):
    def __init__(self, type_: type, parent_type: type) -> None:
        super().__init__(f'Unsuported parent. child:[{type_}], parent:[{parent_type}]')


class NotStatusBarAppError(ViewParsingError):
    def __init__(self) -> None:
        super().__init__(f'This view requires a StatusBarApp but is being used in a different kind of App.')


class InvalidBindingTransformError(ViewParsingError):
    def __init__(self) -> None:
        super().__init__('Invalid binding transform.')


class InvalidBindingExpressionError(ViewParsingError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

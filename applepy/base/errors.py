class ApplepyException(Exception):
    pass


class ViewParsingError(ApplepyException):
    pass


class AddingMultipleChildrenToNonStackableViewError(ViewParsingError):
    def __init__(self, *args: object) -> None:
        super().__init__('Only one child view can be added to a non-stackable view.', *args)

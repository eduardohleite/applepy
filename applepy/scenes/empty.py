from .. import Scene
from ..backend.app_kit import NSObject


class EmptyScene(Scene):
    """ An Empty Scene. Use it for applications that do not have a main window. """

    def __init__(self) -> None:
        """
        Add a new `EmptyScene` scene, which can be used in applications that have no main windows,
        such as Status Bar only applications.
        Always return the scene from the application's body and use it in a `with` statement in order
        to add children to it. Example:

        >>> with EmptyScene() as w:
                StatusIcon().set_title('status only')
                return w

        Layouts and Control views cannot be children of an `EmptyScene`. As it has no appearence, it only
        accepts non-visible views as children.
        """
        super().__init__((type(None),))

    def body(self) -> Scene:
        """
        EmptyScene's body method.
        It can be overriden in the View code.
        It is used internally for rendering the components, do not call it directly.

        Returns:
            EmptyScene: self
        """
        return super().body()

    def get_ns_object(self) -> NSObject:
        """
        Empty scenes have no underlying NSObject, so this always returns None.

        Returns:
            None.
        """
        return None

    def parse(self) -> Scene:
        """
        EmptyScene's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            EmptyScene: self
        """
        return super().parse()

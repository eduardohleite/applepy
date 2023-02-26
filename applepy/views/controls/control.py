from ...base.view import View
from ...base.transform_mixins import Enable
from ..layout import StackView


class Control(View, Enable):
    """ Base class for Control-based views. """

    def __init__(self) -> None:
        """
        Create a new `Control` view.
        """        
        View.__init__(self)
        Enable.__init__(self)

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Control: self
        """
        if isinstance(self.parent, StackView):
            self.parent.ns_object.addArrangedSubview_(self.ns_object)
        else:
            self.parent.set_content_view(self.ns_object)
        return View.parse(self)

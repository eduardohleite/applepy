from ...base.view import View
from ...base.transform_mixins import Enable
from ..layout import StackView


class Control(View, Enable):
    def __init__(self) -> None:
        View.__init__(self)
        Enable.__init__(self)

    def parse(self):
        if isinstance(self.parent, StackView):
            self.parent.ns_object.addArrangedSubview_(self.ns_object)
        else:
            self.parent.ns_object.contentView = self.ns_object

        return View.parse(self)

    def ignore_multi_click(self, value: bool):
        def __modifier():
            self.ns_object.ignore_multi_click = value

        self._modifiers.append(__modifier)

        return self

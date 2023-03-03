from ..backend import _MACOS, _IOS
from .. import Scene
from ..base.mixins import Modifiable
from ..base.errors import NotSupportedError

if _IOS:
    from ..backend.ui_kit import UIPageViewController, NSObject


class PageController(Scene,
                    Modifiable):
    def __init__(self) -> None:
        if _MACOS:
            raise NotSupportedError()

        Scene.__init__(self, (type(None),))
        Modifiable.__init__(self)

        self.view_controller = None

    def body(self) -> Scene:
        return super().body()

    def get_ns_object(self):
        return self.view_controller

    def parse(self) -> Scene:
        Scene.parse(self)
        Modifiable.parse(self)

        self.view_controller = UIPageViewController.alloc().init()

        return self
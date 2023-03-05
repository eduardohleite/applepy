from uuid import uuid4

from ..backend import _MACOS, _IOS
from .. import Scene
from ..base.errors import AddingMultipleChildrenToNonStackableViewError
from ..base.mixins import Modifiable
from ..base.errors import NotSupportedError

if _IOS:
    from ..backend.ui_kit import UIViewController, NSObject, objc_method
if _MACOS:
    from ..backend.app_kit import UIViewController, NSObject, objc_method


class SimpleScreen(Scene,
                   Modifiable):
    def __init__(self) -> None:
        if _MACOS:
            raise NotSupportedError()

        Scene.__init__(self, (type(None),))
        Modifiable.__init__(self)

        self.view_controller = None
        self.content_view = None

    def body(self) -> Scene:
        return super().body()

    def get_ns_object(self) -> UIViewController:
        return self.view_controller

    def parse(self) -> Scene:
        @objc_method
        def viewDidLoad(_self):
            _self.view = self.content_view

        _ViewController = type(f'_ViewController_{uuid4().hex[:8]}', (UIViewController,), {
            'viewDidLoad': viewDidLoad
        })

        self.view_controller = _ViewController.alloc().init()

        Scene.parse(self)
        Modifiable.parse(self)

        return self
    
    def set_content_view(self, content_view: NSObject) -> None:
        if self.content_view:
            raise AddingMultipleChildrenToNonStackableViewError()

        self.content_view = content_view

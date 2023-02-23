from typing import Callable, Optional, Union

from .. import Scene, Size, Point
from ..base.binding import AbstractBinding, bindable
from ..base.mixins import Modifiable
from ..base.transform_mixins import (
    BackgroundColor,
    AlphaValue,
    HasShadow,
    TitledControl,
    Visible
)
from ..backend.app_kit import (
    NSObject,
    NSWindow,
    NSWindowStyleMask,
    NSBackingStoreType,
    NSRect, NSPoint, NSSize,
    objc_method
)


class Window(Scene,
             Modifiable,
             BackgroundColor,
             AlphaValue,
             HasShadow,
             TitledControl,
             Visible):

    @bindable(Size)
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, val: Size):
        self._size = val

    def __init__(self,
                 *,
                 title: Union[AbstractBinding, str],
                 size: Size,
                 position: Point = Point(0, 0),
                 borderless: bool = False,
                 titled: bool = True,
                 closable: bool = True,
                 resizable: bool = True,
                 miniaturizable: bool = True,
                 full_screen: bool = False,
                 full_size_content_view: bool = False,
                 utility_window: bool = False,
                 doc_modal_window: bool = False,
                 non_activating_panel: bool = False,
                 hud_window: bool = False,
                 min_size: Optional[Size] = None,
                 max_size: Optional[Size] = None,
                 on_close: Optional[Callable] = None) -> None:

        Scene.__init__(self)
        Modifiable.__init__(self)
        BackgroundColor.__init__(self)
        TitledControl.__init__(self, title)

        class _Delegate(NSObject):
            @objc_method
            def windowWillClose_(_self, sender):
                if on_close and callable(on_close):
                    on_close()

            @objc_method
            def windowDidEndLiveResize_(_self, notification):
                w = self.window
                pass


        self._controller = _Delegate.alloc().init()

        self._size = size
        self.position = position
        self.borderless = borderless
        self.titled = titled
        self.closable = closable
        self.resizable = resizable
        self.miniaturizable = miniaturizable
        self.full_screen = full_screen
        self.full_size_content_view = full_size_content_view
        self.utility_window = utility_window
        self.doc_modal_window = doc_modal_window
        self.non_activating_panel = non_activating_panel
        self.hud_window = hud_window
        self.min_size = min_size
        self.max_size = max_size

    def body(self):
        return super().body()

    def get_ns_object(self):
        return self.window

    def parse(self):
        style_mask = 0

        if self.borderless:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskBorderless.value

        if self.titled:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskTitled.value

        if self.closable:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskClosable.value

        if self.resizable:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskResizable.value

        if self.miniaturizable:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskMiniaturizable.value

        if self.full_screen:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskFullScreen.value

        if self.full_size_content_view:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskFullSizeContentView.value

        if self.doc_modal_window:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskDocModalWindow.value

        if self.non_activating_panel:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskNonactivatingPanel.value

        if self.hud_window:
            style_mask |= NSWindowStyleMask.NSWindowStyleMaskHUDWindow.value

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSRect(NSPoint(self.position.x, self.position.y),
                   NSSize(self.size.width, self.size.height)),
            style_mask,
            NSBackingStoreType.NSBackingStoreBuffered.value,
            False
        )

        self.window.delegate = self._controller
        self.window.orderFrontRegardless()
        self.window.title = self.title
        if self.min_size:
            self.window.minSize = NSSize(self.min_size.width, self.min_size.height)
        if self.max_size:
            self.window.maxSize = NSSize(self.max_size.width, self.max_size.height)

        Scene.parse(self)
        Modifiable.parse(self)

        return self

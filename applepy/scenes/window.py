from .. import Scene, Size, Point
from ..base.mixins import Modifiable
from ..base.transform_mixins import (
    BackgroundColor,
    AlphaValue,
    HasShadow
)
from ..backend.app_kit import (
    NSWindow,
    NSWindowStyleMask,
    NSBackingStoreType,
    NSRect, NSPoint, NSSize
)


class Window(Scene,
             Modifiable,
             BackgroundColor,
             AlphaValue,
             HasShadow):
    def __init__(self,
                 *,
                 title: str,
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
                 hud_window: bool = False) -> None:

        Scene.__init__(self)
        Modifiable.__init__(self)
        BackgroundColor.__init__(self)

        self.title = title
        self.size = size
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

        self.window.orderFrontRegardless()
        self.window.title = self.title

        Scene.parse(self)
        Modifiable.parse(self)

        return self

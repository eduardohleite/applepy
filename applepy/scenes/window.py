from typing import Callable, Optional, Union
from uuid import uuid4

from .. import Scene, Size, Point
from ..views.menu import MainMenu
from ..base.binding import AbstractBinding, bindable
from ..base.mixins import Modifiable
from ..base.utils import attachable, try_call
from ..base.view import View
from ..base.errors import (
    AddingMultipleChildrenToNonStackableViewError
)
from ..base.transform_mixins import (
    BackgroundColor,
    AlphaValue,
    HasShadow,
    TitledControl,
    Visible
)
from ..backend.app_kit import (
    NSApp,
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
    """ Display a MacOS Window. """

    @bindable(Size)
    def size(self) -> Size:
        """
        Window content dimensions.
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            Size: the dimensions of the window's content area.
        """
        return self._size

    @size.setter
    def size(self, val: Size) -> None:
        self._size = val

    @bindable(Point)
    def position(self) -> Point:
        """
        Window position (origin).
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            Point: the position (origin) of the window.
        """
        return self._position

    @position.setter
    def position(self, val: Point) -> None:
        self._position = val

    @bindable(bool)
    def full_screen(self) -> bool:
        """
        Gets whether window is in full-screen mode.
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            bool: `True` if window is in full-screen mode, `False` otherwise.
        """
        return self._full_screen

    @full_screen.setter
    def full_screen(self, val: bool) -> None:
        self._full_screen = val

    @attachable(MainMenu)
    def menu(self) -> MainMenu:
        """
        A main menu to be displayed if this is the main window.
        Do not call it directly, instead, add a MainMenu element to the window's stack.

        Returns:
            MainMenu: The application's main menu when this is the main window.
        """
        return self._menu

    @menu.setter
    def menu(self, val: MainMenu) -> None:
        self._menu = val
        NSApp.mainMenu = val._main_menu

    # @attachable(Toolbar)
    # def toolbar(self) -> Toolbar:
    #     return self._toolbar

    # @toolbar.setter
    # def toolbar(self, val: Toolbar) -> None:
    #     self._toolbar = val

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
                 on_close: Optional[Callable] = None,
                 on_resized: Optional[Callable] = None,
                 on_moved: Optional[Callable] = None,
                 on_full_screen_changed: Optional[Callable] = None,
                 on_minimized: Optional[Callable] = None) -> None:

        """
        Add a new `Window` scene, which generates a native MacOS window.
        Windows, as scenes, can only be a top level item in the App's body method, they cannot be a stacked or child of a view.
        The first `Window` instance added to the application will be set as the main window for the application, but for it to be effective,
        return the window object at the end of the body method.
        Use it in a `with` statement in order to add children to it. Example:

        >>> with Window() as w:
                Label(text='hello world')
                return w

        If you need more than one widget in the same window, use layout widgets such as the `StackView`:

        >>> with Window() as w:
                with VerticalStack():
                    Label(text='I am at the top')
                    Label(text='I am at the bottom')
                return w

        A window can also receive modifiers. For instance, to bind the `visible` property to an external bindable, use:

        >>> with Window() as w:
                return w.is_visible(Binding(MyApp.show_main_window, self))

        Args:
            title (Union[AbstractBinding, str]): The window's title. This parameter accepts binding. Binding can also be set later with the `set_title` modifier.
            size (Size): The window's initial content size.
            position (Point, optional): The window's initial position (origin). Defaults to Point(0, 0).
            borderless (bool, optional): Whether the window should be borderless. Defaults to False.
            titled (bool, optional): Whether the window should display the title bar. Defaults to True.
            closable (bool, optional): Whether the window should be closable. Defaults to True.
            resizable (bool, optional): Whether the window should be resizable. Defaults to True.
            miniaturizable (bool, optional): Whether the window should be minimizable. Defaults to True.
            full_screen (bool, optional): Whether the window should be open in full-screen mode. Defaults to False.
            full_size_content_view (bool, optional): Whether the window should have a full sized content view. Defaults to False.
            utility_window (bool, optional): Whether the window should be displayed as a utility window. Defaults to False.
            doc_modal_window (bool, optional): Whether the window is a document-modal panel. Defaults to False.
            non_activating_panel (bool, optional): Whether the window is a `Panel` that does not activate the owning app. Defaults to False.
            hud_window (bool, optional): Whether the window should be a HUD panel. Defaults to False.
            min_size (Optional[Size], optional): The window's minimum size. Defaults to None.
            max_size (Optional[Size], optional): The window's maximum size. Defaults to None.
            on_close (Optional[Callable], optional): Action to be executed when the window closes. Defaults to None.
            on_resized (Optional[Callable], optional): Action to be executed when the window is resized. Defaults to None.
            on_moved (Optional[Callable], optional): Action to be executed when the window is moved. Defaults to None.
            on_full_screen_changed (Optional[Callable], optional): Action to be executed when the window enters or exits full-screen mode. Defaults to None.
            on_minimized (Optional[Callable], optional): Action to be executed when the window is minimized. Defaults to None.
        """
        Scene.__init__(self, (type(None), Window))
        Modifiable.__init__(self)
        BackgroundColor.__init__(self)
        TitledControl.__init__(self, title)

        @objc_method
        def windowWillClose_(_self, sender):
            try_call(on_close)

        @objc_method
        def windowDidEndLiveResize_(_self, notification):
            w_rect = self.window.contentRectForFrameRect_(self.window.frame)
            self.size = Size(int(w_rect.size.width), int(w_rect.size.height))
            self.position = Point(int(w_rect.origin.x), int(w_rect.origin.y))
            try_call(on_resized)

        @objc_method
        def windowDidMove_(_self, notification):
            w_rect = self.window.contentRectForFrameRect_(self.window.frame)
            self.position = Point(int(w_rect.origin.x), int(w_rect.origin.y))
            try_call(on_moved)

        @objc_method
        def windowWillEnterFullScreen_(_self, notification):
            self.full_screen = True
            try_call(on_full_screen_changed)

        @objc_method
        def windowWillExitFullScreen_(_self, notification):
            self.full_screen = False
            try_call(on_full_screen_changed)

        @objc_method
        def windowDidMiniaturize_(self, notification):
            try_call(on_minimized)

        _WindowDelegate = type(f'_WindowDelegate_{uuid4().hex[:8]}', (NSObject,), {
            'windowWillClose_': windowWillClose_,
            'windowDidEndLiveResize_': windowDidEndLiveResize_,
            'windowDidMove_': windowDidMove_,
            'windowWillEnterFullScreen_': windowWillEnterFullScreen_,
            'windowWillExitFullScreen_': windowWillExitFullScreen_,
            'windowDidMiniaturize_': windowDidMiniaturize_
        })

        self.window = None
        self._controller = _WindowDelegate.alloc().init()

        # bindables
        self._size = size
        self._position = position
        self._full_screen = full_screen

        # regular properties
        self.borderless = borderless
        self.titled = titled
        self.closable = closable
        self.resizable = resizable
        self.miniaturizable = miniaturizable
        self.full_size_content_view = full_size_content_view
        self.utility_window = utility_window
        self.doc_modal_window = doc_modal_window
        self.non_activating_panel = non_activating_panel
        self.hud_window = hud_window
        self.min_size = min_size
        self.max_size = max_size

        # child views
        self.content_view: Optional[NSObject] = None

        # attachables
        self._menu: Optional[View] = None
        self._toolbar: Optional[View] = None

        # inferred properties
        self.is_main = False

    def body(self) -> Scene:
        """
        Window's body method.
        It can be overriden in the View code.
        It is used internally for rendering the components, do not call it directly.

        Returns:
            Window: self
        """
        return super().body()

    def get_ns_object(self) -> NSWindow:
        """
        Window's NSWindow instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSWindow: window's NSWindow instance.
        """
        return self.window

    def parse(self) -> Scene:
        """
        Window's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Window: self
        """
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

    def set_content_view(self, content_view: NSObject) -> None:
        """
        Sets the window's content view.
        A window is not a stacked view, so it can only have one content view.
        It is used internally for rendering the components, do not call it directly.

        Args:
            content_view (NSObject): The content view to be added to the window.

        Raises:
            AddingMultipleChildrenToNonStackableViewError: Window already has a content view.
        """
        if self.content_view:
            raise AddingMultipleChildrenToNonStackableViewError()
        
        self.content_view = content_view
        self.window.contentView = content_view

    def center(self) -> None:
        """
        Center the window in the screen.
        """        
        def __modifier():
            self.window.center()

        self._modifiers.append(__modifier)
        return self

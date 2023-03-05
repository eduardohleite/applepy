import asyncio

from abc import ABC, abstractmethod
from typing import Callable, Union, Any

from ..backend import _IOS, _MACOS
from .utils import try_call, try_call_async
from .errors import NotSupportedError

if _MACOS:
    from ..backend.app_kit import (
        NSObject,
        NSApp,
        NSMenuItem,
        NSButton,
        NSStatusBar,
        UIButton,
        EventLoopPolicy,
        CocoaLifecycle,
        objc_method,
        SEL
    )

if _IOS:
    from ..backend.ui_kit import (
        NSObject,
        NSMenuItem,
        NSButton,
        UIWindow,
        UIScreen,
        UIButton,
        UIApplicationMain,
        NSStringFromClass,
        ObjCInstance,
        EventLoopPolicy,
        iOSLifecycle,
        objc_method,
        objc_property,
        SEL
    )


_current_app = None


class StackMixin:
    """
    StackMixin
    Mixin that adds a `list` variable to the target class and methods to handle
    it as a Stack data structure.
    """

    def __init__(self) -> None:
        """
        Initialize the `StackMixin`.
        """    
        self._stack: list = []

    def stack(self, child: Any) -> None:
        """
        Add a child element to the top of the stack.

        Args:
            child (Any): Child element to be added to stack.
        """        
        self._stack.append(child)

    def pop(self) -> Any:
        """
        Remove and return the last element in the stack.

        Returns:
            Any: Item removed from the stack.
        """        
        return self._stack.pop()

    def pop_first(self) -> Any:
        """
        Remove and return the first element in the stack.

        Returns:
            Any: Item removed from the stack.
        """        
        return self._stack.pop(0)

    def get(self) -> Any:
        """
        Return the last element in the stack without removing it.

        Returns:
            Any: Last item in the stack.
        """        
        return self._stack[-1] if len(self._stack) > 0 else None

    def is_stacked(self, ptr: Any) -> bool:
        """
        Checks whether the provided object has been stacked already.

        Args:
            ptr (Any): Pointer to be object to be checked.

        Returns:
            bool: True is pointer has alsready been stacked. False otherwise.
        """        
        return ptr in self._stack

if _MACOS:
    class _ApplicationController(NSObject):
        @objc_method
        def applicationDidFinishLaunching_(self, notification):
            _current_app.setup_scene()

        @objc_method
        def actionProxy_(self, target):
            _current_app.invoke_action(target)

        @objc_method
        def actionProxyAsync_(self, target):
            asyncio.create_task(_current_app.invoke_action_async(target))

if _IOS:
    class _TouchApplicationController(NSObject):
        window = objc_property()

        @objc_method
        def application_didFinishLaunchingWithOptions_(self, app, options) -> bool:
            _current_app.setup_scene()
            return True
        
        @objc_method
        def actionProxy_(self, target):
            _current_app.invoke_action(target)

        @objc_method
        def actionProxyAsync_(self, target):
            asyncio.create_task(_current_app.invoke_action_async(target))


class App(ABC, StackMixin):
    def __init__(self) -> None:
        StackMixin.__init__(self)

        if _MACOS:
            self._controller = _ApplicationController.alloc().init()
            NSApp.delegate = self._controller
        
        if _IOS:
            self._controller = _TouchApplicationController.alloc().init()

        self._actions = {}
        self._async_actions = {}

    def _register_scene(self) -> None:
        if _MACOS:
            from ..scenes import Window
            if isinstance(self._scene, Window):
                self._controller.mainWindow = self._scene.window
                NSApp.activateIgnoringOtherApps_(True)
        
        if _IOS:
            from ..scenes import SimpleScreen
            if isinstance(self._scene, SimpleScreen):
                self._controller.window = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
                self._controller.window.rootViewController = self._scene.view_controller
                self._controller.window.makeKeyAndVisible()

    @abstractmethod
    def body(self):
        return self

    def run(self) -> int:
        global _current_app
        _current_app = self

        if _MACOS:
            return NSApp.run()

        if _IOS:
            return UIApplicationMain(0, None, None, ObjCInstance(NSStringFromClass(_TouchApplicationController)))
        
    def run_async(self) -> int:
        global _current_app
        _current_app = self

        asyncio.set_event_loop_policy(EventLoopPolicy())
        self.loop = asyncio.new_event_loop()

        if _MACOS:
            self.loop.run_forever(lifecycle=CocoaLifecycle(NSApp))

        if _IOS:
            class _TouchAsyncApplicationController(_TouchApplicationController):
                @objc_method
                def application_didFinishLaunchingWithOptions_(_self, app, options) -> bool:
                    _current_app.setup_scene()
                    self.loop.run_forever_cooperatively(lifecycle=iOSLifecycle())
                    return True

            return UIApplicationMain(0, None, None, ObjCInstance(NSStringFromClass(_TouchAsyncApplicationController)))

    def setup_scene(self) -> None:
        self._scene = self.body().parse()
        self._register_scene()

    def register_action(self, caller: Union[NSMenuItem, NSButton, UIButton], action: Callable) -> SEL:
        self._actions[caller] = action
        return SEL('actionProxy:')
    
    def register_async_action(self, caller: Union[NSMenuItem, NSButton, UIButton], action: Callable) -> SEL:
        self._async_actions[caller] = action
        return SEL('actionProxyAsync:')

    def invoke_action(self, caller: Union[NSMenuItem, NSButton, UIButton]):
        action = self._actions.get(caller)
        try_call(action)

    async def invoke_action_async(self, caller: Union[NSMenuItem, NSButton, UIButton]):
        action = self._async_actions.get(caller)
        await try_call_async(action)

    def quit(self):
        if _MACOS:
            NSApp.terminate_(None)

        if _IOS:
            raise NotSupportedError()


class StatusBarApp(App):
    """
    An `App` that may use a button in the Operating System's Status Bar
    """

    def __init__(self) -> None:
        """
        Initialize a new `StatusBarApp` instance.
        """
        if _IOS:
            raise NotSupportedError()

        super().__init__()
        self.status_bar_icon = NSStatusBar.systemStatusBar.statusItemWithLength_(-1.)


def get_current_app() -> App:
    """
    Return the current running `App` instance.

    Returns:
        App: Current running `App` instance.
    """
    return _current_app

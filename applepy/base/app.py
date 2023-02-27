from abc import ABC, abstractmethod
from typing import Callable, Union, Any

from .utils import try_call
from ..backend.app_kit import (
    NSObject,
    NSApp,
    NSMenuItem,
    NSButton,
    NSStatusBar,
    objc_method,
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


class _ApplicationController(NSObject):
    @objc_method
    def applicationDidFinishLaunching_(self, notification):
        _current_app.setup_scene()

    @objc_method
    def menuAction_(self, menu_item):
        _current_app.invoke_action(menu_item)


class App(ABC, StackMixin):
    def __init__(self) -> None:
        StackMixin.__init__(self)

        self._controller = _ApplicationController.alloc().init()
        NSApp.delegate = self._controller

        self._actions = {}

    def _register_scene(self) -> None:
        from ..scenes import Window
        if isinstance(self._scene, Window):
            self._controller.mainWindow = self._scene.window
            NSApp.activateIgnoringOtherApps_(True)

    @abstractmethod
    def body(self):
        return self

    def run(self) -> None:
        global _current_app
        _current_app = self

        NSApp.run()

    def setup_scene(self) -> None:
        self._scene = self.body().parse()
        self._register_scene()

    def register_action(self, caller: Union[NSMenuItem, NSButton], action: Callable) -> SEL:
        self._actions[caller] = action
        return SEL('menuAction:')

    def invoke_action(self, caller: Union[NSMenuItem, NSButton]):
        action = self._actions.get(caller)
        try_call(action)

    def quit(self):
        NSApp.terminate_(None)


class StatusBarApp(App):
    """
    An `App` that may use a button in the Operating System's Status Bar
    """

    def __init__(self) -> None:
        """
        Initialize a new `StatusBarApp` instance.
        """        
        super().__init__()
        self.status_bar_icon = NSStatusBar.systemStatusBar.statusItemWithLength_(-1.)


def get_current_app() -> App:
    """
    Return the current running `App` instance.

    Returns:
        App: Current running `App` instance.
    """    
    return _current_app


from abc import ABC, abstractmethod
from typing import Callable, Optional, Union

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
    def __init__(self) -> None:
        self._stack: list = []

    def stack(self, child) -> None:
        self._stack.append(child)

    def pop(self):
        return self._stack.pop()

    def pop_first(self):
        return self._stack.pop(0)

    def get(self):
        return self._stack[-1] if len(self._stack) > 0 else None

    def is_stacked(self, ptr):
        return ptr in self._stack


class ApplicationController(NSObject):
    @objc_method
    def applicationDidFinishLaunching_(self, notification):
        _current_app.setup_scene()

    @objc_method
    def menuAction_(self, menu_item):
        _current_app.invoke_action(menu_item)


class App(ABC, StackMixin):
    def __init__(self) -> None:
        StackMixin.__init__(self)

        self._controller = ApplicationController.alloc().init()
        NSApp.delegate = self._controller

        self._actions = {}

    def _register_scene(self) -> None:
        self._scene.is_main = True
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
    def __init__(self) -> None:
        super().__init__()
        self.status_bar_icon = NSStatusBar.systemStatusBar.statusItemWithLength_(-2.)


def get_current_app() -> App:
    return _current_app


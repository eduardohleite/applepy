from typing import Callable, Optional, Union

from .. import View, StackedView, Image
from ..backend.app_kit import NSMenu, NSMenuItem, NSApp, NSStatusBar, NSImage, NSSize
from ..base.app import get_current_app, StatusBarApp
from ..base.binding import Binding


class MainMenu(StackedView):
    def __init__(self) -> None:
        super().__init__()

    def get_ns_object(self):
        return self._main_menu

    def parse(self):
        self._main_menu = NSMenu.alloc().init()
        super().parse()
        NSApp.mainMenu = self._main_menu
        return self


class Menu(StackedView):
    def __init__(self, *, title: str,
                          action: Optional[Callable] = None,
                          key_equivalent: str = '') -> None:
        super().__init__()
        self._parent_menu = get_current_app().get()

        if type(self._parent_menu) != MainMenu:
            raise Exception('Menu should be a child of MainMenu.')

        self.id = id
        self.title = title
        self.action = action
        self.key_equivalent = key_equivalent

    def get_ns_object(self):
        return self._main_menu_item

    def parse(self):
        self._main_menu_item = NSMenuItem \
            .alloc() \
            .initWithTitle_action_keyEquivalent_(self.title,
                                                 None,
                                                 self.key_equivalent)

        if self.action:
            self._main_menu_item.setAction_(
                get_current_app().register_action(self._main_menu_item, self.action) 
            )

        self._main_menu_item_menu = NSMenu \
            .alloc() \
            .initWithTitle(self.title)

        self._main_menu_item.submenu = self._main_menu_item_menu
        self._parent_menu._main_menu.addItem(self._main_menu_item)

        super().parse()


class MenuItem(View):
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

        if self._menu_item:
            self._menu_item.title = value

    def __init__(self, *, title: Union[str, Binding],
                          action: Optional[Callable] = None,
                          key_equivalent: str = '') -> None:
        super().__init__()

        self._parent_menu = get_current_app().get()
        self._menu_item = None

        if type(self._parent_menu) != Menu:
            raise Exception('MenuItem should be a child of Menu.')
        
        if isinstance(title, Binding):
            self.bound_title = title
            self.bound_title.on_changed.connect(self._on_title_changed)
            self.title = title.value
        else:
            self.title = title

        self.action = action
        self.key_equivalent = key_equivalent

    def _on_title_changed(self, signal, sender, event):
        self.title = self.bound_title.value

    def get_ns_object(self):
        return self._menu_item

    def parse(self):
        self._menu_item = self._parent_menu \
                              ._main_menu_item_menu \
                              .addItemWithTitle_action_keyEquivalent_(
                                  self.title,
                                  None,
                                  self.key_equivalent
                              )
        
        if self.action:
            self._menu_item.setAction_(
                get_current_app().register_action(self._menu_item, self.action) 
            )


class StatusIcon(View):
    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, val: Image) -> None:
        self._image = val
        self.ns_object.image = val.value

    def __init__(self) -> None:
        if not isinstance(get_current_app(), StatusBarApp):
            raise Exception('StatusIcon can only be used in a StatusBarApp')

        self._image = None

        super().__init__()

    def get_ns_object(self):
        return get_current_app().status_bar_icon.button

    def parse(self):
        super().parse()

        return self

    def set_image(self, image: Image): #TODO binding
        def __modifier():
            size = get_current_app().status_bar_icon.statusBar.thickness * 0.8
            image.value.size = NSSize(size, size)
            self.image = image

        self._modifiers.append(__modifier)

        return self

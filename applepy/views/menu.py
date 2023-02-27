from typing import Callable, Optional, Union

from .. import View, StackedView, Image, ImagePosition
from ..backend.app_kit import NSMenu, NSMenuItem, NSButton, NSSize
from ..base.mixins import AttachableMixin
from ..base.app import get_current_app, StatusBarApp
from ..base.utils import attachable
from ..base.errors import NotStatusBarAppError
from ..base.binding import AbstractBinding, bindable
from ..base.transform_mixins import Enable, TitledControl, KeyBindable, ImageControl


class Menu(StackedView, AttachableMixin):
    """
    Control that generates a native MacOS generic Menu that can be attached to other views.
    """    

    def __init__(self) -> None:
        """
        Add a new `Menu` view, which creates a native MacOS generic Menu that can be attached
        to other views.

        Use it within a `with` statement to attach it to the parent view and use a `with`
        statement to append nested submenus and menu items.

        Example:
        >>> with StatusIcon():
                with Menu():
                    Submenu(title='Close')
        """
        StackedView.__init__(self)
        AttachableMixin.__init__(self, (StatusIcon,))

    def get_ns_object(self) -> NSMenu:
        """
        The menu's NSMenu instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSMenu: the menu's NSMenu instance.
        """
        return self._main_menu

    def parse(self) -> StackedView:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Menu: self
        """
        self._main_menu = NSMenu.alloc().init()
        self._main_menu.autoenablesItems = False

        StackedView.parse(self)
        AttachableMixin.parse(self)

        return self


class MainMenu(StackedView, AttachableMixin):
    """
    Control that generates a native MacOS generic Menu that can be attached to a
    window to be set as the System Menu.
    """

    def __init__(self) -> None:
        """
        Add a new `MainMenu` view, which creates a native MacOS generic Menu that can be attached
        to a window to be set as the System Menu.

        Use it within a `with` statement to attach it to the parent scene and use a `with`
        statement to append nested submenus and menu items.

        Example:
        >>> with Window():
                with Menu():
                    Submenu(title='File')
                    Submenu(title='Edit')
                    Submenu(title='Help')
        """
        StackedView.__init__(self)
        from ..scenes import Window
        AttachableMixin.__init__(self, (Window,))

        self._main_menu = None

    def get_ns_object(self) -> NSMenu:
        """
        The menu's NSMenu instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSMenu: the menu's NSMenu instance.
        """
        return self._main_menu

    def parse(self) -> StackedView:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            MainMenu: self
        """
        self._main_menu = NSMenu.alloc().init()
        self._main_menu.autoenablesItems = False

        StackedView.parse(self)
        AttachableMixin.parse(self)

        return self


class Submenu(StackedView,
              TitledControl,
              Enable,
              KeyBindable):
    """
    Control that generates a native MacOS submenu that can be attached to a
    `Menu` or `MainMenu` and have nested `MenuItem`s.
    """

    def __init__(self, *, title: str,
                          action: Optional[Callable] = None,
                          key_equivalent: str = '') -> None:
        """
        Add a new `Submenu` view, which creates a native MacOS submenu that can be attached
        to a `Menu` or `MainMenu` and have nested `MenuItem`s.

        Use it within a `with` statement to attach it to the parent menu and use a `with`
        statement to append nested submenus and menu items.

        Example:
        >>> with Window():
                with Menu():
                    with Submenu(title='File'):
                        MenuItem(title='New')
                        MenuItem(title='Open...')
        """
        StackedView.__init__(self, (Menu, MainMenu))
        TitledControl.__init__(self, title)
        KeyBindable.__init__(self, key_equivalent)

        self._main_menu_item = None
        self.action = action

    def get_ns_object(self) -> NSMenuItem:
        """
        The submenu's NSMenuItem instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSMenuItem: the submenu's NSMenuItem instance.
        """
        return self._main_menu_item

    def parse(self) -> StackedView:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Submenu: self
        """
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

        self._main_menu_item_menu.autoenablesItems = False
        self._main_menu_item.submenu = self._main_menu_item_menu
        self.parent._main_menu.addItem(self._main_menu_item)

        StackedView.parse(self)
        TitledControl.parse(self, TitledControl)
        KeyBindable.parse(self, KeyBindable)

        return self


class MenuItem(View,
               TitledControl,
               Enable,
               KeyBindable):
    """
    Control that generates a native MacOS menu item that can be attached to a `Submenu`.
    """
    def __init__(self, *, title: Union[str, AbstractBinding],
                          action: Optional[Callable] = None,
                          key_equivalent: str = '') -> None:
        """
        Add a new `MenuItem` view, which creates a native MacOS menu item that can be attached
        to a `Menu` or `Submenu`.

        Use it within a `with` statement to attach it to the parent submenu.

        Example:
        >>> with Window():
                with Menu():
                    with Submenu(title='File'):
                        MenuItem(title='New')
                        MenuItem(title='Open...')

        A `MenuItem` can also be bound to an action and a key shortcut with its initializers:
        >>> with Window():
                with Menu():
                    with Submenu(title='app'):
                        MenuItem(title='Quit',
                                 key_equivalent='q',
                                 action=self.quit)
        """
        View.__init__(self, (Submenu, MainMenu, Menu))
        TitledControl.__init__(self, title)
        Enable.__init__(self)
        KeyBindable.__init__(self, key_equivalent)

        self._menu_item = None
        self.action = action
        self.key_equivalent = key_equivalent

    def get_ns_object(self) -> NSMenuItem:
        """
        The menu item's NSMenuItem instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSMenuItem: the menu item's NSMenuItem instance.
        """
        return self._menu_item

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            MenuItem: self
        """
        if isinstance(self.parent, Submenu):
            self._menu_item = self.parent \
                                  ._main_menu_item_menu \
                                  .addItemWithTitle_action_keyEquivalent_(
                                      self.title,
                                      None,
                                      self.key_equivalent
                                  )
        else:
            self._menu_item = NSMenuItem \
                                .alloc() \
                                .initWithTitle_action_keyEquivalent_(self.title,
                                                                     None,
                                                                     self.key_equivalent)
            self.parent.ns_object.addItem(self._menu_item)
        
        if self.action:
            self._menu_item.setAction_(
                get_current_app().register_action(self._menu_item, self.action) 
            )

        View.parse(self)
        TitledControl.parse(self, TitledControl)
        KeyBindable.parse(self, KeyBindable)

        return self


class MenuSeparator(View):
    """ Control that generates a MacOS native Menu Separator. """

    def __init__(self) -> None:
        """
        Add a new `MenuSeparator` view, which creates a native MacOS menu separator that can be attached
        to a `Menu` or `Submenu`.
        Example:
        >>> with MainMenu():
                with Submenu(title='File'):
                    MenuItem(title='New')
                    MenuItem(title='Open...')
                    MenuSeparator()
                    MenuItem(title='Save')
        """        
        super().__init__((Submenu, Menu))
        self._menu_item = None

    def get_ns_object(self) -> NSMenuItem:
        """
        The Menu Separator's NSMenuItem instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSMenuItem: the Menu Separator's NSMenuItem instance.
        """
        return self._menu_item

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            MenuSeparator: self
        """
        self._menu_item = NSMenuItem.separatorItem()

        if isinstance(self.parent, Submenu):
            self.parent._main_menu_item_menu.addItem(self._menu_item)
        else:
            self.parent.ns_object.addItem(self._menu_item)

        super().parse()

        return self


class StatusIcon(StackedView,
                 ImageControl,
                 TitledControl):

    """ Control that generates a native MacOS icon in the Status Bar. """

    @bindable(bool)
    def is_template(self) -> bool:
        """
        Whether the image in the icon is a template image, i.e. should adapt itself
        to changes in the Operating System's theme.
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            bool: True if the image in the icon is a template image, False otherwise.
        """        
        return self._is_template

    @is_template.setter
    def is_template(self, val: bool) -> None:
        self._is_template = val

    @attachable(Menu)
    def menu(self) -> Menu:
        """
        A menu to be displayed when user clicks the Status Bar button.
        Do not call it directly, instead, add a Menu element to the StatusIcon's stack.

        Returns:
            Menu: The menu displayed when user clicks the Status Bar button.
        """        
        return self._menu

    @menu.setter
    def menu(self, val: Menu) -> None:
        self._menu = val
        get_current_app().status_bar_icon.menu = self.menu.ns_object if self.menu else None

    def __init__(self, *, image: Optional[Union[Image, AbstractBinding]]=None,
                          image_position: Optional[Union[ImagePosition, AbstractBinding]]=None,
                          is_template: bool=True) -> None:
        """
        Add a new `StatusIcon` view, which adds an icon to the Operating System's Status Bar
        while the application is running. A menu can be specified with a `with` statement:

        >>> with StatusIcon():
                with Menu():
                    Submenu('Hello, World')

        Usually, the StatusIcon will display an image. The image can be a template image, i.e.
        adapt itself automatically to changes in the Operating System's theme. Before setting
        an image as template, make sure all pixels in the image are black and the visibility of
        each pixel is controlled by the Alpha channel. Please refer to Apple's documentation for
        more details.
        In case the image should not be treated as a template image, set it in the `is_template`
        initializer:

        >> StatusIcon(image=Image.from_file('icon.png'), is_template=False)

        The icon can also contain text, which is set with the `set_title` modifier. When using
        text, pay attention to the `image_position` initializer. The following sample will not
        display any text:

        >> StatusIcon(image=Image.from_file('icon.png')) \
            .set_title('Application')

        That is because, if an image is supplied, the default value for `image_position` is
        `ImagePosition.image_only`.

        The next example will, however display the text:

        >> StatusIcon() \
            .set_title('Application')

        That is because, if no image is supplied, the default value for `image_position` is
        `ImagePosition.no_image`.

        If you do want to display both an image and a text at once, you can control the placement
        of them using the `image_position` initializer. For example, the following example will
        display both the image (on the left) and the text (on the right):

        >> StatusIcon(image=Image.from_system('NSInfo'),
                      image_position=ImagePosition.image_left) \
                .set_title('Application')

        Args:
            image (Optional[Union[Image, AbstractBinding]], optional): Optional image to be displayed in the Status Bar icon. Defaults to None.
            image_position (Optional[Union[ImagePosition, AbstractBinding]], optional): Optional placement of the button image. Defaults to None.
            is_template (bool, optional): Whether the image in the icon is a template image. Defaults to True.

        Raises:
            NotStatusBarAppError: StatusIcon can only be used in a StatusBarApp
        """                         
                       
        if not isinstance(get_current_app(), StatusBarApp):
            raise NotStatusBarAppError()

        self._image = None
        self._menu = None
        self.is_template = is_template

        StackedView.__init__(self)
        TitledControl.__init__(self)
        ImageControl.__init__(self,
                              image,
                              image_position,
                              ImagePosition.image_only,
                              self._before_set_image)

    def _before_set_image(self, image: Image) -> None:
        size = get_current_app().status_bar_icon.statusBar.thickness * 0.8
        image.value.size = NSSize(size, size)
        image.value.template = self.is_template
        self._image = image

    def get_ns_object(self) -> NSButton:
        """
        The Status Bar item's button's NSButton instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSButton: the Status Bar item's button's NSButton instance.
        """
        return get_current_app().status_bar_icon.button

    def parse(self) -> StackedView:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            StatusIcon: self
        """
        StackedView.parse(self)
        TitledControl.parse(self, TitledControl)
        ImageControl.parse(self, ImageControl)
        return self

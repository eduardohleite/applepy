from uuid import uuid4
from typing import Union, Optional, Callable, Coroutine, List
from inspect import iscoroutinefunction

from ...backend import _IOS
from ...base.utils import attachable
from ...base.app import get_current_app
from ...base.types import Image, ToolbarDisplayMode, ToolbarStyle
from ...base.view import StackedView, View
from ...base.transform_mixins import (
    ControlWithLabel,
    ImageControl,
    Visible,
    Enable
)
from ...base.binding import BindableMixin, AbstractBinding, bindable
from ...base.mixins import AttachableMixin
from ...base.errors import NotSupportedError


if _IOS:
    raise NotSupportedError()

from ...backend.app_kit import (
    NSObject,
    NSToolbar,
    NSToolbarItem,
    objc_method
)


class ToolbarItem(View,
                  ControlWithLabel,
                  ImageControl,
                  Visible,
                  Enable,
                  AttachableMixin):
    @bindable(bool)
    def navigational(self) -> bool:
        return self._navigational
    
    @navigational.setter
    def navigational(self, val: bool) -> None:
        self._navigational = val

        if self.ns_object:
            self.ns_object.navigational = val

    def __init__(self, *,
                 label: Optional[Union[str, AbstractBinding]]=None,
                 image: Optional[Union[Image, AbstractBinding]]=None,
                 action: Optional[Union[Callable, Coroutine]]=None,
                 navigational: Union[bool, AbstractBinding]=False) -> None:
        View.__init__(self)
        ControlWithLabel.__init__(self, label)
        ImageControl.__init__(self, image)
        Visible.__init__(self)
        Enable.__init__(self)
        AttachableMixin.__init__(self)

        self.identifier = uuid4().hex[:8]
        self.action = action
        self._toolbar_item = None
        self._bordered = True

        if isinstance(navigational, AbstractBinding):
            self.bound_navigational = navigational
            self.bound_navigational.on_changed.connect(self._on_navigational_changed)
            self._navigational = navigational.value
        else:
            self._navigational = navigational

    def _on_navigational_changed(self, signal, sender, event):
        self.navigational = self.bound_navigational.value

    def get_ns_object(self) -> NSToolbarItem:
        return self._toolbar_item
    
    def parse(self):
        self._toolbar_item = NSToolbarItem.alloc().initWithItemIdentifier_(self.identifier)
        self._toolbar_item.bordered = True

        if self.action:
            self._toolbar_item.target = get_current_app()._controller
            if iscoroutinefunction(self.action):
                self._toolbar_item.action = \
                    get_current_app().register_async_action(self._toolbar_item, self.action)
            else:
                self._toolbar_item.action = \
                    get_current_app().register_action(self._toolbar_item, self.action)
        
        View.parse(self)
        ImageControl.parse(self, ImageControl)
        ControlWithLabel.parse(self, ControlWithLabel)
        AttachableMixin.parse(self)

        return self


class Toolbar(StackedView, AttachableMixin):
    @attachable(ToolbarItem)
    def items(self) -> List[ToolbarItem]:
        return self._items
    
    @items.setter
    def items(self, item: ToolbarItem):
        self._items.append(item)

    @bindable(ToolbarStyle)
    def style(self) -> ToolbarStyle:
        return self._style
    
    @style.setter
    def style(self, val: ToolbarStyle) -> None:
        self._style = val
        self._set_style()

    def __init__(self,
                 *,
                 display_mode: ToolbarDisplayMode=ToolbarDisplayMode.default,
                 show_separator: bool=True,
                 style: Union[AbstractBinding, ToolbarStyle]=ToolbarStyle.automatic) -> None:
        StackedView.__init__(self)
        AttachableMixin.__init__(self)

        self._toolbar = None
        self.display_mode = display_mode
        self.show_separator = show_separator
        self._items = []

        if isinstance(style, AbstractBinding):
            self.bound_style = style
            self.bound_style.on_changed.connect(self._on_style_changed)
            self._style = style.value
        else:
            self._style = style

        @objc_method
        def toolbarAllowedItemIdentifiers_(_self, toolbar):
            return []

        @objc_method
        def toolbarDefaultItemIdentifiers_(_self, toolbar):
            return [i.identifier for i in self._items]
        
        @objc_method
        def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(_self, toolbar, identifier, flag):
            item = next(filter(lambda i: i.identifier == identifier, self._items))
            return item.ns_object

        _ToolbarDelegate = type(f'_ToolbarDelegate{uuid4().hex[:8]}', (NSObject,), {
            'toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_': toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_,
            'toolbarDefaultItemIdentifiers_': toolbarDefaultItemIdentifiers_,
            'toolbarAllowedItemIdentifiers_': toolbarAllowedItemIdentifiers_
        })

        self._controller = _ToolbarDelegate.alloc().init()

    def get_ns_object(self) -> NSToolbar:
        return self._toolbar
    
    def _set_style(self) -> None:
        from ...scenes import Window
        if isinstance(self.parent, Window):
            self.parent.ns_object.toolbarStyle = self.style

    
    def parse(self):
        StackedView.parse(self)

        self._toolbar = NSToolbar.alloc().init()
        self._toolbar.displayMode = self.display_mode.value
        self._toolbar.showsBaselineSeparator = self.show_separator
        self._toolbar.delegate = self._controller

        self._set_style()

        AttachableMixin.parse(self)

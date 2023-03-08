from uuid import uuid4
from typing import Union, Optional, Callable, Coroutine, List, Tuple
from inspect import iscoroutinefunction

from ...backend import _IOS
from ...base.utils import attachable
from ...base.app import get_current_app
from ...base.types import (
    Image,
    ToolbarDisplayMode,
    ToolbarStyle,
    ToolbarItemSystemIdentifier
)
from ...base.view import StackedView, View
from ...base.transform_mixins import (
    ControlWithLabel,
    ImageControl,
    Visible,
    Enable
)
from ...base.binding import AbstractBinding, bindable
from ...base.mixins import AttachableMixin
from ...base.errors import NotSupportedError


if _IOS:
    raise NotSupportedError()

from ...backend.app_kit import (
    NSObject,
    NSToolbar,
    NSToolbarItem,
    NSToolbarItemGroup,
    NSSet,
    objc_method
)


class ToolbarItemBase(View,
                      AttachableMixin):
    """ Base class for Toolbar items (MacOS only). """

    def __init__(self,
                 identifier: Optional[str]=None) -> None:
        """
        Add a new `ToolbarItemBase` view.
        Do not use it directly, use one of its subclasses instead.
        If no identifier is provided, one will be generated.

        Args:
            identifier (Optional[str], optional): _description_. Defaults to None.
        """
        View.__init__(self, (Toolbar,))
        AttachableMixin.__init__(self)
        self.identifier = identifier if identifier else uuid4().hex[:8]

    def parse(self):
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            ToolbarItemBase: self
        """
        View.parse(self)
        AttachableMixin.parse(self)
        return self


class Toolbar(StackedView, AttachableMixin):
    """ Control that generates a native MacOS Toolbar (MacOS only)."""

    @attachable(ToolbarItemBase)
    def items(self) -> List[ToolbarItemBase]:
        """
        List of attachable items displayed in the toolbar.

        Returns:
            List[ToolbarItemBase]: List of items displayed in the toolbar.
        """        
        return self._items
    
    @items.setter
    def items(self, item: ToolbarItemBase):
        self._items.append(item)

    @bindable(ToolbarStyle)
    def style(self) -> ToolbarStyle:
        """
        Toolbar style.

        Returns:
            ToolbarStyle: Toolbar style.
        """        
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
        """
        Add a new `Toolbar` view, which creates a native MacOS Toolbar (MacOS only).
        It needs to be attached to a `Window` and can have items attached to it using a `with` statement.

        Example:
        >>> with Window():
                with Toolbar():
                    ToolbarSpace()

        Args:
            display_mode (ToolbarDisplayMode, optional): _description_. Defaults to ToolbarDisplayMode.default.
            show_separator (bool, optional): _description_. Defaults to True.
            style (Union[AbstractBinding, ToolbarStyle], optional): _description_. Defaults to ToolbarStyle.automatic.

        Returns:
            _type_: _description_
        """        
        StackedView.__init__(self)
        AttachableMixin.__init__(self)

        self._toolbar = None
        self.display_mode = display_mode
        self.show_separator = show_separator
        self._items: List[ToolbarItemBase] = []

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
        """
        The toolbar's NSToolbar instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSToolbar: the toolbar's NSToolbar instance.
        """
        return self._toolbar
    
    def _set_style(self) -> None:
        from ...scenes import Window
        if isinstance(self.parent, Window):
            self.parent.ns_object.toolbarStyle = self.style

    def parse(self):
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Toolbar: self
        """
        StackedView.parse(self)

        self._toolbar = NSToolbar.alloc().init()
        self._toolbar.displayMode = self.display_mode.value
        self._toolbar.showsBaselineSeparator = self.show_separator
        self._toolbar.delegate = self._controller

        self._set_style()

        AttachableMixin.parse(self)

        self._toolbar.centeredItemIdentifiers = \
            NSSet.setWithArray([x.identifier for x in self._items if x.centered])

        return self


class ToolbarItem(ToolbarItemBase,
                  ControlWithLabel,
                  ImageControl,
                  Visible,
                  Enable):
    """ Control that generates a native MacOS ToolbarItem (MacOS only). """

    @bindable(bool)
    def navigational(self) -> bool:
        """
        Whether the ToolbarItem is a navigational item.

        Returns:
            bool: `True` if the ToolbarItem is a navigational item. `False` otherwise.
        """        
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
                 system: Optional[ToolbarItemSystemIdentifier]=None,
                 navigational: Union[bool, AbstractBinding]=False,
                 centered: bool=False) -> None:
        """
        Add a new `ToolbarItem` view, which creates a MacOS native ToolbarItem (MacOS only).
        It must be attached to a `Toolbar`. Example:

        >>> with Toolbar():
                ToolbarItem(label='Settings',
                            action=self.show_settings)

        Args:
            label (Optional[Union[str, AbstractBinding]], optional): The ToolbarItem's label. Defaults to None.
            image (Optional[Union[Image, AbstractBinding]], optional): The ToolbarItem's image. Defaults to None.
            action (Optional[Union[Callable, Coroutine]], optional): The action to be executed when the ToolbarItem is clicked. Defaults to None.
            system (Optional[ToolbarItemSystemIdentifier], optional): The ID of the system-generated ToolbarItem. Defaults to None.
            navigational (Union[bool, AbstractBinding], optional): Whether the ToolbarItem is navigational. Defaults to False.
            centered (bool, optional): Whether the ToolbarItem is centered. Defaults to False.
        """        
        ToolbarItemBase.__init__(self)
        ControlWithLabel.__init__(self, label)
        ImageControl.__init__(self, image)
        Visible.__init__(self)
        Enable.__init__(self)

        self._toolbar_item = None
        self._bordered = True
        self.centered = centered

        if system is not None:
            self._system = True
            self.identifier = system.value
        else:
            self._system = False
            self.action = action

            if isinstance(navigational, AbstractBinding):
                self.bound_navigational = navigational
                self.bound_navigational.on_changed.connect(self._on_navigational_changed)
                self._navigational = navigational.value
            else:
                self._navigational = navigational

    def _on_navigational_changed(self, signal, sender, event):
        self.navigational = self.bound_navigational.value

    def get_ns_object(self) -> NSToolbarItem:
        """
        The toolbar item's NSToolbarItem instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSToolbarItem: the toolbar item's NSToolbarItem instance.
        """
        return self._toolbar_item
    
    def parse(self):
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            ToolbarItem: self
        """
        if not self._system:
            self._toolbar_item = NSToolbarItem.alloc().initWithItemIdentifier_(self.identifier)
            self._toolbar_item.bordered = True
            self._toolbar_item.allowsDuplicatesInToolbar = False

            if self.action:
                self._toolbar_item.target = get_current_app()._controller
                if iscoroutinefunction(self.action):
                    self._toolbar_item.action = \
                        get_current_app().register_async_action(self._toolbar_item, self.action)
                else:
                    self._toolbar_item.action = \
                        get_current_app().register_action(self._toolbar_item, self.action)
        
        ToolbarItemBase.parse(self)
        ImageControl.parse(self, ImageControl)
        ControlWithLabel.parse(self, ControlWithLabel)

        return self
    

class ToolbarItemGroup(ToolbarItem):
    """ Control that generates a native, text based, single selection MacOS ToolbarItemGroup (MacOS only). """

    @bindable(int)
    def selected_index(self) -> int:
        """
        The index of the selected item.
        Databinding: This property supports two-way binding.

        Returns:
            int: The index of the selected item.
        """        
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, val: int) -> None:
        self._selected_index = val
        if self.ns_object and self.ns_object.selectedIndex != val:
            self._toolbar_item.setSelected_atIndex_(True, val)

    def __init__(self, *,
                 labels: List[str],
                 label: Optional[Union[str, AbstractBinding]]=None,
                 action: Optional[Union[Callable, Coroutine]]=None,
                 centered: bool=True) -> None:
        """
        Add a new `ToolbarItemGroup` view which creates a native, text-based, single selection
        MacOS ToolbarItemGroup (MacOS only).

        It must be attached to a `Toolbar`. Example:

        >>> with Toolbar():
                ToolbarItemGroup(labels=['Value1', 'Value2', 'Value3'],
                                 action=self.value_selected)

        To start with one of the groups selected, use the `set_selected_index` modifier:

        >>> with Toolbar():
                ToolbarItemGroup(labels=['Value1', 'Value2', 'Value3'],
                                 action=self.value_selected) \
                    .set_selected_index(0)

        Args:
            labels (List[str]): Labels of the items in the group.
            label (Optional[Union[str, AbstractBinding]], optional): Label of the group. Defaults to None.
            action (Optional[Union[Callable, Coroutine]], optional): Action executed when each of the items in the group is clicked. Defaults to None.
            centered (bool, optional): Whether the group should be centered. Defaults to True.
        """        
        super().__init__(label=label,
                         action=action,
                         centered=centered)

        self._selected_index = -1
        self.bound_selected_index = None
        self.labels = labels
    
    def parse(self):
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            ToolbarItemGroup: self
        """
        self._toolbar_item = \
            NSToolbarItemGroup.groupWithItemIdentifier_titles_selectionMode_labels_target_action_(
                self.identifier,
                self.labels,
                0,
                self.labels,
                get_current_app()._controller,
                None
            )
        
        def set_bound_value():
            if self.bound_selected_index:
                self.bound_selected_index.value = self._toolbar_item.selectedIndex
            else:
                self.selected_index = self._toolbar_item.selectedIndex
        
        def action():
            set_bound_value()
            if self.action:
                return self.action()
            
        async def action_async():
            set_bound_value()
            return await self.action()
        
        if self.action and iscoroutinefunction(self.action):
            self._toolbar_item.setAction(
                get_current_app().register_async_action(self._toolbar_item, action_async)
            )
        else:
            self._toolbar_item.setAction(
                get_current_app().register_action(self._toolbar_item, action)
            )

        ToolbarItemBase.parse(self)
        ImageControl.parse(self, ImageControl)
        ControlWithLabel.parse(self, ControlWithLabel)

        return self
    
    def _on_selected_index_changed(self):
        self.selected_index = self.bound_selected_index.value

    def set_selected_index(self, selected_index: Union[bool, AbstractBinding]):
        """
        Set or bind the ToolbarItemGroup's selected index.

        Args:
            selected_index (Union[bool, AbstractBinding]): Value or bindable.
        """        
        def __modifier():
            if isinstance(selected_index, AbstractBinding):
                self.bound_selected_index = selected_index
                self.bound_selected_index.on_changed.connect(self._on_selected_index_changed)
                self.selected_index = selected_index.value
            else:
                self.selected_index = selected_index

        self._modifiers.append(__modifier)

        return self


class ToolbarSpace(ToolbarItem):
    """ Toolbar item control with `NSToolbarSpaceItem` system identifier (MacOS only). """

    def __init__(self) -> None:
        """
        Add a new `ToolbarSpace` view which generates a ToolbarItem with `NSToolbarSpaceItem` system
        identifier (MacOS only).

        It must be attached to a `Toolbar`. Example:

        >>> with Toolbar():
                ToolbarSpace()
        """        
        super().__init__(system=ToolbarItemSystemIdentifier.space)


class ToolbarFlexibleSpace(ToolbarItem):
    """ Toolbar item control with `NSToolbarFlexibleSpaceItem` system identifier (MacOS only). """

    def __init__(self) -> None:
        """
        Add a new `ToolbarFlexibleSpace` view which generates a ToolbarItem with `NSToolbarFlexibleSpaceItem` system
        identifier (MacOS only).

        It must be attached to a `Toolbar`. Example:

        >>> with Toolbar():
                ToolbarFlexibleSpace()

        It can be used to lay out items in the toolbar:

        >>> with Toolbar(style=ToolbarStyle.unified,
                         display_mode=ToolbarDisplayMode.label_only):
                ToolbarItem(label='Left')
                ToolbarFlexibleSpace()
                ToolbarItem(label='Center')
                ToolbarFlexibleSpace()
                ToolbarItem(label='Right')
        """    
        super().__init__(system=ToolbarItemSystemIdentifier.flexible_space)

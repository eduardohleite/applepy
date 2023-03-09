from applepy.base.types.layout import Orientation
from ...backend import _IOS
from ...base.errors import (
    NotSupportedError,
    AddingMultipleChildrenToNonStackableViewError
)


if _IOS:
    raise NotSupportedError()


from typing import Optional, Union

from ...backend.app_kit import NSBox, NSObject, NSSize
from ...base.types import (
    Color,
    Size,
    BoxType,
    BorderType,
    TitlePosition
)
from ...base.view import StackedView
from ...base.binding import AbstractBinding, bindable
from ...views.controls.control import Control
from ...base.transform_mixins import (
    Width,
    Height,
    TitledControl
)


class DecoratedView(StackedView, 
                    Control,
                    TitledControl,
                    Width,
                    Height):
    """ Control that generates a view container that can be used to separate child controls. """
    
    @bindable(BoxType)
    def box_type(self) -> BoxType:
        """
        Type of the box container.

        Returns:
            BoxType: Type of the box container.
        """        
        return self._box_type

    @box_type.setter
    def box_type(self, val: BoxType) -> None:
        self._box_type = val
        self._box.boxType = val.value

    @bindable(BorderType)
    def border_type(self) -> BorderType:
        """
        Type of the box container's border.

        Returns:
            BorderType: Type of the box container's border.
        """        
        return self._border_type

    @border_type.setter
    def border_type(self, val: BorderType) -> None:
        self._border_type = val
        self._box.borderType = val.value

    @bindable(TitlePosition)
    def title_position(self) -> TitlePosition:
        """
        Position of the box container's title.

        Returns:
            TitlePosition: Position of the box container's title.
        """        
        return self._title_position

    @title_position.setter
    def title_position(self, val: TitlePosition) -> None:
        self._title_position = val
        self._box.titlePosition = val.value

    @bindable(float)
    def corner_radius(self) -> float:
        """
        Radius of the box container's corners.

        Returns:
            float: Radius of the box container's corners.
        """        
        return self._corner_radius

    @corner_radius.setter
    def corner_radius(self, val: float) -> None:
        self._corner_radius = val
        self._box.cornerRadius = val

    @bindable(Color)
    def fill_color(self) -> Color:
        """
        Color to fill container.

        Returns:
            Color: Color to fill container.
        """        
        return self._fill_color

    @fill_color.setter
    def fill_color(self, val: Color) -> None:
        self._fill_color = val
        self._box.fillColor = val.value

    @bindable(Color)
    def border_color(self) -> Color:
        """
        Color of the box container's borders.

        Returns:
            Color: Color of the box container's borders.
        """        
        return self._border_color

    @border_color.setter
    def border_color(self, val: Color) -> None:
        self._border_color = val
        self._box.borderColor = val.value

    @bindable(float)
    def border_width(self) -> float:
        """
        Width of the box container's borders.

        Returns:
            float: Width of the box container's borders.
        """        
        return self._border_width

    @border_width.setter
    def border_width(self, val: float) -> None:
        self._border_width = val
        self._box.borderWidth = val

    @bindable(Size)
    def margin(self) -> Size:
        """
        Margin between border and content.

        Returns:
            Size: Margin between border and content.
        """        
        return self._margin

    @margin.setter
    def margin(self, val: Size) -> None:
        self._margin = val
        self._box.contentViewMargins = NSSize(val.width, val.height)

    def __init__(self,
                 *,
                 title: Optional[Union[str, AbstractBinding]]=None,
                 box_type: BoxType=BoxType.primary,
                 border_type: BorderType=BorderType.line,
                 title_position: TitlePosition=TitlePosition.no_title,
                 corner_radius: float=5.,
                 fill_color: Color=Color.control_background_color,
                 border_color: Color=Color.secondary_label_color,
                 border_width: float=1.,
                 margin: Size=Size(5., 5.)) -> None:
        """
        Add a new `DecoratedView`, which creates a decorated container for separating child controls.
        Controls can be attached to it using a with statement:

        >>> with DecoratedView():
                with VerticalStack():
                    Label(text='Name')
                    TextEdit(text=Binding(ViewModel.name, self.vm))

        Args:
            title (Optional[Union[str, AbstractBinding]], optional): Title of the decorated view. Defaults to None.
            box_type (BoxType, optional): Box type of the decorated view. Defaults to BoxType.primary.
            border_type (BorderType, optional): Border type of the decorated view. Defaults to BorderType.line.
            title_position (TitlePosition, optional): Position of the decorated view's title. Defaults to TitlePosition.no_title.
            corner_radius (float, optional): Radius of the decorated view's corners. Defaults to 5..
            fill_color (Color, optional): Color to fill the decorated view. Defaults to Color.control_background_color.
            border_color (Color, optional): Color of the decorated view's borders. Defaults to Color.secondary_label_color.
            border_width (float, optional): Width of the decorated view's borders. Defaults to 1..
            margin (Size, optional): Margin between the borders and content. Defaults to Size(5., 5.).
        """        
        StackedView.__init__(self)
        Control.__init__(self)
        TitledControl.__init__(self, title)
        Width.__init__(self)
        Height.__init__(self)

        self._box = None
        self.content_view = None

        self._box_type = box_type
        self._border_type = border_type
        self._title_position = title_position
        self._corner_radius = corner_radius
        self._fill_color = fill_color
        self._border_color = border_color
        self._border_width = border_width
        self._margin = margin

    def get_ns_object(self) -> NSBox:
        """
        The container's NSBox instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSBox: the container's NSBox instance.
        """
        return self._box
    
    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            DecoratedView: self
        """
        self._box = NSBox.alloc().init()
        self._box.boxType = self.box_type.value
        self._box.borderType = self.border_type
        self._box.titlePosition = self.title_position
        self._box.cornerRadius = self.corner_radius
        self._box.fillColor = self.fill_color.value
        self._box.borderColor = self.border_color.value
        self._box.borderWidth = self.border_width
        self._box.contentViewMargins = NSSize(self.margin.width, self.margin.height)

        self._box.sizeToFit()

        TitledControl.parse(self, TitledControl)
        Control.parse(self)
        StackedView.parse(self)
        return self
    
    def set_content_view(self, content_view: NSObject) -> None:
        if self.content_view:
            raise AddingMultipleChildrenToNonStackableViewError()
        
        self.content_view = content_view
        self._box.contentView = content_view


class Separator(Control,
                Width,
                Height):
    """ Control that renders an horizontal or vertical separation line. """

    def __init__(self,
                 *,
                 orientation: Orientation=Orientation.horizontal) -> None:
        """
        Add a new `Separator` view, which adds an horizontal or vertical line for control separation.

        Args:
            orientation (Orientation, optional): Separator's orientation. Defaults to Orientation.horizontal.
        """        
        Control.__init__(self)
        Width.__init__(self)
        Height.__init__(self)

        self._box = None
        self.orientation = orientation

    def get_ns_object(self) -> NSBox:
        """
        The separator's NSBox instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSBox: the separator's NSBox instance.
        """
        return self._box
    
    def _add_constraints_to_superview(self):
        if self.orientation == Orientation.vertical:
            padding = 0., 0.

            if isinstance(self.parent, StackedView):
                padding = self._box.superview.edgeInsets.top, self._box.superview.edgeInsets.bottom

            width_constraint = self._box.widthAnchor.constraintEqualToConstant(1)
            width_constraint.active = True
            top_contraint = self._box.topAnchor.constraintEqualToAnchor_constant_(self._box.superview.topAnchor, padding[0])
            top_contraint.active = True
            bottom_contraint = self._box.bottomAnchor.constraintEqualToAnchor_constant_(self._box.superview.bottomAnchor, -padding[1])
            bottom_contraint.active = True

    def parse(self) -> Control:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Separator: self
        """
        self._box = NSBox.alloc().init()
        self._box.boxType = BoxType.separator

        if self.orientation == Orientation.vertical:
            self._box.translatesAutoresizingMaskIntoConstraints = False

        Control.parse(self)
        return self

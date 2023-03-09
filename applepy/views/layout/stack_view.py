from typing import Optional, Union

from ... import StackedView, Alignment, Orientation, StackDistribution
from ...backend import _MACOS, _IOS
from ...base.binding import bindable
from ...base.mixins import Modifiable
from ...base.scene import Scene
from ...base.view import View
from ...base.transform_mixins import (
    BackgroundColor,
    LayoutSpacing,
    LayoutPadding,
    LayoutAlignment
)

if _MACOS:
    from ...backend.app_kit import NSStackView, UIStackView

if _IOS:
    from ...backend.ui_kit import NSStackView, UIStackView


class StackView(StackedView,
                BackgroundColor,
                LayoutSpacing,
                LayoutPadding,
                LayoutAlignment):

    """ Layout view horizontally or vertically in a stack. """

    @bindable(Orientation)
    def orientation(self) -> Orientation:
        """
        Stack layout orientation.
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            StackOrientation: the stack's layout orientation.
        """
        return self._orientation

    @orientation.setter
    def orientation(self, val: Orientation) -> None:
        self._orientation = val
        if self._stack_view:
            self._stack_view.orientation = val.value

    @bindable(StackDistribution)
    def distribution(self) -> StackDistribution:
        """
        Stack layout distribution.
        Data Binding: This property is a read-only bind. Setting this value will have no effect.

        Returns:
            StackDistribution: the stack's layout distribution.
        """
        return self._distribution
    
    @distribution.setter
    def distribution(self, val: StackDistribution) -> None:
        self._distribution = val
        if self._stack_view:
            self._stack_view.distribution = val.value

    def __init__(self, *, orientation: Orientation,
                          alignment: Optional[Alignment]=None,
                          distribution: Optional[StackDistribution]=None) -> None:
        """
        Add a new `StackView` view, which lays out child views in a horizontal or vertical
        stack. Child views can be specified with a `with` statement:

        >>> with StackView(orientation=StackOrientation.vertical):
                Label(text='hello world')

        Stack views can be nested, creating complex layouts:

        >>> with StackView(orientation=StackOrientation.vertical):
                with StackView(orientation=StackOrientation.horizontal):
                    Label(text='row 1 column 1')
                    Label(text='row 1 column 2')
                with StackView(orientation=StackOrientation.horizontal):
                    Label(text='row 2 column 1')
                    Label(text='row 2 column 2')

        If no distribution is set in the initializer, the first stack, that is added as a content view of a `Scene`
        is set to `StackDistribution.fill`. All inner stacks are set to `StackDistribution.gravity_areas`.

        Unless you plan to choose the stack view's orientation programatically, prefer to
        use the shortcut classes `HorizontalStack` and `VerticalStack`.

        Args:
            orientation (StackOrientation): The stack layout orientation.
            alignment (Alignment, optional): The alignment of the stacked views. Defaults to Alignment.left.
            distribution (StackDistribution, optional): The distribution of the stacked views.
        """
        if not alignment:
            if _MACOS:
                alignment = Alignment.macos_left

            if _IOS:
                alignment = Alignment.ios_leading

        StackedView.__init__(self, (Scene, StackedView))
        BackgroundColor.__init__(self)
        LayoutPadding.__init__(self)
        LayoutSpacing.__init__(self)
        LayoutAlignment.__init__(self, default_alignment=alignment)

        self._orientation = orientation
        if not distribution:
            if isinstance(self.parent, Scene):
                self._distribution = StackDistribution.fill
            else:
                self._distribution = StackDistribution.gravity_areas
        else:
            self._distribution = distribution

    def get_ns_object(self) -> Union[NSStackView, UIStackView]:
        """
        The stack view's NSStackView instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSStackView: the stack view's NSStackView instance.
        """
        return self._stack_view

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            StackView: self
        """
        if _MACOS:
            self._stack_view = NSStackView.alloc().init()
            self._stack_view.orientation = self.orientation.value
            self._stack_view.distribution = self.distribution.value
        if _IOS:
            self._stack_view = UIStackView.alloc().init()
            self._stack_view.axis = self.orientation.value
            self._stack_view.distribution = self.distribution.value

        if isinstance(self.parent, StackView):
            self.parent.ns_object.addArrangedSubview_(self.ns_object)
        else:
            self.parent.set_content_view(self.ns_object)

        if isinstance(self.parent, Scene):
            # grab parent
            top_contraint = self._stack_view.topAnchor.constraintEqualToAnchor(self._stack_view.superview.topAnchor)
            top_contraint.active = True
            bottom_contraint = self._stack_view.bottomAnchor.constraintEqualToAnchor(self._stack_view.superview.bottomAnchor)
            bottom_contraint.active = True
            left_contraint = self._stack_view.leftAnchor.constraintEqualToAnchor(self._stack_view.superview.leftAnchor)
            left_contraint.active = True
            right_contraint = self._stack_view.rightAnchor.constraintEqualToAnchor(self._stack_view.superview.rightAnchor)
            right_contraint.active = True
        else:
            self._add_constraints_to_superview()

        StackedView.parse(self)
        LayoutAlignment.parse(self, LayoutAlignment)
        LayoutSpacing.parse(self, LayoutSpacing)
        Modifiable.parse(self)
    
        return self


class HorizontalStack(StackView):
    """ Layout view horizontally in a stack. """

    def __init__(self, *, alignment: Optional[Alignment]=None,
                          distribution: Optional[StackDistribution]=None) -> None:
        """
        Shortcut to create a horizontal StackView.
        Child views can be specified with a `with` statement:

        >>> with HorizontalStack():
                Label(text='hello world')

        Stack views can be nested, creating complex layouts:

        >>> with VerticalStack():
                with HorizontalStack():
                    Label(text='row 1 column 1')
                    Label(text='row 1 column 2')
                with HorizontalStack():
                    Label(text='row 2 column 1')
                    Label(text='row 2 column 2')

        If no distribution is set in the initializer, the first stack, that is added as a content view of a `Scene`
        is set to `StackDistribution.fill`. All inner stacks are set to `StackDistribution.gravity_areas`.

        Args:
            alignment (Alignment, optional): The alignment of the stacked views. Defaults to Alignment.center_y.
            distribution (StackDistribution, optional): The distribution of the stacked views. Defaults to StackDistribution.fill.
        """
        if not alignment:
            if _MACOS:
                alignment = Alignment.macos_center_y

            if _IOS:
                alignment = Alignment.ios_center

        super().__init__(orientation=Orientation.horizontal,
                         alignment=alignment,
                         distribution=distribution)


class VerticalStack(StackView):
    """ Layout view vertically in a stack. """

    def __init__(self, *, alignment: Optional[Alignment]=None,
                          distribution: Optional[StackDistribution]=None) -> None:
        """
        Shortcut to create a vertical StackView.
        Child views can be specified with a `with` statement:

        >>> with VerticalStack():
                Label(text='hello world')

        Stack views can be nested, creating complex layouts:

        >>> with VerticalStack():
                with HorizontalStack():
                    Label(text='row 1 column 1')
                    Label(text='row 1 column 2')
                with HorizontalStack():
                    Label(text='row 2 column 1')
                    Label(text='row 2 column 2')

        If no distribution is set in the initializer, the first stack, that is added as a content view of a `Scene`
        is set to `StackDistribution.fill`. All inner stacks are set to `StackDistribution.gravity_areas`.

        Args:
            alignment (Alignment, optional): The alignment of the stacked views. Defaults to Alignment.center_y.
            distribution (StackDistribution, optional): The distribution of the stacked views. Defaults to StackDistribution.fill.
        """
        if not alignment:
            if _MACOS:
                alignment = Alignment.macos_center_x

            if _IOS:
                alignment = Alignment.ios_center

        super().__init__(orientation=Orientation.vertical,
                         alignment=alignment,
                         distribution=distribution)


class Spacer(View, BackgroundColor):
    """ A Layout view that fills all the remaining space in a stack."""

    def __init__(self) -> None:
        """
        Create a new `Spacer`, which will fill the remaining space in a Stack.
        Can only be used as a child of a StackView.
        Example:
        >>> with VerticalStack():
                Label(text='Top of the stack!')
                Spacer()
                Label(text='Bottom of the stack!')
        """         
        super().__init__((StackedView,))
        self._stack_view = None

    def parse(self) -> View:
        """
        View's parse method.
        It is used internally for rendering the components. Do not call it directly.

        Returns:
            Spacer: self
        """
        if _MACOS:
            self._stack_view = NSStackView.alloc().init()
            self._stack_view.orientation = Orientation.vertical
            self._stack_view.distribution = StackDistribution.fill

        if _IOS:
            self._stack_view = UIStackView.alloc().init()
            self._stack_view.axis = Orientation.vertical
            self._stack_view.distribution = StackDistribution.fill

        self.parent.ns_object.addArrangedSubview_(self.ns_object)
        return super().parse()

    def get_ns_object(self) -> Union[NSStackView, UIStackView]:
        """
        The spacer's NSStackView instance.
        Do not call it directly, use the ns_object property instead.

        Returns:
            NSStackView: the stack view's NSStackView instance.
        """
        return self._stack_view

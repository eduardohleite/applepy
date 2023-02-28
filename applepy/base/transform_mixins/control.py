from typing import Union, Optional, Tuple, Callable

from ...base.types import Color, Image, ImagePosition
from ... import AbstractBinding, bindable
from ...base.utils import try_call
from .base import TransformMixin


class TitledControl(TransformMixin):
    @bindable(str)
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, val: str) -> None:
        self._title = val
        TitledControl._set(self)

    def __init__(self, default_title: Union[str, AbstractBinding]='') -> None:
        if isinstance(default_title, AbstractBinding):
            self.bound_title = default_title
            self.bound_title.on_changed.connect(self._on_title_changed)
            self._title = default_title.value
        else:
            self._title = default_title

    def _on_title_changed(self, signal, sender, event):
        self.title = self.bound_title.value

    def _set(self) -> None:
        if self.ns_object:
            self.ns_object.title = self._title

    def set_title(self, title: Union[str, AbstractBinding]):
        def __modifier():
            if isinstance(title, AbstractBinding):
                self.bound_title = title
                self.bound_title.on_changed.connect(self._on_title_changed)
                self.title = title.value
            else:
                self.title = title

        self._modifiers.append(__modifier)

        return self


class Placeholder(TransformMixin):
    @bindable(str)
    def placeholder(self) -> Optional[str]:
        return self._placeholder

    @placeholder.setter
    def placeholder(self, val: str) -> None:
        self._placeholder = val
        Placeholder._set(self)

    def __init__(self) -> None:
        self._placeholder = None

    def _on_placeholder_changed(self, signal, sender, event):
        self.placeholder = self.bound_placeholder.value

    def _set(self) -> None:
        self.ns_object.placeholderString = self.placeholder

    def set_placeholder(self, placeholder: Union[Optional[str], AbstractBinding]):
        def __modifier():
            if isinstance(placeholder, AbstractBinding):
                self.bound_placeholder = placeholder
                self.bound_placeholder.on_changed.connect(self._on_placeholder_changed)
                self.placeholder = placeholder.value
            else:
                self.placeholder = placeholder

        self._modifiers.append(__modifier)

        return self


class ControlWithState(TransformMixin):
    @bindable(int)
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, val: int) -> None:
        self._state = val
        ControlWithState._set(self)

    def __init__(self, default_state: int=0) -> None:
        self._state = default_state

    def _on_state_changed(self, signal, sender, event):
        self.state = self.bound_state.value

    def _set(self) -> None:
        self.ns_object.state = self._state

    def set_state(self, state: Union[int, AbstractBinding]):
        def __modifier():
            if isinstance(state, AbstractBinding):
                self.bound_state = state
                self.bound_state.on_changed.connect(self._on_state_changed)
                self.state = state.value
            else:
                self.state = state

        self._modifiers.append(__modifier)

        return self


class BezelColor(TransformMixin):
    @bindable(Color)
    def bezel_color(self) -> Color:
        return self._bezel_color

    @bezel_color.setter
    def bezel_color(self, val: Color) -> None:
        self._bezel_color = val
        BezelColor._set(self)

    def __init__(self) -> None:
        self._bezel_color = Color.control_color

    def _on_bezel_color_changed(self, signal, sender, event):
        self.bezel_color = self.bound_bezel_color.value

    def _set(self) -> None:
        self.ns_object.bezelColor = self.bezel_color.value

    def set_bezel_color(self, bezel_color: Union[Color, AbstractBinding]):
        def __modifier():
            if isinstance(bezel_color, AbstractBinding):
                self.bound_bezel_color = bezel_color
                self.bound_bezel_color.on_changed.connect(self._on_bezel_color_changed)
                self.bezel_color = bezel_color.value
            else:
                self.bezel_color = bezel_color

        self._modifiers.append(__modifier)

        return self


class KeyBindable(TransformMixin):
    @bindable(str)
    def key_equivalent(self) -> str:
        return self._key_equivalent

    @key_equivalent.setter
    def key_equivalent(self, val: str) -> None:
        self._key_equivalent = val
        self._set()

    def __init__(self, key_equivalent: Optional[str]=None) -> None:
        self._key_equivalent = key_equivalent

    def _on_key_equivalent_changed(self, signal, sender, event):
        self.key_equivalent = self.bound_key_equivalent.value

    def _set(self) -> None:
        self.ns_object.keyEquivalent = self.key_equivalent or ''

    def set_key_equivalent(self, key_equivalent: Union[str, AbstractBinding]):
        def __modifier():
            if isinstance(key_equivalent, AbstractBinding):
                self.bound_key_equivalent = key_equivalent
                self.bound_key_equivalent.on_changed.connect(self._on_key_equivalent_changed)
                self.key_equivalent = key_equivalent.value
            else:
                self.key_equivalent = key_equivalent

        self._modifiers.append(__modifier)

        return self


class TextColor(TransformMixin):
    @bindable(Color)
    def text_color(self) -> Color:
        return self._text_color

    @text_color.setter
    def text_color(self, val: Color) -> None:
        self._text_color = val
        TextColor._set(self)

    def __init__(self) -> None:
        self._text_color = Color.text_color

    def _on_text_color_changed(self, signal, sender, event):
        self.text_color = self.bound_text_color.value

    def _set(self) -> None:
        self.ns_object.textColor = self.text_color.value

    def set_text_color(self, text_color: Union[Color, AbstractBinding]):
        def __modifier():
            if isinstance(text_color, AbstractBinding):
                self.bound_text_color = text_color
                self.bound_text_color.on_changed.connect(self._on_text_color_changed)
                self.text_color = text_color.value
            else:
                self.text_color = text_color

        self._modifiers.append(__modifier)

        return self


class TextControl(TransformMixin):
    @bindable(str)
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        self._text = val
        TextControl._set(self)

    def __init__(self, text: Union[str, AbstractBinding]='') -> None:
        if isinstance(text, AbstractBinding):
            self.bound_text = text
            self.bound_text.on_changed.connect(self._on_text_changed)
            self._text = text.value
        else:
            self._text = text

    def _on_text_changed(self, signal, sender, event):
        self.text = self.bound_text.value

    def _set(self) -> None:
        if self.ns_object:
            self.ns_object.stringValue = self.text

    def set_text(self, text: Union[str, AbstractBinding]):
        def __modifier():
            if isinstance(text, AbstractBinding):
                self.bound_text = text
                self.bound_text.on_changed.connect(self._on_text_changed)
                self.text = text.value
            else:
                self.text = text

        self._modifiers.append(__modifier)

        return self


class ImageControl(TransformMixin):
    @bindable(Image)
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, val: Image) -> None:
        self._image = val
        ImageControl._set(self)

    @bindable(ImagePosition)
    def image_position(self) -> ImagePosition:
        return self._image_position

    @image_position.setter
    def image_position(self, image_position: ImagePosition) -> None:
        self._image_position = image_position
        ImageControl._set(self)

    def __init__(self, image: Optional[Union[Image, AbstractBinding]]=None,
                       image_position: Optional[Union[ImagePosition, AbstractBinding]]=None,
                       default_image_position: ImagePosition=ImagePosition.no_image,
                       before_set: Optional[Callable]=None) -> None:

        self._default_image_position = default_image_position
        self._before_set = before_set
        image, image_position = self.__compute_image_and_position(image, image_position)

        if isinstance(image, AbstractBinding):
            self.bound_image = image
            self.bound_image.on_changed.connect(self._on_image_changed)
            self._image = image.value
        else:
            self._image = image
        
        if isinstance(image_position, AbstractBinding):
            self.bound_image_position = image_position
            self.bound_image_position.on_changed.connect(self._on_image_position_changed)
            self._image_position = image_position.value
        else:
            self._image_position = image_position

    def __compute_image_and_position(self,
                                     image: Optional[Union[Image, AbstractBinding]],
                                     image_position: Optional[Union[ImagePosition, AbstractBinding]]) \
                                        -> Tuple[Optional[Union[Image, AbstractBinding]],
                                                 Optional[Union[ImagePosition, AbstractBinding]]]:
        if image:
            if not image_position:
                image_position = self._default_image_position
        else:
            if image_position:
                image_position = image_position.no_image

        return image, image_position


    def _on_image_changed(self, signal, sender, event):
        self.image = self.bound_image.value

    def _on_image_position_changed(self, signal, sender, event):
        self.image_position = self.bound_image_position.value

    def _set(self) -> None:
        if self.ns_object and self._image:
            try_call(self._before_set, self._image)
            self.ns_object.image = self._image.value
            self.ns_object.imagePosition = self._image_position.value

    def set_image(self, image: Union[Image, AbstractBinding]='',
                        image_position: Union[ImagePosition, AbstractBinding]=ImagePosition.no_image):
        def __modifier():
            image, image_position = self.__compute_image_and_position(image, image_position)

            if isinstance(image, AbstractBinding):
                self.bound_image = image
                self.bound_image.on_changed.connect(self._on_image_changed)
                self.image = image.value
            else:
                self.image = image
        
            if isinstance(image_position, AbstractBinding):
                self.bound_image_position = image_position
                self.bound_image_position.on_changed.connect(self._on_image_position_changed)
                self.image_position = image_position.value
            else:
                self.image_position = image_position

        self._modifiers.append(__modifier)

        return self

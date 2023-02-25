from enum import Enum

from ...backend.app_kit import NSImage
from ..binding import BindableMixin


class Image(BindableMixin):
    def __init__(self, image: NSImage) -> None:
        self._image = image

    @classmethod
    def from_system(cls, system_name: str):
        return cls(NSImage.imageNamed_(system_name))

    @classmethod
    def from_file(cls, path: str):
        img = NSImage.alloc().initByReferencingFile_(path)
        if img and img.isValid() == 1:
            return cls(img)
        else:
            raise Exception('Invalid image.')

    @property
    def value(self):
        return self._image


class ImagePosition(BindableMixin, Enum):
    no_image = 0
    image_only = 1
    image_leading = 7
    image_trailing = 8
    image_left = 2
    image_right = 3
    image_below = 4
    image_above = 5
    image_overlaps = 6

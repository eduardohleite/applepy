from ...backend.app_kit import NSImage
from ..binding import Bindable


class Image(Bindable):
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

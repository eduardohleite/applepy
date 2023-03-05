from ..backend import _MACOS, _IOS

if _MACOS:
    from .window import Window

if _IOS:
    from .simple_screen import SimpleScreen

from .empty import EmptyScene

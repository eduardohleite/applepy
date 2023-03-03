from ..backend import _MACOS, _IOS

if _MACOS:
    from .window import Window

if _IOS:
    from .view_controller import ViewController

from .empty import EmptyScene

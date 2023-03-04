from ..backend import _MACOS, _IOS

if _MACOS:
    from .menu import (
        Menu,
        MainMenu,
        Submenu,
        MenuItem,
        StatusIcon
    )

    from .feedback import (
        Alert,
        FileDialog,
        OpenDialog,
        SaveDialog
    )

if _IOS:
    from .feedback import Alert

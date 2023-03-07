from enum import Enum

from ..binding import BindableMixin


class ToolbarDisplayMode(Enum):
    default = 0
    icon_and_label = 1
    icon_only = 2
    label_only = 3


class ToolbarStyle(BindableMixin, Enum):
    automatic = 0
    expanded = 1
    preference = 2
    unified = 3
    unified_compact = 4


class ToolbarItemSystemIdentifier(str, Enum):
    print = 'NSToolbarPrintItem'
    fonts = 'NSToolbarShowFontsItem'
    space = 'NSToolbarSpaceItem'
    flexible_space = 'NSToolbarFlexibleSpaceItem'
    cloud_sharing = 'NSToolbarCloudSharingItem'
    colors = 'NSToolbarShowColorsItem'
    toggle_sidebar = 'NSToolbarToggleSidebarItem'
    sidebar_tracking_separator = 'NSToolbarSidebarTrackingSeparatorItem'
    sidebar_tracking_separator_item = 'NSToolbarPrimarySidebarTrackingSeparatorItem'
    supplementary_sidebar_tracking_separator_item = 'NSToolbarSupplementarySidebarTrackingSeparatorItem'

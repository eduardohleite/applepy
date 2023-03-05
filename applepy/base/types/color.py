from typing import Union

from ...base.binding import BindableMixin
from ..errors import NotSupportedError
from ...backend import _IOS, _MACOS

if _MACOS:
    from ...backend.app_kit import NSColor, UIColor

if _IOS:
    from ...backend.ui_kit import NSColor, UIColor


class Color(BindableMixin):
    def __init__(self, value: Union[NSColor, UIColor]) -> None:
        self.value = value

    @classmethod
    def from_rgba(cls, red: float, green: float, blue: float, alpha: float):
        if _MACOS:
            return cls(NSColor.colorWithRed_green_blue_alpha_(red, green, blue, alpha))
        
        if _IOS:
            return cls(UIColor.colorWithRed_green_blue_alpha_(red, green, blue, alpha))

    @classmethod
    def from_hsba(cls, hue: float, saturation: float, brightness: float, alpha: float):
        if _MACOS:
            return cls(NSColor.colorWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha))
        
        if _IOS:
            return cls(UIColor.colorWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha))

    @classmethod
    def from_cmyk(cls, cyan: float, magenta: float, yellow: float, black: float, alpha: float):
        if _MACOS:
            return cls(NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(cyan, magenta, yellow, black, alpha))
        
        if _IOS:
            raise NotSupportedError()

    # Adaptable System Colors
    @classmethod
    @property
    def system_blue(cls):
        if _MACOS:
            return cls(NSColor.systemBlueColor)
        
        if _IOS:
            return cls(UIColor.systemBlueColor())

    @classmethod
    @property
    def system_brown(cls):
        if _MACOS:
            return cls(NSColor.systemBrownColor)
        
        if _IOS:
            return cls(UIColor.systemBrownColor())

    @classmethod
    @property
    def system_gray(cls):
        if _MACOS:
            return cls(NSColor.systemGrayColor)
        
        if _IOS:
            return cls(UIColor.systemGrayColor())
        
    @classmethod
    @property
    def system_cyan(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemCyanColor())

    @classmethod
    @property
    def system_green(cls):
        if _MACOS:
            return cls(NSColor.systemGreenColor)
        
        if _IOS:
            return cls(UIColor.systemGreenColor())

    @classmethod
    @property
    def system_indigo(cls):
        if _MACOS:
            return cls(NSColor.systemIndigoColor)
        
        if _IOS:
            return cls(UIColor.systemIndigoColor())
        
    @classmethod
    @property
    def system_mint(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemMintColor())

    @classmethod
    @property
    def system_orange(cls):
        if _MACOS:
            return cls(NSColor.systemOrangeColor)
        
        if _IOS:
            return cls(UIColor.systemOrangeColor())

    @classmethod
    @property
    def system_pink(cls):
        if _MACOS:
            return cls(NSColor.systemPinkColor)
        
        if _IOS:
            return cls(UIColor.systemPinkColor())

    @classmethod
    @property
    def system_purple(cls):
        if _MACOS:
            return cls(NSColor.systemPurpleColor)
        
        if _IOS:
            return cls(UIColor.systemPurpleColor())

    @classmethod
    @property
    def system_red(cls):
        if _MACOS:
            return cls(NSColor.systemRedColor)
        
        if _IOS:
            return cls(UIColor.systemRedColor())

    @classmethod
    @property
    def system_teal(cls):
        if _MACOS:
            return cls(NSColor.systemTealColor)
        
        if _IOS:
            return cls(UIColor.systemTealColor())

    @classmethod
    @property
    def system_yellow(cls):
        if _MACOS:
            return cls(NSColor.systemYellowColor)
        
        if _IOS:
            return cls(UIColor.systemYellowColor())
        
    # Adaptable Gray Colors (iOS only)
    @classmethod
    @property
    def system_gray2(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemGray2Color())
        
    @classmethod
    @property
    def system_gray3(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemGray3Color())
        
    @classmethod
    @property
    def system_gray4(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemGray4Color())
        
    @classmethod
    @property
    def system_gray5(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemGray5Color())
        
    @classmethod
    @property
    def system_gray6(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemGray6Color())

    # Transparent Color
    @classmethod
    @property
    def system_clear_color(cls):
        if _MACOS:
            return cls(NSColor.systemClearColor)
        
        if _IOS:
            return cls(UIColor.clearColor)

    # Fixed Colors
    @classmethod
    @property
    def black(cls):
        if _MACOS:
            return cls(NSColor.blackColor)
        
        if _IOS:
            return cls(UIColor.blackColor)

    @classmethod
    @property
    def blue(cls):
        if _MACOS:
            return cls(NSColor.blueColor)
        
        if _IOS:
            return cls(UIColor.blueColor)

    @classmethod
    @property
    def brown(cls):
        if _MACOS:
            return cls(NSColor.brownColor)
        
        if _IOS:
            return cls(UIColor.brownColor)

    @classmethod
    @property
    def cyan(cls):
        if _MACOS:
            return cls(NSColor.cyanColor)
        
        if _IOS:
            return cls(UIColor.cyanColor)

    @classmethod
    @property
    def dark_gray(cls):
        if _MACOS:
            return cls(NSColor.darkGrayColor)
        
        if _IOS:
            return cls(UIColor.darkGrayColor)

    @classmethod
    @property
    def gray(cls):
        if _MACOS:
            return cls(NSColor.grayColor)
        
        if _IOS:
            return cls(UIColor.grayColor)

    @classmethod
    @property
    def green(cls):
        if _MACOS:
            return cls(NSColor.greenColor)
        
        if _IOS:
            return cls(UIColor.greenColor)

    @classmethod
    @property
    def light_gray(cls):
        if _MACOS:
            return cls(NSColor.lightGrayColor)
        
        if _IOS:
            return cls(UIColor.lightGrayColor)

    @classmethod
    @property
    def magenta(cls):
        if _MACOS:
            return cls(NSColor.magentaColor)
        
        if _IOS:
            return cls(UIColor.magentaColor)

    @classmethod
    @property
    def orange(cls):
        if _MACOS:
            return cls(NSColor.orangeColor)
        
        if _IOS:
            return cls(UIColor.orangeColor)

    @classmethod
    @property
    def purple(cls):
        if _MACOS:
            return cls(NSColor.purpleColor)
        
        if _IOS:
            return cls(UIColor.purpleColor)

    @classmethod
    @property
    def red(cls):
        if _MACOS:
            return cls(NSColor.redColor)
        
        if _IOS:
            return cls(UIColor.redColor)

    @classmethod
    @property
    def white(cls):
        if _MACOS:
            return cls(NSColor.whiteColor)
        
        if _IOS:
            return cls(UIColor.whiteColor)

    @classmethod
    @property
    def yellow(cls):
        if _MACOS:
            return cls(NSColor.yellowColor)
    
        if _IOS:
            return cls(UIColor.yellowColor)
        
    # Label Colors
    @classmethod
    @property
    def label_color(cls):
        if _MACOS:
            return cls(NSColor.labelColor)
        
        if _IOS:
            return cls(UIColor.labelColor())

    @classmethod
    @property
    def secondary_label_color(cls):
        if _MACOS:
            return cls(NSColor.secondaryLabelColor)
        
        if _IOS:
            return cls(UIColor.secondaryLabelColor())

    @classmethod
    @property
    def tertiary_label_color(cls):
        if _MACOS:
            return cls(NSColor.tertiaryLabelColor)
        
        if _IOS:
            return cls(UIColor.tertiaryLabelColor())

    @classmethod
    @property
    def quaternary_label_color(cls):
        if _MACOS:
            return cls(NSColor.quaternaryLabelColor)
        
        if _IOS:
            return cls(UIColor.quaternaryLabelColor())
        
    # Fill Colors (iOS only)
    @classmethod
    @property
    def system_fill_color(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.systemFillColor())
        
    @classmethod
    @property
    def secondary_system_fill_color(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.secondarySystemFillColor())
        
    @classmethod
    @property
    def tertiary_system_fill_color(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.tertiarySystemFillColor())
        
    @classmethod
    @property
    def quaternary_system_fill_color(cls):
        if _MACOS:
            raise NotSupportedError()
        
        if _IOS:
            return cls(UIColor.quaternarySystemFillColor())

    # Text Colors
    @classmethod
    @property
    def text_color(cls):
        if _MACOS:
            return cls(NSColor.textColor)
        
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def placeholder_text_color(cls):
        if _MACOS:
            return cls(NSColor.placeholderTextColor)

        if _IOS:
            return cls(UIColor.placeholderTextColor())

    @classmethod
    @property
    def selected_text_color(cls):
        if _MACOS:
            return cls(NSColor.selectedTextColor)
    
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def text_background_color(cls):
        if _MACOS:
            return cls(NSColor.textBackgroundColor)
    
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def selected_text_background_color(cls):
        if _MACOS:
            return cls(NSColor.selectedTextBackgroundColor)
    
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def keyboard_focus_indicator_color(cls):
        if _MACOS:
            return cls(NSColor.keyboardFocusIndicatorColor)
    
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def unemphasized_selected_text_color(cls):
        if _MACOS:
            return cls(NSColor.unemphasizedSelectedTextColor)
    
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def unemphasized_selected_text_background_color(cls):
        if _MACOS:
            return cls(NSColor.unemphasizedSelectedTextBackgroundColor)
    
        if _IOS:
            raise NotSupportedError()
        
    # Tint Colors (iOS Only)
    @classmethod
    @property
    def tint_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.tintColor())
        
    # Standard Control Background Colors (iOS Only)
    @classmethod
    @property
    def system_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.systemBackgroundColor())
        
    @classmethod
    @property
    def secundary_system_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.secondarySystemBackgroundColor())
        
    @classmethod
    @property
    def tertiary_system_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.tertiarySystemBackgroundColor())
        
    # Grouped Content Background Colors (iOS Only)
    @classmethod
    @property
    def system_grouped_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.systemGroupedBackgroundColor())
        
    @classmethod
    @property
    def secondary_system_grouped_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.secondarySystemGroupedBackgroundColor())
        
    @classmethod
    @property
    def tertiary_system_grouped_background_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.tertiarySystemGroupedBackgroundColor())
        
    # Separator Colors (iOS Only)
    @classmethod
    @property
    def separator_color(cls):
        if _MACOS:
            return cls(NSColor.separatorColor)
    
        if _IOS:
            return cls(UIColor.separatorColor())
        
    @classmethod
    @property
    def opaque_separator_color(cls):
        if _MACOS:
            raise NotSupportedError()
    
        if _IOS:
            return cls(UIColor.opaqueSeparatorColor())

    # Content Colors
    @classmethod
    @property
    def link_color(cls):
        if _MACOS:
            return cls(NSColor.linkColor)
        
        if _IOS:
            return cls(UIColor.linkColor())

    @classmethod
    @property
    def selected_content_background_color(cls):
        if _MACOS:
            return cls(NSColor.selectedContentBackgroundColor)
        
        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def unemphasized_selected_content_background_color(cls):
        if _MACOS:
            return cls(NSColor.unemphasizedSelectedContentBackgroundColor)

        if _IOS:
            raise NotSupportedError()

    # Menu Colors (MacOS Only)
    @classmethod
    @property
    def selected_menu_item_text_color(cls):
        if _MACOS:
            return cls(NSColor.selectedMenuItemTextColor)

        if _IOS:
            raise NotSupportedError()

    # Table Colors (MacOS Only)
    @classmethod
    @property
    def grid_color(cls):
        if _MACOS:
            return cls(NSColor.gridColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def header_text_color(cls):
        if _MACOS:
            return cls(NSColor.headerTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def alternating_content_background_colors(cls):
        if _MACOS:
            return cls(NSColor.alternatingContentBackgroundColors)

        if _IOS:
            raise NotSupportedError()

    # Control Colors (MacOS Only)
    @classmethod
    @property
    def control_accent_color(cls):
        if _MACOS:
            return cls(NSColor.controlAccentColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def control_color(cls):
        if _MACOS:
            return cls(NSColor.controlColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def control_background_color(cls):
        if _MACOS:
            return cls(NSColor.controlBackgroundColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def control_text_color(cls):
        if _MACOS:
            return cls(NSColor.controlTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def disabled_control_text_color(cls):
        if _MACOS:
            return cls(NSColor.disabledControlTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def current_control_tint(cls):
        if _MACOS:
            return cls(NSColor.currentControlTint)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def selected_control_color(cls):
        if _MACOS:
            return cls(NSColor.selectedControlColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def selected_control_text_color(cls):
        if _MACOS:
            return cls(NSColor.selectedControlTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def alternate_selected_control_text_color(cls):
        if _MACOS:
            return cls(NSColor.alternateSelectedControlTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def scrubber_textured_background_color(cls):
        if _MACOS:
            return cls(NSColor.scrubberTexturedBackgroundColor)

        if _IOS:
            raise NotSupportedError()

    # Window Colors (MacOS Only)
    @classmethod
    @property
    def window_background_color(cls):
        if _MACOS:
            return cls(NSColor.windowBackgroundColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def window_frame_text_color(cls):
        if _MACOS:
            return cls(NSColor.windowFrameTextColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def under_page_background_color(cls):
        if _MACOS:
            return cls(NSColor.underPageBackgroundColor)

        if _IOS:
            raise NotSupportedError()

    # Highlights and Shadows (MacOS Only)
    @classmethod
    @property
    def find_hightlight_color(cls):
        if _MACOS:
            return cls(NSColor.findHighlightColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def highlight_color(cls):
        if _MACOS:
            return cls(NSColor.highlightColor)

        if _IOS:
            raise NotSupportedError()

    @classmethod
    @property
    def shadow_color(cls):
        if _MACOS:
            return cls(NSColor.shadowColor)

        if _IOS:
            raise NotSupportedError()

    # Nonadaptable Colors (iOS Only)
    @classmethod
    @property
    def dark_text_color(cls):
        if _MACOS:
            raise NotSupportedError()

        if _IOS:
            return cls(UIColor.darkTextColor())
        
    @classmethod
    @property
    def light_text_color(cls):
        if _MACOS:
            raise NotSupportedError()

        if _IOS:
            return cls(UIColor.lightTextColor())

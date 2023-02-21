from ...base.binding import BindableMixin
from ...backend.app_kit import NSColor


class Color(BindableMixin):
    def __init__(self, value: NSColor) -> None:
        self.value = value

    @classmethod
    def from_rgba(cls, red: float, green: float, blue: float, alpha: float):
        return cls(NSColor.colorWithRed_green_blue_alpha_(red, green, blue, alpha))

    @classmethod
    def from_hsba(cls, hue: float, saturation: float, brightness: float, alpha: float):
        return cls(NSColor.colorWithHue_saturation_brightness_alpha_(hue, saturation, brightness, alpha))

    @classmethod
    def from_cmyk(cls, cyan: float, magenta: float, yellow: float, black: float, alpha: float):
        return cls(NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(cyan, magenta, yellow, black, alpha))

    # Adaptable System Colors
    @classmethod
    @property
    def system_blue(cls):
        return cls(NSColor.systemBlueColor)

    @classmethod
    @property
    def system_brown(cls):
        return cls(NSColor.systemBrownColor)

    @classmethod
    @property
    def system_gray(cls):
        return cls(NSColor.systemGrayColor)

    @classmethod
    @property
    def system_green(cls):
        return cls(NSColor.systemGreenColor)

    @classmethod
    @property
    def system_indigo(cls):
        return cls(NSColor.systemIndigoColor)

    @classmethod
    @property
    def system_orange(cls):
        return cls(NSColor.systemOrangeColor)

    @classmethod
    @property
    def system_pink(cls):
        return cls(NSColor.systemPinkColor)

    @classmethod
    @property
    def system_purple(cls):
        return cls(NSColor.systemPurpleColor)

    @classmethod
    @property
    def system_red(cls):
        return cls(NSColor.systemRedColor)

    @classmethod
    @property
    def system_teal(cls):
        return cls(NSColor.systemTealColor)

    @classmethod
    @property
    def system_yellow(cls):
        return cls(NSColor.systemYellowColor)

    # Transparent Color
    @classmethod
    @property
    def system_clear_color(cls):
        return cls(NSColor.systemClearColor)

    # Fixed Colors
    @classmethod
    @property
    def black(cls):
        return cls(NSColor.blackColor)

    @classmethod
    @property
    def blue(cls):
        return cls(NSColor.blueColor)

    @classmethod
    @property
    def brown(cls):
        return cls(NSColor.brownColor)

    @classmethod
    @property
    def cyan(cls):
        return cls(NSColor.cyanColor)

    @classmethod
    @property
    def dark_gray(cls):
        return cls(NSColor.darkGrayColor)

    @classmethod
    @property
    def gray(cls):
        return cls(NSColor.grayColor)

    @classmethod
    @property
    def green(cls):
        return cls(NSColor.greenColor)

    @classmethod
    @property
    def light_gray(cls):
        return cls(NSColor.lightGrayColor)

    @classmethod
    @property
    def magenta(cls):
        return cls(NSColor.magentaColor)

    @classmethod
    @property
    def orange(cls):
        return cls(NSColor.orangeColor)

    @classmethod
    @property
    def purple(cls):
        return cls(NSColor.purpleColor)

    @classmethod
    @property
    def red(cls):
        return cls(NSColor.redColor)

    @classmethod
    @property
    def white(cls):
        return cls(NSColor.whiteColor)

    @classmethod
    @property
    def yellow(cls):
        return cls(NSColor.yellowColor)
        
    # Label Colors
    @classmethod
    @property
    def label_color(cls):
        return cls(NSColor.labelColor)

    @classmethod
    @property
    def secondary_label_color(cls):
        return cls(NSColor.secondaryLabelColor)

    @classmethod
    @property
    def tertiary_label_color(cls):
        return cls(NSColor.tertiaryLabelColor)

    @classmethod
    @property
    def quaternary_label_color(cls):
        return cls(NSColor.quaternaryLabelColor)

    # Text Colors

    @classmethod
    @property
    def text_color(cls):
        return cls(NSColor.textColor)

    @classmethod
    @property
    def placeholder_text_color(cls):
        return cls(NSColor.placeholderTextColor)

    @classmethod
    @property
    def selected_text_color(cls):
        return cls(NSColor.selectedTextColor)

    @classmethod
    @property
    def text_background_color(cls):
        return cls(NSColor.textBackgroundColor)

    @classmethod
    @property
    def selected_text_background_color(cls):
        return cls(NSColor.selectedTextBackgroundColor)

    @classmethod
    @property
    def keyboard_focus_indicator_color(cls):
        return cls(NSColor.keyboardFocusIndicatorColor)

    @classmethod
    @property
    def unemphasized_selected_text_color(cls):
        return cls(NSColor.unemphasizedSelectedTextColor)

    @classmethod
    @property
    def unemphasized_selected_text_background_color(cls):
        return cls(NSColor.unemphasizedSelectedTextBackgroundColor)

    # Content Colors
    @classmethod
    @property
    def link_color(cls):
        return cls(NSColor.linkColor)

    @classmethod
    @property
    def separator_color(cls):
        return cls(NSColor.separatorColor)

    @classmethod
    @property
    def selected_content_background_color(cls):
        return cls(NSColor.selectedContentBackgroundColor)

    @classmethod
    @property
    def unemphasized_selected_content_background_color(cls):
        return cls(NSColor.unemphasizedSelectedContentBackgroundColor)

    # Menu Colors
    @classmethod
    @property
    def selected_menu_item_text_color(cls):
        return cls(NSColor.selectedMenuItemTextColor)

    # Table Colors
    @classmethod
    @property
    def grid_color(cls):
        return cls(NSColor.gridColor)

    @classmethod
    @property
    def header_text_color(cls):
        return cls(NSColor.headerTextColor)

    @classmethod
    @property
    def alternating_content_background_colors(cls):
        return cls(NSColor.alternatingContentBackgroundColors)

    # Control Colors
    @classmethod
    @property
    def control_accent_color(cls):
        return cls(NSColor.controlAccentColor)

    @classmethod
    @property
    def control_color(cls):
        return cls(NSColor.controlColor)

    @classmethod
    @property
    def controlBackgroundColor(cls):
        return cls(NSColor.controlBackgroundColor)

    @classmethod
    @property
    def control_text_color(cls):
        return cls(NSColor.controlTextColor)

    @classmethod
    @property
    def disabled_control_text_color(cls):
        return cls(NSColor.disabledControlTextColor)

    @classmethod
    @property
    def current_control_tint(cls):
        return cls(NSColor.currentControlTint)

    @classmethod
    @property
    def selected_control_color(cls):
        return cls(NSColor.selectedControlColor)

    @classmethod
    @property
    def selected_control_text_color(cls):
        return cls(NSColor.selectedControlTextColor)

    @classmethod
    @property
    def alternate_selected_control_text_color(cls):
        return cls(NSColor.alternateSelectedControlTextColor)

    @classmethod
    @property
    def scrubber_textured_background_color(cls):
        return cls(NSColor.scrubberTexturedBackgroundColor)

    # Window Colors
    @classmethod
    @property
    def window_background_color(cls):
        return cls(NSColor.windowBackgroundColor)

    @classmethod
    @property
    def window_frame_text_color(cls):
        return cls(NSColor.windowFrameTextColor)

    @classmethod
    @property
    def under_page_background_color(cls):
        return cls(NSColor.underPageBackgroundColor)

    # Highlights and Shadows
    @classmethod
    @property
    def find_hightlight_color(cls):
        return cls(NSColor.findHighlightColor)

    @classmethod
    @property
    def highlight_color(cls):
        return cls(NSColor.highlightColor)

    @classmethod
    @property
    def shadow_color(cls):
        return cls(NSColor.shadowColor)

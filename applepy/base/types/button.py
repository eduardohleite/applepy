from enum import Enum


class ButtonStyle(Enum):
    # Creates a configuration for a button with a transparent background.
    plain = 0

    # Creates a configuration for a button with a gray background.
    gray = 1

    # Creates a configuration for a button with a tinted background color.
    tinted = 2

    # Creates a configuration for a button with a background filled with the button’s tint color.
    filled = 3

    # Creates a configuration for a button that has a borderless style.
    borderless = 4
    
    # Creates a configuration for a button that has a bordered style.
    bordered = 5

    # Creates a configuration for a button that has a tinted, bordered style.
    bordered_tinted = 6

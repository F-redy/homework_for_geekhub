COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'orange': '\033[31;2m',
    'blue': '\033[34m',
    'violet': '\033[35m',
    'light_blue': '\033[36m',
    'drop_color': '\033[0m'
}


class UnsupportedColorError(ValueError):
    pass


def colorize_text(text: str, color: str) -> str:
    """
    The function paints the input text in the specified color.

    Available colors:
    - 'green'     : Green color
    - 'red'       : Red color
    - 'yellow'    : Yellow color
    - 'blue'      : Blue color
    - 'violet'    : Violet color
    - 'light_blue': Light blue color
    """
    if color in COLORS:
        return f"{COLORS[color]}{text}{COLORS['drop_color']}"
    else:
        raise UnsupportedColorError(f'Don\'t have color: {color}')

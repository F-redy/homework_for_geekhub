# task 1.
# Програма-світлофор.
#    Створити програму-емулятор світлофора для авто і пішоходів.
#    Після запуска програми на екран виводиться в лівій половині - колір автомобільного,
#    а в правій - пішохідного світлофора. Кожну 1 секунду виводиться поточні кольори.
#    Через декілька ітерацій - відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах
#    (пішоходам зелений тільки коли автомобілям червоний).
#    Приблизний результат роботи наступний:
#       Red        Green
#       Red        Green
#       Red        Green
#       Red        Green
#       Yellow     Red
#       Yellow     Red
#       Green      Red
#       Green      Red
#       Green      Red
#       Green      Red
#       Yellow     Red
#       Yellow     Red
#       Red        Green


from time import sleep

SETTINGS = {
    'padding between text': 15,
    'headers text': f'CAR {"":^16}PEOPLE'
}

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


class UnsupportedColorError(Exception):
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


def get_colors():
    return [colorize_text(color.capitalize(), color) for color in ['red', 'green', 'yellow']]


def print_colors(car_color: str, people_color: str, repeat: int = 4, timer_sleep: int = 1) -> None:
    """
    :param car_color: traffic light color for cars
    :param people_color: traffic light color for people
    :param repeat: Number of times to repeat the print.
    :param timer_sleep: Sleep duration between prints.

    """
    __padding = SETTINGS['padding between text']

    for _ in range(repeat):
        print(f'{car_color:<{__padding}}{"":>{__padding}}'
              f'{people_color}')
        sleep(timer_sleep)


def traffic_light():
    """
    Simulates a traffic light sequence by printing colored lines representing the traffic light state.

    The sequence consists of the following steps:
    1. Cars: Red -> People: Green; default (repeated four times)
    2. Cars: Yellow -> People: Red (repeated twice)
    3. Cars: Green -> People: Red; default (repeated four times)

    The function uses the colors defined in the `get_colors` function and sets the padding between text based on
    the value stored in SETTINGS['padding between text'].

    This function provides a visual representation of a traffic light sequence with specified sleep durations between
    each step.

    Example:
    traffic_light()
    """
    red, green, yellow = get_colors()

    print_colors(red, green)
    print_colors(yellow, red, repeat=2)
    print_colors(green, red)
    print_colors(yellow, red, repeat=2)
    print_colors(red, green, repeat=1)


def crossroads(repeat: int = 1):
    """
    Simulates a traffic light sequence at a crossroads with a specified number of repetitions.

    This func prints a header text followed by a series of traffic light sequences, simulating a crossroads scenario.
    The traffic light sequence is defined by the 'traffic_light' function.

    :param repeat: Number of times to repeat the traffic light sequence at the crossroads.
    """
    print(f'{SETTINGS["headers text"]}'
          f'\n{"-" * len(SETTINGS["headers text"])}')
    while repeat:
        traffic_light()
        repeat -= 1


if __name__ == '__main__':
    crossroads()

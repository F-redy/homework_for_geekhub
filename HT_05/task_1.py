# task 1.
# Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та яка буде повертати пору року,
# якiй цей мiсяць належить (зима, весна, лiто або осiнь).
# У випадку некоректного введеного значення - виводити відповідне повідомлення.


from HT_05.common import colorize_text, UnsupportedColorError

SEASONS = {
    f'{colorize_text("Зима", "blue")}': (1, 2, 3),
    f'{colorize_text("Весна", "green")}': (4, 5, 6),
    f'{colorize_text("Лето", "light_blue")}': (7, 8, 9),
    f'{colorize_text("Осень", "yellow")}': (10, 11, 12)
}


class NumberOutOfRangeError(ValueError):
    pass


def check_number(number):
    if number not in range(1, 13):
        raise NumberOutOfRangeError(f'\n{colorize_text("The number must be in the range from 1 to 12!", "red")}')


def season(month_number: int) -> str:
    check_number(user_input)
    for month, numbers in SEASONS.items():
        if month_number in numbers:
            return month


if __name__ == '__main__':
    result = None

    try:
        user_input = int(input('Enter the month number (from 1 to 12): '))
        result = season(user_input)
    except ValueError:
        print(f'\n{colorize_text("The number must be an integer", "red")}')
    except NumberOutOfRangeError as out_of_range:
        print(out_of_range)
    except UnsupportedColorError as error_color:
        print('\nContact the development department')

    if result:
        print(f'\nThis month refers to the time of year: {result}')

# task 3.
# Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями.
# Створiть просту умовну конструкцiю (звiсно вона повинна бути в тiлi ф-цiї),
# пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" та у випадку нервіності - виводити ще і різницю.
#     Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
#     x > y;       вiдповiдь - "х бiльше нiж у на z"
#     x < y;       вiдповiдь - "у бiльше нiж х на z"
#     x == y.      вiдповiдь - "х дорiвнює z"


def check_numeric(value: str) -> int | float | None:
    try:
        result = int(value)
    except ValueError:
        try:
            result = float(value)
        except ValueError:
            result = None

    return result


def get_correct_input(text_input: str, error_message: str) -> int | float:
    user_input = check_numeric(input(text_input))

    while type(user_input) not in (int, float):
        user_input = check_numeric(input(error_message))

    return user_input


def comparison(x: int, y: int) -> str:
    a, b = max(x, y), min(x, y)
    if a != b:
        return f'{a} больше чем {b} на {a - b}'

    return f'{a} равняется {b}'


if __name__ == '__main__':
    _x = get_correct_input('Enter a numeric for x: ', '\nInvalid input! \nEnter a numeric for x: ')
    _y = get_correct_input('Enter a numeric for y: ', '\nInvalid input! \nEnter a numeric for y: ')

    print(comparison(_x, _y))

# task 5.
# Ну і традиційно - калькулятор
# Повинна бути 1 ф-цiя, яка б приймала 3 аргументи - один з яких операцiя, яку зробити!
# Аргументи брати від юзера (можна по одному - 2, окремо +, окремо 2; можна всі разом - типу 1 + 2).
# Операції що мають бути присутні: +, -, *, /, %, //, **.


from HT_05.common import colorize_text

# OPERATIONS = {
#     '+': '__add__',
#     '-': '__sub__',
#     '*': '__mul__',
#     '/': '__truediv__',
#     '%': '__mod__',
#     '//': '__floordiv__',
#     '**': '__pow__',
# } # Проблема с разно типовыми переменными a: int  b: float

OPERATIONS = ('+', '-', '*', '/', '%', '//', '**')

INFO = f'\nHello! This is a light version of the calculator...' \
       f'\nPlease stick to simple rules:\n' \
       f'\nAllowed operations: {" | ".join(OPERATIONS)}' \
       f'\n{colorize_text("Correct", "green")} typing format: {colorize_text("1 + 2", "green")}' \
       f'\n{colorize_text("Incorrect", "red")} typing format: {colorize_text("9/3 | 1- 1 | 2 *3", "red")}\n'

MIN_POWER = -1000
MAX_POWER = 1000


def has_three_parts(string: str) -> bool:
    return len(string.split()) == 3


def check_type(values: tuple) -> bool:
    return all(val is not None for val in values)


def get_operation(operation: str) -> str | None:
    return (None, operation)[operation in OPERATIONS]
    # return OPERATIONS.get(operation)


def get_numeric(value: str) -> int | float | None:
    error_message = colorize_text('Invalid input! Values must be int or float', "red")

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            print(error_message)
            return None


def parse_expression(string: str) -> tuple:
    if has_three_parts(string):
        value_a, operation, value_b = string.split()

        num_1 = get_numeric(value_a)
        num_2 = get_numeric(value_b)
        operation = get_operation(operation)

        return num_1, num_2, operation

    print(colorize_text('Incorrect input!', 'red'))
    return None, None, None


def validate_input(string: str) -> tuple | None:
    expression = parse_expression(string)

    if check_type(expression):
        num_1, num_2, operation = expression

        if operation == "**":
            error_message = f'Error input for ** operation!MAX_POWER = {MAX_POWER - 1} and MIN_POWER = {MIN_POWER + 1}'

            if MIN_POWER < num_1 < MAX_POWER and MIN_POWER < num_2 < MAX_POWER:
                return num_1, num_2, operation
            else:
                print(f'{colorize_text(error_message, "red")}')
                return None

        return num_1, num_2, operation
    return None


def get_user_input() -> tuple[int | float, int | float, str]:
    correct_msg = f'{colorize_text("enter", "light_blue")} math expression: '

    while True:
        user_input = input(correct_msg).strip()
        data = validate_input(user_input)

        if data:
            return data


def get_result_expression(num1: int | float, num2: int | float, operation: str) -> int | float:
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        result = num1 / num2
    elif operation == '%':
        result = num1 % num2
    elif operation == '//':
        result = num1 // num2
    elif operation == '**':
        result = num1 ** num2

    return result
    # return getattr(num1, operation)(num2)


def calculator() -> None:
    print(INFO)
    a, b, value_op = get_user_input()

    try:
        result = get_result_expression(a, b, value_op)
        print(f'\n{a} {value_op} {b} = {result}')
        # print(f'\n{a} {OPERATIONS[value_op]} {b} = {result}')

    except ZeroDivisionError:
        print(f'{colorize_text("Zero Division Error!", "red")}')


if __name__ == '__main__':
    # print(eval(input())) :)
    calculator()

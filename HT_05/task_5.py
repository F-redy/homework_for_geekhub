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


MIN_POWER = -1000
MAX_POWER = 1000

OPERATIONS = ('+', '-', '*', '/', '%', '//', '**')

INFO = f'\nHello! This is a light version of the calculator...' \
       f'\nPlease stick to simple rules:\n' \
       f'\nAllowed operations: {" | ".join(OPERATIONS)}' \
       f'\n{colorize_text("Correct", "green")} typing format: {colorize_text("1 + 2", "green")}' \
       f'\n{colorize_text("Incorrect", "red")} typing format: {colorize_text("9/3 | 1- 1 | 2 *3", "red")}\n'

MESSAGES = {
    'int or float': colorize_text('Invalid input! Values must be int or float', "red"),
    'incorrect': colorize_text('Incorrect input!', 'red'),
    '**': f'Error input for ** operation!MAX_POWER = {MAX_POWER - 1} and MIN_POWER = {MIN_POWER + 1}',
    'correct message': f'{colorize_text("enter", "light_blue")} math expression: ',
    'error operation': colorize_text('Invalid operation. Enter one of the available operations.', 'red'),
    'zero': f'{colorize_text("Zero Division Error!", "red")}'

}


def has_three_parts(string: str) -> bool:
    return len(string.split()) == 3


def check_type(values: tuple) -> bool:
    return all(val is not None for val in values)


def get_operation(operation: str) -> str | None:
    return (None, operation)[operation in OPERATIONS]
    # return OPERATIONS.get(operation)


def check_numeric(value: str) -> int | float:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            raise


def parse_expression(string: str) -> tuple:
    num_1 = num_2 = operation = None

    if has_three_parts(string):
        value_a, operation, value_b = string.split()

        try:
            num_1 = check_numeric(value_a)
            num_2 = check_numeric(value_b)
            operation = get_operation(operation)
        except ValueError:
            error_message = colorize_text('Invalid input! Values must be int or float', "red")
            print(error_message)
            return num_1, num_2, operation

        return num_1, num_2, operation

    print(colorize_text('Incorrect input!', 'red'))
    return num_1, num_2, operation


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


def calculator(num1: int | float, num2: int | float, operation: str) -> None:
    if operation == '+':
        print(f'\n{num1 + num2 = }')
    elif operation == '-':
        print(f'\n{num1 - num2 = }')
    elif operation == '*':
        print(f'\n{num1 * num2 = }')
    elif operation == '/':
        print(f'\n{num1 / num2 = }')
    elif operation == '%':
        print(f'\n{num1 % num2 = }')
    elif operation == '//':
        print(f'\n{num1 // num2 = }')
    elif operation == '**':
        if MIN_POWER < num1 < MAX_POWER and MIN_POWER < num2 < MAX_POWER:
            print(f'\n{num1 ** num2 = }')
        else:
            print(MESSAGES['**'])

    else:
        print(MESSAGES['error operation'])

    # return getattr(num1, operation)(num2)


# def task_5() -> None:
#     print(INFO)
#     a, b, value_op = get_user_input()
#
#     try:
#         result = get_result_expression(a, b, value_op)
#         print(f'\n{a} {value_op} {b} = {result}')
#         # print(f'\n{a} {OPERATIONS[value_op]} {b} = {result}')
#
#     except ZeroDivisionError:
#         print(f'{colorize_text("Zero Division Error!", "red")}')


if __name__ == '__main__':
    # print(eval(input())) :)
    # task_5()
    print(INFO)

    a = b = value_op = None

    while True:
        user_input = input(MESSAGES['correct message']).strip()
        data = validate_input(user_input)

        if data:
            a, b, value_op = data
            break

    try:
        res = calculator(a, b, value_op)
        print(f'\n{a} {value_op} {b} = {res}')
    except ZeroDivisionError:
        print(MESSAGES['zero'])
    # a, b, value_op = parse_expression
    #
    # try:
    #     result = get_result_expression(a, b, value_op)
    #     print(f'\n{a} {value_op} {b} = {result}')
    #     # print(f'\n{a} {OPERATIONS[value_op]} {b} = {result}')
    #
    # except ZeroDivisionError:
    #     print(f'{colorize_text("Zero Division Error!", "red")}')

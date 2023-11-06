# task 5.
# Ну і традиційно - калькулятор
# Повинна бути 1 ф-цiя, яка б приймала 3 аргументи - один з яких операцiя, яку зробити!
# Аргументи брати від юзера (можна по одному - 2, окремо +, окремо 2; можна всі разом - типу 1 + 2).
# Операції що мають бути присутні: +, -, *, /, %, //, **.


from HT_05.common import colorize_text

OPERATIONS = ['+', '-', '*', '/', '%', '//', '**']

CORRECT_EXPRESSION = ' | '.join([f"1 {op} 2" for op in OPERATIONS])

INFO = f'\nHello! This is a light version of the calculator...' \
       f'\nPlease stick to simple rules:\n' \
       f'\n{colorize_text("Correct", "green")} typing format: {CORRECT_EXPRESSION}' \
       f'\n{colorize_text("Incorrect", "red")} typing format: {colorize_text("9/3 | 1- 1 | 2 *3", "red")}\n'


class InvalidPowerOperationError(Exception):
    """
        Исключение, возникающее при попытке выполнить операцию возведения в степень
        с неверными параметрами.
    """
    pass


class IncorrectInputError(Exception):
    """
        Исключение, возникающее при неверном формате математического выражения.
        Возникает, если выражение не соответствует ожидаемому формату.
    """
    pass


class InvalidOperatorError(Exception):
    """
        Исключение, возникающее при попытке выполнить операцию с недопустимым оператором.
        Возникает, если оператор не является одним из допустимых (например, "+", "-", "*", и так далее).
    """
    pass


class Calculator:
    MIN_POWER = -1000
    MAX_POWER = 1000

    def __init__(self, num_1, operator, num_2):
        self.__check_inputs(num_1, num_2, operator)
        self.num1 = self.__get_numeric(num_1)
        self.num2 = self.__get_numeric(num_2)
        self.operator = self.__get_operator(operator)
        self.result = self.__calculate()

    def __str__(self):
        return str(self.result)

    @staticmethod
    def __check_inputs(a, b, op):
        for value in [a, b, op]:
            if value is None:
                raise IncorrectInputError(f'Invalid input! {value} none must be None.')

    @staticmethod
    def __get_numeric(value) -> int | float:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                raise TypeError(f'Invalid input! Value "{value}" must be int or float')

    @staticmethod
    def __get_operator(operation: str) -> str:
        if operation in OPERATIONS:
            return operation
        raise InvalidOperatorError(f'Invalid operator! Enter one of the available operations. '
                                   f'Allowed operations: {" | ".join(OPERATIONS)}')

    def __calculate(self) -> int | float:
        calc_dict = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '%': lambda a, b: a % b,
            '//': lambda a, b: a // b,
            '**': lambda a, b: a ** b,
        }

        if self.operator == '**':
            if not (Calculator.MIN_POWER < self.num1 < Calculator.MAX_POWER or
                    Calculator.MIN_POWER < self.num2 < Calculator.MAX_POWER):
                raise InvalidPowerOperationError(f'Error input for ** operation! '
                                                 f'MAX_POWER = {Calculator.MAX_POWER - 1} '
                                                 f'and MIN_POWER = {Calculator.MIN_POWER + 1}')

        return calc_dict.get(self.operator)(self.num1, self.num2)


if __name__ == '__main__':
    print(INFO)
    while True:
        try:
            user_input = input(
                f'\nAllowed operations: {" | ".join(OPERATIONS)}\nenter math expression: ').strip().split()
            result = Calculator(*user_input).result
            if result:
                print(f'\n{" ".join(user_input)} = {result}')

        except ZeroDivisionError as zero:
            print(f'\n{colorize_text(f"Error: {zero}", "red")}')
        except InvalidPowerOperationError as power:
            print(f'\n{colorize_text(f"Error: {power}", "red")}')
        except InvalidOperatorError as error_operator:
            print(f'\n{colorize_text(f"Error: {error_operator}", "red")}')
        except IncorrectInputError as incorrect_input:
            print(f'\n{colorize_text(f"Error: {incorrect_input}", "red")}')
        except TypeError as type_error:
            print(f'\n{colorize_text(f"Error: {str(type_error)[22:]}", "red")}')
        except KeyboardInterrupt:
            print('\n\napp finished working')
            break

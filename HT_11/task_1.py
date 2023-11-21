# 1. Створити клас Calc, який буде мати атребут last_result та 4 методи.
# Методи повинні виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, ділення.
# - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення.
# - Якщо використати один з методів - last_result повенен повернути результат виконання ПОПЕРЕДНЬОГО методу.
#     Example:
#     last_result --> None
#     1 + 1
#     last_result --> None
#     2 * 3
#     last_result --> 2
#     3 * 4
#     last_result --> 6
#     ...
# - Додати документування в клас (можете почитати цю статтю:
# https://realpython.com/documenting-python-code/ )

class Calc:
    """
       Простой калькулятор для выполнения арифметических операций и отслеживания последнего результата вызова метода.
    """

    def __init__(self):
        self.__pre_last_result = None
        self.last_result = None

    def __change_last_result(self, result: int | float) -> None:
        """
        Приватный метод для обновления предыдущего и последнего результатов вычислений.

        Args:
            result (int | float): Результат вызова одного из методов класса.

        Returns: None
        """
        self.last_result = self.__pre_last_result
        self.__pre_last_result = result

    def add(self, num1: int | float, num2: int | float) -> int | float:
        """
        Складывает два числа num1 и num2.

        Args:
            num1 (float or int): Первое число.
            num2 (float or int): Второе число.

        Returns:
            float: Результат сложения num1 и num2.
        """
        result = num1 + num2
        self.__change_last_result(result)
        return result

    def sub(self, num1: int | float, num2: int | float) -> int | float:
        """
        Вычитает число num1 из числа num2.

        Args:
            num1 (float or int): Число, из которого вычитается.
            num2 (float or int): Число, которое вычитается.

        Returns:
            (float or int): Результат вычитания num1 из num2.
        """
        result = num1 - num2
        self.__change_last_result(result)
        return result

    def mul(self, num1: int | float, num2: int | float) -> int | float:
        """
        Умножает число num1 на число num2.

        Args:
            num1 (float or int): Первое число.
            num2 (float or int): Второе число.

        Returns:
            (float or int): Результат умножения num1 на num2.
        """
        result = num1 * num2
        self.__change_last_result(result)

        return result

    def div(self, num1: int | float, num2: int | float) -> float | None:
        """
        Делит число num1 на число b.

        Args:
            num1 (float or int): Делимое число.
            num2 (float or int): Делитель.

        Returns:
            float or None: Результат деления num1 на num2, или None, если y равно 0.
        """
        try:
            result = num1 / num2
        except ZeroDivisionError as e:
            result = str(e)
        self.__change_last_result(result)
        return result


if __name__ == '__main__':
    obj = Calc()
    example_case = [
        (obj.add, 1, 1),
        (obj.sub, 2, 3),
        (obj.mul, 3, 4),
        (obj.div, 5, 0),
        (obj.add, 7, 12)
    ]
    print(f'0. {obj.last_result = }')
    for indx, (func, _num1, _num2) in enumerate(example_case, start=1):
        func(_num1, _num2)
        print('-' * 38)
        print(f'{indx}. {obj.last_result = }')

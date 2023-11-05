from calculator import (Calculator, InvalidOperatorError,
                        InvalidPowerOperationError)

test_data = [
    # верные данные
    ([1, '+', 2], 3),
    ([1, '-', 2], -1),
    ([1, '*', 2], 2),
    ([1, '/', 2], 0.5),
    ([1, '%', 2], 1),
    ([1, '//', 2], 0),
    ([1, '**', 2], 1),
    # неверные данные, ожидается исключение
    ([1, '+', 'abc'], TypeError),  # Ожидаем TypeError из-за неверного второго операнда
    ([1, '^', 2], InvalidOperatorError),  # Ожидаем InvalidOperatorError из-за неверного оператора
    ([1000, '**', 2000], InvalidPowerOperationError),  # Ожидаем InvalidPowerOperationError из-за превышения лимита
    (['one', '+', 2], TypeError),  # Ожидаем ValueError из-за неверного первого операнда
]

if __name__ == '__main__':
    print('\nTEST FOR Calculator')
    for indx, (data, answer) in enumerate(test_data):
        try:
            result = Calculator(*data).result
        except Exception as e:
            assert isinstance(e, answer), f'ERROR: Expected {answer}, but got {type(e)}'
            print(f'TEST №{indx + 1:<3} - OK: Raised expected error - {e}')
        else:
            assert result == answer, f'TEST №{indx + 1} - ERROR!\n{result} != {answer}\nERROR in:\n {data}'
            print(f'TEST №{indx + 1:<3} - OK: Result = {result}')

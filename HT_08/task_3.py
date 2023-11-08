# task 3.
# Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
# Тобто щоб її можна було використати у вигляді:
#     for i in my_range(1, 10, 2):
#         print(i)
#     1
#     3
#     5
#     7
#     9
#    P.S. Повинен вертатись генератор.
#    P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній:
#    https://docs.python.org/3/library/stdtypes.html#range
#    P.P.P.S Не забудьте обробляти невалідні ситуації (аналог range(1, -10, 5)).
#    Подивіться як веде себе стандартний range в таких випадках.

def are_values_integers(*args):
    if any(type(value) is not int for value in args):
        raise TypeError('Values must be int!')


def custom_range(stop: int, start: int = None, step: int = 1):
    if step == 0:
        raise ValueError("Step cannot be zero")

    if stop is not None and start is not None:
        start, stop = stop, start
    else:
        start, stop = 0, stop

    are_values_integers(start, stop, step)

    if (start < stop and step < 0) or (start > stop and step > 0):
        return

    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step


if __name__ == '__main__':
    tests = [
        [(1, 10, 2), [1, 3, 5, 7, 9]],
        [(1, -10, -1), [1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9]],
        [(10,), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        [(10, 2), []],
        [(-5,), []],
        [(5, 21), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
        [(17, 105, 0), ValueError],
        [(17, 1.5), TypeError],
    ]
    for indx, (example, answer) in enumerate(tests):
        try:
            result = list(custom_range(*example))
        except Exception as e:
            assert isinstance(e, answer), f'ERROR: Expected {answer}, but got {type(e)}'
            print(f'TEST №{indx + 1:<3} - OK: Raised expected error - {e}')
        else:
            assert result == answer, f'TEST №{indx + 1} - ERROR!\n{result} != {answer}\nERROR in:\n {example}'
            print(f'TEST №{indx + 1:<3} - OK: Result = {result}')

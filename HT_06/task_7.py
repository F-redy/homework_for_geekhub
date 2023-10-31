# task 7.
# Написати функцію, яка приймає на вхід список (через кому),
# підраховує кількість однакових елементів у ньомy і виводить результат.
# Елементами списку можуть бути дані будь-яких типів.
#     Наприклад:
#     1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"


def count_same(*args) -> None:
    elements = {}
    for elem in args:
        elements[str(elem)] = elements.get(str(elem), 0) + 1

    print(', '.join([f'{key} -> {value}' for key, value in elements.items()]))


if __name__ == '__main__':
    count_same(1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2])

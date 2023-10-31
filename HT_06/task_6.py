# task 6.
# Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку.
# Тобто функція приймає два аргументи: список і величину зсуву
# (якщо ця величина додатня - пересуваємо з кінця на початок, якщо від'ємна - навпаки
# - пересуваємо елементи з початку списку в його кінець).
#    Наприклад:
#    fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
#    fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]

def cyclic_shift(list_items: list, shift: int) -> list:
    if not list_items:
        return list_items

    shift %= len(list_items)

    if shift > 0:
        rotated = list_items[-shift:] + list_items[:-shift]
    else:
        rotated = list_items[shift:] + list_items[:shift]

    return rotated


if __name__ == '__main__':
    print(cyclic_shift([1, 2, 3, 4, 5], shift=1))
    print(cyclic_shift([1, 2, 3, 4, 5], shift=-2))
    print(cyclic_shift([], shift=7))

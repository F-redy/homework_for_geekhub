# task 1.
# Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата,
# і вертатиме 3 значення у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ.

def square(side: int) -> tuple:
    perimeter = side * 4
    area = side ** 2
    diagonal = round(side * (2 ** 0.5), 2)
    return perimeter, area, diagonal


if __name__ == '__main__':
    print(square(side=4))

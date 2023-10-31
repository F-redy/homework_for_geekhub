# task 5.
# Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його.


def fibonacci(number: int) -> None:
    f1, f2 = 1, 1
    for _ in range(1, n + 1):
        if f1 > number:
            return
        print(f1, end=' ')
        f1, f2 = f2, f1 + f2


if __name__ == '__main__':
    n = 35
    fibonacci(n)

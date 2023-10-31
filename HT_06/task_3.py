# task 3.
# Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, и яка вертатиме True,
# якщо це число просте і False - якщо ні.


def is_prime(number: int) -> bool:
    if number <= 1:
        return False

    for num in range(2, int(number ** 0.5) + 1):
        if number % num == 0:
            return False
    return True


if __name__ == '__main__':
    for i in range(1001):
        print(f'{i:<5}| {is_prime(i)}')

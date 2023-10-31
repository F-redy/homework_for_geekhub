# task 4.
# Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона,
# і вертатиме список простих чисел всередині цього діапазона.
# Не забудьте про перевірку на валідність введених даних та у випадку невідповідності - виведіть повідомлення.


from HT_06.task_3 import is_prime


def get_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise TypeError(f'Invalid input: "{value}"! Value must be integer!')


def prime_list(start: int, end: int) -> list[int]:
    return list(filter(is_prime, range(start, end + 1)))


if __name__ == '__main__':
    try:
        user_start = get_int(input('Enter start of range: '))
        user_end = get_int(input('Enter end of range: '))
    except TypeError as e:
        print(e)
    else:
        print('List of prime numbers:', prime_list(user_start, user_end), sep='\n')

# Write a script which accepts a sequence of comma-separated numbers
# from user and generate a list and a tuple with those numbers.


def get_list_digits(string_digits: str, separator: str = ',') -> list[int]:
    try:
        return list(map(int, string_digits.split(separator)))
    except ValueError:
        raise ValueError(f'Values must be numbers. Separator must be "{separator}"')


user_input = input()
list_digits = get_list_digits(user_input)
tuple_digits = tuple(get_list_digits(user_input))

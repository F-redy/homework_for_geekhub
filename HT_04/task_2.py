# task 2.
# Create a custom exception class called NegativeValueError.
# Write a Python program that takes an integer as input and raises the NegativeValueError if the input is negative.
# Handle this custom exception with a try/except block and display an error message.


class NegativeValueError(Exception):
    pass


def check_negative(value: int):
    if value < 0:
        raise NegativeValueError('Negative values are not allowed')


try:
    num = int(input('Enter an integer: '))
    check_negative(num)
except ValueError as e:
    print(e)
except NegativeValueError as e:
    print(e)

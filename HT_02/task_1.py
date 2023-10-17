"""
    Write a script which accepts a sequence of comma-separated numbers
    from user and generate a list and a tuple with those numbers.
"""

user_input = input()
list_digits = user_input.split(',')
tuple_digits = tuple(list_digits)

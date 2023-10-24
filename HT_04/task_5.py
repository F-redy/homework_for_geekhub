# task 5.
# Create a Python program that repeatedly prompts the user for a number until a valid integer is provided.
# Use a try/except block to handle any ValueError exceptions,
# and keep asking for input until a valid integer is entered.
# Display the final valid integer.


def is_integer(value: str):
    try:
        return int(value)
    except ValueError:
        return value


user_input = input('Enter integer number: ')
while isinstance(is_integer(user_input), str):
    user_input = input('Error input!\nEnter integer number: ')

print(f'\nValid value: {user_input}')

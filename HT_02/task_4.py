# Write a script which accepts a <number> from user and then <number> times asks user for string input.
# At the end script must print out result of concatenating all <number> strings.


def concatenate_strings(user_data: list[str]) -> str:
    return ''.join(user_data)


user_input = int(input('Enter number: '))
data = [input(f'Enter string №{i + 1}: ') for i in range(user_input)]

print(concatenate_strings(data))

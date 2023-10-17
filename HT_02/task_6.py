# Write a script to check whether a value from user input is contained in a group of values.
# e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
#      [1, 2, 'u', 'a', 4, True] --> 5 --> False


def check_value_in_group(value: str, group: list) -> bool:
    return value in map(str, group)


user_value = input('Enter the search value: ')
group_values = [1, 2, 'u', 'a', 4, True]

print(check_value_in_group(user_value, group_values))

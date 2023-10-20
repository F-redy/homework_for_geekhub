# 1. Write a script that will run through a list of tuples and replace the last value for each tuple.
# The list of tuples can be hardcoded. The "replacement" value is entered by user.
# The number of elements in the tuples must be different.


from random import randint

random_number_tuples = [tuple(randint(0, 100) for _ in range(randint(3, 7))) for _ in range(randint(5, 10))]
print(f'Started list:\n{random_number_tuples}\n')

user_value = int(input('Enter the number to replace: '))

random_number_tuples = [tuple(t[:-1] + (user_value,)) for t in random_number_tuples if t]

print(f'\nChanged list:\n{random_number_tuples}')

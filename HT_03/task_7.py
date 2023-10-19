# 7. Write a script which accepts a <number> from user and
# generates dictionary in range <number> where key is <number> and value is <number>*<number>
#     e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}


user_input = int(input('Enter number: '))
dictionary_numbers = {num: num * num for num in range(user_input + 1)}

print(dictionary_numbers)

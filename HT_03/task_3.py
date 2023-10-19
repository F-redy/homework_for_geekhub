# 3. Write a script to concatenate following dictionaries to create a new one.
#     dict_1 = {'foo': 'bar', 'bar': 'buz'}
#     dict_2 = {'dou': 'jones', 'USD': 36}
#     dict_3 = {'AUD': 19.2, 'name': 'Tom'}


dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}

# Python 3.9 +
new_dict_3_9 = dict_1 | dict_2 | dict_3
print(f'{new_dict_3_9 = }')

# Python < 3.9
new_dict_older = dict()
new_dict_older.update(dict_1)
new_dict_older.update(dict_2)
new_dict_older.update(dict_3)

new_dict_older_short = {**dict_1, **dict_2, **dict_3}

print(f'{new_dict_older = }')
print(f'{new_dict_older_short = }')

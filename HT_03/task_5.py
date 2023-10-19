# 5. Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.


from copy import deepcopy

original_dictionary = {'foo': 'bar',
                       'bar': 'buz',
                       'name': 'Tom',
                       'dou': 'jones',
                       'USD': 36,
                       'AUD': 19.2,
                       'buz': 'bar',
                       'admin': 'Tom',
                       }

temporary_dictionary = dict()

for key, value in original_dictionary.items():
    if value not in temporary_dictionary.values():
        temporary_dictionary[key] = value

original_dictionary = deepcopy(temporary_dictionary)

print(original_dictionary)

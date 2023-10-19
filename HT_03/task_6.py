# 6. Write a script to get the maximum and minimum value in a dictionary.

dictionary = {
    'id': 17,
    'name': 'NoName',
    'freeze': -35,
    'count': 1,
    'admin': False,
    'errors': [400, 403],
    'email': None,
    'salary': 3750,
    'speed': 75.8,
    'file': 100644,
}

values = list(filter(lambda value: type(value) in (int, float), dictionary.values()))

if values:
    min_value, max_value = min(values), max(values)
    print(f'{min_value = }\n{max_value = }')  # min: -35 max: 100644
else:
    print("The dictionary doesn't contain numbers")

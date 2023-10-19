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

print(f'min = {min(values, default=0)}\nmax = {max(values, default=0)}')

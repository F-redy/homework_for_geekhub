"""
    Write a script to concatenate all elements in a list into a string and print it.
    List must be include both strings and integers and must be hardcoded.
"""

DATA = [
    'Brittney', 60, 'red', None, 'dog',
    46, "Roberttown", 0.5, True, 'Michael',
    3, "Davidstad", 2.0, 'Matthew'
]


def concatenated_list() -> str:
    return ''.join(list(map(str, DATA)))


print(concatenated_list())

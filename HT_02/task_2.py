"""
    Write a script which accepts two sequences of comma-separated colors from user.
    Then print out a set containing all the colors from color_list_1 which are not present in color_list_2.
"""


def find_colors_not_in_second_list(color_list_1: set[str], color_list_2: set[str]) -> str:
    return ' '.join(color_list_1 - color_list_2).strip()


count_color_lists = 2
list_1, list_2 = (set(input().split(',')) for _ in range(count_color_lists))

print(find_colors_not_in_second_list(list_1, list_2))

# task 2.
# Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів.
# Файл також додайте в репозиторій. На екран повинен вивестись список із трьома блоками - символи з початку,
# із середини та з кінця файлу. Кількість символів в блоках - та, яка введена в другому параметрі.
# Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі або, наприклад,
# файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?).
# Не забудьте додати перевірку чи файл існує.


import os

ROOTPATH = os.path.dirname(os.path.abspath(__file__))


def check_path(path_to_file):
    if not os.path.isfile(path_to_file):
        raise FileNotFoundError(f"Error: File '{path_to_file}' not found!")


def check_type(value, type_value: type):
    if not isinstance(value, type_value):
        raise TypeError(f'Type {value} does not match with {type_value}!')


def is_length_below_limit(text_chars: str, limit: int) -> bool:
    return len(text_chars) < limit


def check_data(path_to_file, count_chars):
    """Check the validity of data for file processing"""
    try:
        check_type(path_to_file, str)
        check_type(count_chars, int)
        check_path(path_to_file)
    except TypeError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    else:
        return True


def check_length():
    ...


def calculate_mid_positions(content: str, count_chars):
    """Calculate start and end positions for the middle block of characters."""

    mid = int(len(content) / 2)
    start = int(mid - count_chars / 2)
    end = start + count_chars

    return start, end


def get_middle(content, count_chars):
    start_position, end_position = calculate_mid_positions(content, count_chars)

    return content[start_position:end_position]


def custom_reader(path_to_file: str, block_size: int) -> list | None:
    """
    Read a custom block of characters from a file.

    :param path_to_file: The path to the file.
    :param block_size : The number of characters for the block.
    :return: List containing the start, middle, and end blocks of characters, or None if data is invalid.
    """

    if not check_data(path_to_file, block_size):
        return

    with open(path_to_file, encoding='utf-8') as f:
        file_content = f.read()

    if is_length_below_limit(file_content, block_size):
        print(f'Chars into file is less than {block_size}!')
        return [[]] * 3

    start = file_content[:block_size]
    middle = get_middle(file_content, block_size)
    end = file_content[-block_size:]

    return [start, middle, end]


if __name__ == '__main__':
    file = r"example_txt.txt"
    for count_ch in [20, 5, 10, 700, 2]:
        print('-' * 80)
        print(f'result block of characters:\n{custom_reader(file, count_ch)}')

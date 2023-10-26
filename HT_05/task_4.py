# task 4.
# Наприклад маємо рядок -->
# "f98neroi4nr0c3n30irn03ien3c0rfe  kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345"
# -> просто потицяв по клавi =)
#    Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
# -  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
# -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
# -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)


from HT_05.common import colorize_text

MIN_LENGTH = 30
MAX_LENGTH = 50


def get_count_letters(string: str) -> list[str]:
    return [char for char in string if char.isalpha()]


def get_count_digits(string: str) -> list[str]:
    return [char for char in string if char.isdigit()]


def get_info_string(string: str) -> None:
    letters = get_count_letters(string)
    digits = get_count_digits(string)

    if MIN_LENGTH <= len(string) <= MAX_LENGTH:
        print(f'\nLength string = {len(string)}'
              f'\nCount letters in string = {len(letters)}'
              f'\nCount digits in string = {len(digits)}')

    elif len(string) < MIN_LENGTH:
        empty_msg = "миші з'їли"

        print(f'\nCount digits in string = {sum(map(int, digits))}'
              f'\nLetters from string: {"".join(letters) if letters else empty_msg}')

    else:
        part_1 = colorize_text('УКРА', 'blue')
        part_2 = colorize_text('ЇНИ', 'yellow')

        print(f'Доброго вечора! Мы з {part_1}{part_2}')


if __name__ == '__main__':
    user_string = input('Enter some string (try to enter more than 50 characters): ')
    get_info_string(user_string)

# task 1.
# Написати скрипт, який приймає від користувача два числа (int або float) і робить наступне:

#   a. Кожне введене значення спочатку пробує перевести в int.
#   У разі помилки - пробує перевести в float, а якщо і там ловить помилку - пропонує ввести значення ще раз
#   (зручніше на даному етапі навчання для цього використати цикл while)

#   b. Виводить результат ділення першого на друге.
#   Якщо при цьому виникає помилка - оброблює її і виводить відповідне повідомлення


def is_numeric(value: str) -> int | float | str:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError as e:
            return str(e)


def get_correct_input(variable_name: str) -> int | float:
    user_input = None

    while type(user_input) not in (int, float):
        user_input = is_numeric(input(f'Enter a numeric for {variable_name}: '))
        if isinstance(user_input, str):
            print(f'Error input: {user_input}')

    return user_input


a = get_correct_input('a')
b = get_correct_input('b')

try:
    print(f'\nDivision result: {a} / {b} = {round(a / b, 3)}')
except ZeroDivisionError:
    print('\nZero Division Error')

# task 2.
# Створiть 3 рiзних функцiї (на ваш вибiр).
# Кожна з цих функцiй повинна повертати якийсь результат (напр. інпут від юзера, результат математичної операції тощо).
# Також створiть четверту ф-цiю, яка всередині викликає 3 попереднi, обробляє їх результат
# та також повертає результат своєї роботи.
# Таким чином ми будемо викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3.


from datetime import datetime

YEAR: int = datetime.now().year
MIN_AGE = 0


def check_name(string: str) -> bool:
    return len(string) < 2 or any(map(str.isdigit, string))


def check_age(age: str) -> bool:
    try:
        age = int(age)
        return MIN_AGE < age < YEAR
    except ValueError:
        pass
    return False


def get_count_letter(letters: str) -> str:
    if not isinstance(letters, str):
        raise TypeError(f'{letters} must be string')

    return ' | '.join([f'{letter} - {letters.lower().count(letter)}'
                       for letter in set(letters.lower())])


def get_user_name() -> str:
    name = input('Enter your name: ')

    while check_name(name):
        name = input('It is not real name...\nPlease enter correct name: ')

    return name


def get_user_age() -> int:
    age = input('Enter your age(integer): ')

    while not check_age(age):
        age = input('Invalid input!\nPlease enter an integer corresponding to your age: ')

    return int(age)


def get_data_info(user_name: str, age: int) -> str:
    if not isinstance(user_name, str):
        raise TypeError(f'{user_name} must be string!')

    if type(age) != int:
        raise TypeError(f'{age} must be int!')

    letters: str = get_count_letter(user_name)
    birth_date: int = YEAR - age

    return f'\n{user_name.capitalize()} - a little beat info about your name:' \
           f'\nlength your name = {len(user_name)}' \
           f'\nletters in your name: \n{letters}' \
           f'\nYour were birth in {birth_date}'


def get_user_info():
    user_name = get_user_name()
    user_age = get_user_age()
    return get_data_info(user_name, user_age)


if __name__ == '__main__':
    print(get_user_info())

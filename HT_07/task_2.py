# task 2.
# Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
#    - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
#    - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
#    цифру;
#    - якесь власне додаткове правило :)
#    Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.


MIN_LENGTH_USERNAME = 3
MAX_LENGTH_USERNAME = 50
MIN_LENGTH_PASSWORD = 8
MIN_LETTERS_PASSWORD = 3


class UserNameTooShortError(Exception):
    pass


class UserNameTooLongError(Exception):
    pass


class PasswordTooShortError(Exception):
    pass


class PasswordMissingDigitError(Exception):
    pass


class PasswordMissingLettersError(Exception):
    pass


def validate_min_username_length(username: str) -> bool:
    if len(username) < MIN_LENGTH_USERNAME:
        raise UserNameTooShortError(f'Error: "{username}" short username length! Minimum length: {MIN_LENGTH_USERNAME}')

    return True


def validate_max_username_length(username: str) -> bool:
    if len(username) > MAX_LENGTH_USERNAME:
        raise UserNameTooLongError(f'Error: "{username}"'
                                   f' long username length! Maximum length username: {MAX_LENGTH_USERNAME}')

    return True


def validate_length_password(password: str) -> bool:
    if len(password) < MIN_LENGTH_PASSWORD:
        raise PasswordTooShortError(f'Error: "{password}"'
                                    f' password is short! Minimum password length: {MIN_LENGTH_PASSWORD}')

    return True


def has_password_digit(password: str) -> bool:
    if not any(map(str.isdigit, password)):
        raise PasswordMissingDigitError(f'Error: "{password}"'
                                        f' password must contain at least one number!')

    return True


def has_password_letters(password: str) -> bool:
    if len(list(filter(str.isalpha, password))) < MIN_LETTERS_PASSWORD:
        raise PasswordMissingLettersError(f'Error: "{password}"'
                                          f' password must contain at least {MIN_LETTERS_PASSWORD} letters!')

    return True


def validate_username(username: str) -> bool:
    return validate_min_username_length(username) and validate_max_username_length(username)


def validate_password(password: str) -> bool:
    return validate_length_password(password) and has_password_digit(password) and has_password_letters(password)


def validate_credentials(username: str, password: str) -> bool:
    is_username = validate_username(username)
    is_password = validate_password(password)

    return is_username and is_password

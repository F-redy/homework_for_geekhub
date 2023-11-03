# task 3.
# На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
#    а) створити список із парами ім'я/пароль різноманітних видів
#    (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
#    б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором,
#    перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, наприклад:
#       Name: vasya
#       Password: wasd
#       Status: password must have at least one digit
#       -----
#       Name: vasya
#       Password: vasyapupkin2000
#       Status: OK
#    P.S. Не забудьте використати блок try/except ;)


MIN_LENGTH_USERNAME = 3
MAX_LENGTH_USERNAME = 50
MIN_LENGTH_PASSWORD = 8
MIN_LETTERS_PASSWORD = 3


class LoginException(Exception):
    pass


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


def login(username: str, password: str, silent: bool = False) -> bool:
    users = {
        'bob': 'cP9R@il0!r',
        'neal': '4V^XIdj*@v',
        'sean': 'h+0TA3xW05',
        'jonathan': 'o%tex5PrXL',
        'carriesawyercarriesawyercarriesawyercarriesawyer50': '@$0tZgh0jc',

    }
    validate_username(username)
    validate_password(password)

    response = users.get(username) == password

    if not response and not silent:
        raise LoginException('Authorisation Error')

    return response


def print_login_status(username: str, password: str, silent: bool = False) -> None:
    try:
        result = login(username, password, silent)
    except (LoginException, PasswordMissingDigitError,
            PasswordMissingLettersError, PasswordTooShortError,
            UserNameTooLongError, UserNameTooShortError) as e:
        result = e
    finally:
        print(f'-----\nName: {username}')
        print(f'Password: {password}')
        print(f'Status: {(result, "OK")[type(result) == bool]}')


if __name__ == '__main__':

    tests_users = [
        {'username': 'bob', 'password': 'cP9R@il0!r'},  # True
        {'username': 'carriesawyercarriesawyercarriesawyercarriesawyer50', 'password': '@$0tZgh0jc'},  # True
        {'username': 'neal', 'password': '4V^XIdj*@v'},  # True
        {'username': 'sean', 'password': 'h+0TA3xW05'},  # True
        {'username': 'jonathan', 'password': 'o%tex5PrXL'},  # True
        {'username': 'doby', 'password': 'qwerty12', 'silent': True},  # False
        {'username': 'opps', 'password': '&yUQ$0u85s'},  # LoginException
        {'username': 'td', 'password': '1a3b5c7d'},  # UserNameTooShortError
        {'username': 'carriesawyercarriesawyercarriesawyercarriesawyerl51',
         'password': '@$0tZgh0jc'},  # UserNameTooLongError
        {'username': 'owright', 'password': 'S2bFxR+'},  # PasswordTooShortError
        {'username': 'heathergreer', 'password': '!x%wOQvFnj'},  # PasswordMissingDigitError
        {'username': 'heathergreer', 'password': '12345678'},  # PasswordMissingLettersError
    ]

    for user in tests_users:
        print_login_status(*user.values())

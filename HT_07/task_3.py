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


from HT_07.task_1 import LoginException, login
from HT_07.task_2 import (PasswordMissingDigitError,
                          PasswordMissingLettersError, PasswordTooShortError,
                          UserNameTooLongError, UserNameTooShortError)


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

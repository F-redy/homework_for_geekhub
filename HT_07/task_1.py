# task 1.
# Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
# Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>)
# і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
# Логіка наступна:
#     якщо введено коректну пару ім'я/пароль - вертається True;
#     якщо введено неправильну пару ім'я/пароль:
#     якщо silent == True - функція вертає False
#     якщо silent == False -породжується виключення LoginException (його також треба створити =))


from HT_07.task_2 import validate_credentials


class LoginException(Exception):
    pass


def login(username: str, password: str, silent: bool = False) -> bool:
    users = [
        {'username': 'bob', 'password': 'cP9R@il0!r'},
        {'username': 'neal', 'password': '4V^XIdj*@v'},
        {'username': 'sean', 'password': 'h+0TA3xW05'},
        {'username': 'jonathan', 'password': 'o%tex5PrXL'},
        {'username': 'carriesawyercarriesawyercarriesawyercarriesawyer50', 'password': '@$0tZgh0jc'},
    ]
    validate_credentials(username, password)

    for user in users:
        if user['username'] == username and user['password'] == password:
            return True

    if not silent:
        raise LoginException('Authorisation Error')

    return False

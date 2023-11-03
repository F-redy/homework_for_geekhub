# task 1.
# Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
# Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>)
# і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
# Логіка наступна:
#     якщо введено коректну пару ім'я/пароль - вертається True;
#     якщо введено неправильну пару ім'я/пароль:
#     якщо silent == True - функція вертає False
#     якщо silent == False -породжується виключення LoginException (його також треба створити =))


from HT_07.task_2 import validate_password, validate_username


class LoginException(Exception):
    pass


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

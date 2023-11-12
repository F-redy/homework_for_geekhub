from HT_09.task_3 import settings
from HT_09.task_3.users.view import authenticate_user, register_user


def login() -> dict | None:
    attempts = settings.ATTEMPTS
    attempts_break = settings.ATTEMPTS
    request = {'attempts': attempts, 'attempts_break': attempts_break}

    while attempts and attempts_break:
        print('\nАвторизація')
        username = input("Введіть ім'я користувача: ")
        password = input('Введіть пароль: ')
        request = authenticate_user(request, username, password)
        attempts, attempts_break = request['attempts'], request['attempts_break']

        if request['user']:
            print(request['authenticate'])
            return request['user']

        print(request['message'])


def registration():
    while True:
        print('\nРеєстрація')
        username = input("Введіть ім'я користувача: ")
        password = input('Введіть пароль: ')

        user = register_user(username, password)

        if user:
            return user

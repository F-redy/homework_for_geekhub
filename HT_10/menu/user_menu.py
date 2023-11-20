from HT_10.menu.custom_exceptions import ValidationError
from HT_10.menu.utils import get_user_choose_menu, withdrawal_user_balance
from HT_10.menu.validators import is_integer
from HT_10.users.views import (authenticate_user, change_user_balance,
                               register_user)


class UserMenu:
    MENU = [
        '\nВыберите действие:',
        '1. Авторизация',
        '2. Регистрация',
        '3. Выход\n',
    ]

    USER_MENU = [
        '\nВыберите действие:',
        '1. Проверить баланс',
        '2. Пополнить баланс',
        '3. Снять средства',
        '4. Выход\n',
    ]

    @staticmethod
    def login(connect) -> dict:
        user = None
        while user is None:
            entered_username = input('Введите имя пользователя: ')
            entered_password = input('Введите пароль пользователя: ')
            user = authenticate_user(connect, entered_username, entered_password)

        return dict(user)

    @staticmethod
    def registration_user(connect, role: str = 'user', start_balance: float = 0.0, silent: bool = False) -> dict:
        user = None
        while user is None:
            entered_username = input('Введите имя пользователя: ')
            entered_password = input('Введите пароль пользователя: ')
            user = register_user(connect, entered_username, entered_password, role, start_balance, silent)
        return user

    def get_user(self, connect):
        user_input = get_user_choose_menu(menu=self.MENU)
        user = None

        while user is None:

            match user_input:
                case '1':
                    user = self.login(connect)
                case '2':
                    user = self.registration_user(connect)
                case '3':
                    return
        return user

    @staticmethod
    def show_user_balance(user: dict):
        print()
        print('-' * 40)
        print(f'balance:{"":>20}{user["balance"]}')
        print('-' * 40, '\n')

    @staticmethod
    def change_user_balance(connect, user: dict, atm: dict = None, sub=False):
        value = None
        while value is None:
            try:
                value = is_integer(input('Введите сумму: '))
            except ValidationError as e:
                print(e)

        return change_user_balance(connect, user, value, atm, sub)

    def user_menu(self, connect, user, atm, menu_collector):
        while True:
            user_input = get_user_choose_menu(self.USER_MENU)

            match user_input:
                case '1':
                    self.show_user_balance(user)
                case '2':
                    user, atm = self.change_user_balance(connect, user, atm)
                case '3':
                    user, atm = self.change_user_balance(connect, user, atm, sub=True)
                    atm = withdrawal_user_balance(connect, atm)
                case '4':
                    print('Работа завершена')
                    return

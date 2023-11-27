from HT_12.atm_3_0.custom_exceptions import ValidationError
from HT_12.atm_3_0.menu.utils import get_user_choose_menu
from HT_12.atm_3_0.menu.validators import is_integer


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
        '3. Снять наличные',
        '4. История трансакций',
        '5. Выход\n',
    ]

    def __init__(self, user_view, atm_view):
        self.user_view = user_view
        self.atm_view = atm_view
        self.user_model = None
        self.atm_model = self.atm_view.atm_model

    def login(self):
        user = None
        while user is None:
            entered_username = input('Введите имя пользователя: ')
            entered_password = input('Введите пароль пользователя: ')
            user = self.user_view.authenticate_user(entered_username, entered_password)

        return user

    def registration_user(self, start_balance: float, role: str = 'user', silent: bool = False):
        user = None
        while user is None:
            try:
                entered_username = input('Введите имя пользователя: ')
                entered_password = input('Введите пароль пользователя: ')
                user = self.user_view.register_user(username=entered_username, password=entered_password, role=role,
                                                    balance=start_balance, silent=silent)
            except ValidationError as e:
                print(e)
        return user

    def get_user(self):
        user_input = get_user_choose_menu(menu=self.MENU)

        while self.user_model is None:

            match user_input:
                case '1':
                    self.user_model = self.login()
                case '2':
                    self.user_model = self.registration_user(role='user', start_balance=1000)
                case '3':
                    return

    def change_user_balance(self, sub=False):
        amount = None
        while amount is None:
            try:
                amount = is_integer(input('Введите сумму: '))
            except ValidationError as e:
                print(e)

        self.user_model.change_user_balance(self.user_view.user_db, amount, self.atm_model, self.atm_view, sub)

    def user_menu(self):
        while True:
            user_input = get_user_choose_menu(self.USER_MENU)

            match user_input:
                case '1':
                    print(self.user_model.show_user_balance())
                case '2':
                    self.change_user_balance()
                case '3':
                    self.change_user_balance(sub=True)
                case '4':
                    print(self.user_model.show_user_transactions())
                case '5':
                    print('\nРабота завершена')
                    return

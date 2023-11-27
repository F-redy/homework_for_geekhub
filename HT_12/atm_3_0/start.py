if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[2]))

from HT_12.atm_3_0.atms.views import ATMView
from HT_12.atm_3_0.custom_exceptions import UserExistsError
from HT_12.atm_3_0.menu.collector_menu import CollectorMenu
from HT_12.atm_3_0.menu.user_menu import UserMenu
from HT_12.atm_3_0.menu.utils import get_user_choose_menu
from HT_12.atm_3_0.users.views import UserView


class Statr:
    def __init__(self):
        self.user_view = UserView()
        self.atm_view = ATMView()
        self.user_model = None

    def start(self) -> None:
        self.create_test_data()

        menu = UserMenu(self.user_view, self.atm_view)
        menu.get_user()
        self.user_model = menu.user_model

        if menu.user_model is None:
            print('\nРабота завершена')
            return

        menu_collector = CollectorMenu(self.atm_view, self.user_view)

        match self.user_model.role:
            case 'collector':
                user_input = get_user_choose_menu(menu_collector.CHOOSE_MENU)
                if user_input == '1':
                    menu_collector.collector_menu()
                else:
                    menu.user_menu()
            case 'user':
                menu.user_menu()

    def create_test_data(self):
        """
        Функция для создания тестовых пользователей.
        """

        user_balance = 10000
        users = [
            {'username': 'admin', 'password': 'admin', 'role': 'collector', 'balance': user_balance},
            {'username': 'user_1', 'password': 'password_1', 'role': 'user', 'balance': user_balance},
            {'username': 'user_2', 'password': 'password_2', 'role': 'user', 'balance': user_balance},
            {'username': 'user_3', 'password': 'password_3', 'role': 'user', 'balance': user_balance},
            {'username': 'user_4', 'password': 'password_4', 'role': 'user', 'balance': user_balance},
            {'username': 'user_5', 'password': 'password_5', 'role': 'user', 'balance': user_balance}
        ]

        for userdata in users:
            try:
                self.user_view.register_user(**userdata, silent=True)
            except UserExistsError:
                pass


if __name__ == '__main__':
    Statr().start()

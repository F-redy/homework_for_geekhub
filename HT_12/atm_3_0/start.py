if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[2]))

from database_operations import ATMDataBase, UserDB

from HT_12.atm_3_0.atms.views import ATMView
from HT_12.atm_3_0.custom_exceptions import UserExistsError
from HT_12.atm_3_0.menu.collector_menu import CollectorMenu
from HT_12.atm_3_0.menu.user_menu import UserMenu
from HT_12.atm_3_0.menu.utils import get_user_choose_menu
from HT_12.atm_3_0.users.utils import hash_password


class Statr:
    def __init__(self):
        self.user_db = UserDB()
        self.atm_db = ATMDataBase()
        self.atm_view = ATMView(self.atm_db)
        self.atm_model = None

    def start(self, new_atm):
        """ Запускает систему управления банкоматом.

        Args:
            new_atm (bool): Флаг, указывающий на необходимость создания нового банкомата.

        Returns:
            None

        Если `new_atm` установлен в True, метод создает новый банкомат и
        заполняет тестовыми данными. В противном случае, используется
        существующий банкомат с ID равным 1.

        Метод получает модель банкомата (`atm_model`) и инициализирует пользовательский
        интерфейс (`UserMenu`). В зависимости от роли пользователя (коллектора или обычного
        пользователя), программа предоставляет соответствующие опции меню для взаимодействия.
        """

        if new_atm:
            atm_id = self.create_test_data()
        else:
            atm_id = 1

        self.atm_model = self.atm_view.get_atm_model(atm_id=atm_id)

        menu = UserMenu(self.user_db, self.atm_model, self.atm_db)
        menu.get_user()

        if menu.user_model is None:
            print('\nРабота завершена')
            return

        menu_collector = CollectorMenu(self.atm_db, self.user_db, menu.user_model, self.atm_model)

        match menu.user_model.role:
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
        Функция для создания тестовых пользователей, и нового банкомата.

        Строка 101: Для new_atm устанавливаем new_atm=True.
        Тестовые currency_data с нужными примерами в файле bank_notes_samples.md
        Заменяем, currency_data на нужные данные и проверяем.
        """
        user_balance = 10000
        # Тестовые user-ы не проходят полную валидацию и не получают шанс получить 10% бонуса к начальной сумме.
        users = [
            {'username': 'admin', 'hashed_password': hash_password('admin'), 'role': 'collector',
             'balance': user_balance},
            {'username': 'user_1', 'hashed_password': hash_password('password_1'), 'role': 'user',
             'balance': user_balance},
            {'username': 'user_2', 'hashed_password': hash_password('password_2'), 'role': 'user',
             'balance': user_balance},
            {'username': 'user_3', 'hashed_password': hash_password('password_3'), 'role': 'user',
             'balance': user_balance},
            {'username': 'user_4', 'hashed_password': hash_password('password_4'), 'role': 'user',
             'balance': user_balance},
            {'username': 'user_5', 'hashed_password': hash_password('password_5'), 'role': 'user',
             'balance': user_balance}
        ]

        currency_data = {
            10: 1000,
            20: 1000,
            50: 1000,
            100: 1000,
            200: 1000,
            500: 1000,
            1000: 1000,
        }

        self.atm_view.create_new_atm(currency_data=currency_data)

        for userdata in users:
            try:
                user_id = self.user_db.add_user(**userdata)
                self.user_db.create_user_transaction(user_id=user_id,
                                                     type_transaction='registration',
                                                     amount=user_balance)
            except UserExistsError:
                pass

        return self.atm_view.atm_model.atm_id


if __name__ == '__main__':
    #  При отсутствии DB переключить new_atm=True
    Statr().start(new_atm=False)
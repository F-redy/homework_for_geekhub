from HT_12.atm_3_0.custom_exceptions import ATMCurrencyError
from HT_12.atm_3_0.menu.utils import get_user_choose_menu


class CollectorMenu:
    CHOOSE_MENU = [
        '\n1. Войти как администратор.',
        '2. Войти как пользователь.\n'
    ]
    COLLECTOR_MENU = [
        '\nВыберите действие:',
        '1. Просмотреть общую информацию о банкомате.',
        '2. Просмотреть баланс банкомата.',
        '3. Просмотреть наминал купюр банкомата.',
        '4. Изменить количество купюр.',
        '5. Выход\n',
    ]

    def __init__(self, atm_view, user_view):
        self.atm_view = atm_view
        self.user_view = user_view
        self.user_model = self.user_view.user_model
        self.atm_model = self.atm_view.atm_model

    def change_atm_currency(self):
        denomination = None
        quantity = None

        while denomination is None or quantity is None:
            try:
                if denomination is None:
                    denomination = self.atm_model.validate_denomination(input('\nВведите номинал купюры цифрами: '))
                if quantity is None:
                    quantity = self.atm_model.validate_quantity(input('\nВведите количество купюр цифрами: '))
            except ATMCurrencyError as e:
                print(e)

        self.atm_view.update_denomination(denomination, quantity)
        print('\nОперация прошла успешно.\n')

    def collector_menu(self):
        while True:
            user_input = get_user_choose_menu(self.COLLECTOR_MENU)

            match user_input:
                case '1':
                    print(self.atm_model)
                case '2':
                    print(self.atm_model.show_atm_balance())
                case '3':
                    print(self.atm_model.show_atm_currency())
                case '4':
                    self.change_atm_currency()
                case '5':
                    print('\nРабота завершена.')
                    return

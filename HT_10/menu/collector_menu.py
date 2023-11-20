from HT_10.atm.database_operations.atm_currency_operations import (
    create_atm_currency, delete_atm_currency)
from HT_10.atm.views import change_atm_balance, get_atm_info
from HT_10.menu.custom_exceptions import ValidationError
from HT_10.menu.utils import get_user_choose_menu
from HT_10.menu.validators import is_integer, validate_currencies


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
        '4. Пополнить баланс банкомата.',
        '5. Изъять деньги в банкомате.',
        '6. Добавить наминал купюр в банкомат.',
        '7. Удалить наминал купюр из банкомат.',
        '8. Выход\n',
    ]

    @staticmethod
    def show_atm_info(atm_info: dict):
        print()
        for name, value in atm_info.items():
            print(f'{name}: {value}')
        print()

    @staticmethod
    def show_atm_balance(atm_balance: int):
        print(f'\nБаланс банкомата: {atm_balance}\n')

    @staticmethod
    def show_atm_currencies(all_atm_currencies: list[int]):
        if all_atm_currencies:
            print(all_atm_currencies)
        else:
            print('\nВ банкомат ещё не добавлена валюта.\n')
        print()

    @staticmethod
    def change_balance_atm(connect, atm: dict, sub: bool = False) -> dict:
        old_balance_atm = atm['balance']
        value = None

        while value is None:
            try:
                value = is_integer(input('\nВведите сумму: '))
            except ValidationError as e:
                print(e)

        if sub:
            if old_balance_atm >= value:
                new_balance_atm = old_balance_atm - value
            else:
                print('В банкомате не достаточно средств.')
                return atm
        else:
            new_balance_atm = old_balance_atm + value

        change_atm_balance(connect, atm['id'], new_balance_atm)

        atm = get_atm_info(connect, atm['id'])
        print('Операция прошла успешно.\n')
        return atm

    @staticmethod
    def change_atm_currencies(connect, atm: dict, delete: bool = False):
        denominations_list = None

        while denominations_list is None:
            try:
                message = '\nВведите номиналы купюр цифрами, через пробел: '
                denominations_list = validate_currencies(list(map(int, input(message).split())))
            except ValidationError as e:
                print(e)

        valid_denominations_list = sorted(validate_currencies(denominations_list))

        if delete:
            delete_atm_currency(connect, atm['id'], valid_denominations_list)
        else:
            currency_data = dict.fromkeys(valid_denominations_list, 1000)
            create_atm_currency(connect, atm['id'], currency_data)

        atm = get_atm_info(connect, atm['id'])

        print('\nОперация прошла успешно.\n')
        return atm

    def collector_menu(self, connect, atm):
        while True:
            user_input = get_user_choose_menu(self.COLLECTOR_MENU)

            match user_input:
                case '1':
                    self.show_atm_info(atm)
                case '2':
                    self.show_atm_balance(atm['balance'])
                case '3':
                    self.show_atm_currencies(atm['currencies'])
                case '4':
                    atm = self.change_balance_atm(connect, atm)
                case '5':
                    atm = self.change_balance_atm(connect, atm, sub=True)
                case '6':
                    atm = self.change_atm_currencies(connect, atm)
                case '7':
                    atm = self.change_atm_currencies(connect, atm, delete=True)
                case '8':
                    print('Работа завершена.')
                    return

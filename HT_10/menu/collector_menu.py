from HT_10.atm.database_operations.atm_currency_operations import \
    update_atm_currencies
from HT_10.atm.views import change_atm_balance, get_atm_info
from HT_10.menu.custom_exceptions import ValidationError
from HT_10.menu.utils import get_user_choose_menu
from HT_10.menu.validators import (is_integer, validate_denomination,
                                   validate_quantity)


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

    def show_atm_info(self, atm_info: dict):
        print()
        for name, value in atm_info.items():
            if name == 'currencies':
                self.show_atm_currencies(value)
            else:
                print(f'{name}: {value}')
        print()

    @staticmethod
    def show_atm_balance(atm_balance: int):
        print(f'\nБаланс банкомата: {atm_balance}\n')

    @staticmethod
    def show_atm_currencies(all_atm_currencies: list[dict]):
        if all_atm_currencies:
            title = 'ATM currency'
            print(f'\n{title:^40}')
            for currency in all_atm_currencies:
                print(f'denomination: {currency["denomination"]:<10}quantity: {currency["quantity"]}')
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
    def change_atm_currencies(connect, atm: dict):
        denomination = None
        quantity = None

        while denomination is None or quantity is None:
            try:
                if denomination is None:
                    denomination = validate_denomination(input('\nВведите номинал купюры цифрами: '))
                if quantity is None:
                    quantity = validate_quantity(input('\nВведите количество купюр цифрами: '))
            except ValidationError as e:
                print(e)

        currency_data = {denomination: quantity}
        update_atm_currencies(connect, atm['id'], currency_data)
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
                    atm = self.change_atm_currencies(connect, atm)
                case '5':
                    print('Работа завершена.')
                    return
                # case '4':
                #     atm = self.change_balance_atm(connect, atm)
                # case '5':
                #     atm = self.change_balance_atm(connect, atm, sub=True)
                # case '6':
                #     atm = self.change_atm_currencies(connect, atm)
                # case '7':
                # atm = self.change_atm_currencies(connect, atm, delete=True)

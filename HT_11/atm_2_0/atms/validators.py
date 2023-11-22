from HT_11.atm_2_0.custom_exceptions import (ATMBalanceError, ATMCurrencyError,
                                             ATMError)
from HT_11.atm_2_0.settings import ALLOWED_CURRENCY


class ATMValidator:

    @staticmethod
    def validate_atm_balance(value):
        try:
            balance = int(value)
        except ValueError:
            raise ATMBalanceError('Баланс банкомата должен быть целым числом.')

        if balance < 0:
            raise ATMBalanceError('Баланс банкомата должен быть положительным числом.')

        return balance

    @staticmethod
    def validate_denomination(denomination):
        try:
            denomination = int(denomination)
        except ValueError:
            raise ATMCurrencyError('Купюры могут быть только целым числом.')

        if denomination not in ALLOWED_CURRENCY:
            raise ATMCurrencyError(f'Данного наминала "{denomination}" нет в списке разрешенный номиналов купюр.'
                                   f'\nРазрешенный список номиналов: {ALLOWED_CURRENCY}')

        return denomination

    @staticmethod
    def validate_quantity(quantity):
        try:
            quantity = int(quantity)
        except ValueError:
            raise ATMCurrencyError('Количество купюр должно быть целым числом.')

        if quantity < 0:
            raise ATMCurrencyError('Количество купюр должно быть больше или равно 0')
        return quantity

    @staticmethod
    def validate_atm_id(atm_id):
        try:
            atm_id = int(atm_id)
        except ValueError:
            raise ATMError(f'{atm_id} должно быть числом.')

        return atm_id

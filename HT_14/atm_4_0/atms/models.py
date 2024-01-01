import http
from datetime import datetime

import requests

from HT_14.atm_4_0.atms.Algorithm import Algorithm
from HT_14.atm_4_0.atms.validators import ATMValidator


class ATMModel(ATMValidator, Algorithm):
    def __init__(self, balance: int, currency_data: list[dict]):
        self.__balance = balance
        self.__currency = self.get_valid_currency(currency_data)

    def __str__(self):
        return f'{self.show_atm_balance()}{self.show_atm_currency()}'

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance: int):
        """ Обновляет баланс банкомата. """
        if balance:
            self.__balance = self.validate_atm_balance(balance)

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency_data):
        if currency_data:
            denomination = self.validate_denomination(currency_data['denomination'])
            quantity = self.validate_quantity(currency_data['quantity'])
            self.__currency[denomination] = quantity

    def get_valid_currency(self, currency_data: list[dict]) -> dict:
        valid_currency = {}
        if currency_data:
            for currency in currency_data:
                denomination = self.validate_denomination(currency['denomination'])
                quantity = self.validate_quantity(currency['quantity'])
                valid_currency[denomination] = quantity

            return valid_currency

    def update_currency_data(self, currency_data: dict):
        """ Обновляет данные о наличности в банкомате. """
        for denomination, quantity in currency_data.items():
            self.__currency[self.validate_denomination(denomination)] -= self.validate_quantity(quantity)

    def show_atm_currency(self):
        text_currency = '-' * 40

        if self.currency:
            title = 'ATM currency'

            text_currency += f'\n{title:^40}'
            for denomination, quantity in self.currency.items():
                text_currency += f'\ndenomination: {denomination:<10}quantity: {quantity}'
        else:
            text_currency = '\nВ банкомат ещё не добавлена валюта.\n'

        text_currency += f'\n{"-" * 40}\n'

        return text_currency

    def show_atm_balance(self):
        message = f'Баланс банкомата: {self.balance}'
        return (f'\n{"-" * len(message)}'
                f'\n{message}\n'
                f'{"-" * len(message)}\n')

    @staticmethod
    def show_current_exchange_rate():
        response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
        if response.status_code == http.HTTPStatus.OK:

            today = datetime.now().date()
            print(f'\nКурс на {today.strftime("%Y-%m-%d")}')
            print('-' * 23)

            for currency in response.json():
                print(f'{currency["ccy"]}:')
                print(f'Курс покупки: {round(float(currency["buy"]), 2)} грн')
                print(f'Курс продажи: {round(float(currency["sale"]), 2)} грн')
                print('-' * 23)

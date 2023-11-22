from HT_11.atm_2_0.atms.validators import ATMValidator
from HT_11.atm_2_0.settings import ALLOWED_CURRENCY


class ATMModel(ATMValidator):
    def __init__(self, currency_data: dict = None, balance: int = 0, atm_id: int = None, created_at=None,
                 updated_at=None):
        self.atm_id = atm_id
        self.balance = self.validate_atm_balance(balance)
        self.currencies = self.create_atm_currency_data(currency_data)
        self.created_at = created_at
        self.updated_at = updated_at

    def update_atm_data(self, atm_db, atm_id):
        atm_id, balance, currency_data, created_at, updated_at = self.get_atm_data(atm_db, atm_id)
        self.update_atm_id(atm_id)
        self.update_atm_balance(balance)
        self.update_atm_currency_data(currency_data)
        self.update_atm_created_at(created_at)
        self.update_atm_updated_at(updated_at)
        return self

    def __str__(self):
        return (f'\nATM ID: {self.atm_id}'
                f'{self.show_atm_balance()}'
                f'{self.show_atm_currencies()}'
                f'\nСоздан: {self.created_at}'
                f'\nПоследнее обновление: {self.updated_at}')

    def create_atm_currency_data(self, currency_data: dict):
        atm_currency_data = {}

        if currency_data is None:
            quantity = 1000
            for denomination in ALLOWED_CURRENCY:
                atm_currency_data.update({denomination: quantity})
        else:
            for denomination, quantity in currency_data.items():
                atm_currency_data.update(
                    {self.validate_denomination(denomination): self.validate_quantity(quantity)}
                )

        return atm_currency_data

    def update_atm_balance(self, balance: int):
        if balance:
            self.balance = self.validate_atm_balance(balance)

    def update_atm_currency_data(self, currency_data: dict):
        if currency_data:
            self.currencies = self.create_atm_currency_data(currency_data)

    def update_atm_id(self, atm_id: int):
        if atm_id:
            self.atm_id = self.validate_atm_id(atm_id)

    def update_atm_created_at(self, created_at: str):
        if created_at:
            self.created_at = created_at

    def update_atm_updated_at(self, updated_at: str):
        if updated_at:
            self.updated_at = updated_at

    def get_atm_data(self, atm_db, atm_id):
        atm = atm_db.get_atm(atm_id)
        atm_balance = atm_db.get_sum_atm_currency(atm['id'])
        atm_currency_data = atm_db.get_atm_currencies(atm['id'])

        atm_id = atm['id']
        balance = atm_balance
        currency_data = self.conversion_currency_to_dict(atm_currency_data)
        created_at = atm['created_at']
        updated_at = atm['updated_at']

        return atm_id, balance, currency_data, created_at, updated_at

    @staticmethod
    def conversion_currency_to_dict(atm_currency_data: list) -> dict:
        return {currency['denomination']: currency['quantity'] for currency in atm_currency_data}

    def show_atm_currencies(self):
        text_atm_currency = ''
        line = '-' * 40

        if self.currencies:
            title = 'ATM currency'
            text_atm_currency += f'\n{line}'
            text_atm_currency += f'\n{title:^40}'
            for denomination, quantity in self.currencies.items():
                text_atm_currency += f'\ndenomination: {denomination:<10}quantity: {quantity}'
        else:
            text_atm_currency = '\nВ банкомат ещё не добавлена валюта.\n'

        text_atm_currency += f'\n{line}\n'

        return text_atm_currency

    def show_atm_balance(self):
        message = f'Баланс банкомата: {self.balance}'
        return (f'\n{"-" * len(message)}'
                f'\n{message}\n'
                f'{"-" * len(message)}')

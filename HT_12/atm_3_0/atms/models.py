from datetime import datetime

from HT_12.atm_3_0.atms.validators import ATMValidator
from HT_12.atm_3_0.settings import ALLOWED_CURRENCY


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
        """ Обновляет баланс банкомата. """
        if balance:
            self.balance = self.validate_atm_balance(balance)

    def update_atm_currency_data(self, currency_data: dict):
        """ Обновляет данные о наличности в банкомате. """
        if currency_data:
            self.currencies = self.create_atm_currency_data(currency_data)

    def update_atm_id(self, atm_id: int):
        """ Обновляет идентификатор банкомата. """
        if atm_id:
            self.atm_id = self.validate_atm_id(atm_id)

    def update_atm_created_at(self, created_at: datetime):
        """ Обновляет дату создания банкомата. """
        if created_at and self.created_at is None:
            self.created_at = created_at

    def update_atm_updated_at(self, updated_at: datetime):
        """ Обновляет дату последнего обновления банкомата. """
        if updated_at:
            self.updated_at = updated_at

    def change_atm_currency_data(self, currency_data: dict):
        for denomination, quantity in currency_data.items():
            self.currencies[denomination] -= quantity

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
        """
        Преобразует список объектов sqlite.Row с данными о наличности в банкомате в словарь для удобства работы.

        Args:
            atm_currency_data (list): Список объектов sqlite.Row с данными о наличности в банкомате.

        Returns:
            dict: Словарь, содержащий информацию о наличности в банкомате, где ключ - номинал купюры,
                  значение - количество купюр данного номинала.
        """
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

    def get_allowed_denomination(self, amount: int) -> dict:
        """ Оставляем только нужные номиналы """
        return {denomination: quantity
                for denomination, quantity in self.currencies.items()
                if denomination <= amount and quantity > 0}

    def greedy_algorithm(self, amount: int) -> dict:
        """ Жадный алгоритм выдачи суммы """
        available_denominations = self.get_allowed_denomination(amount)
        sorted_denominations = sorted(available_denominations.keys(), reverse=True)
        selected_denominations = {}
        for current_denomination in sorted_denominations:
            if amount >= current_denomination:
                max_quantity = min(amount // current_denomination, available_denominations.get(current_denomination))
                selected_denominations[current_denomination] = max_quantity
                amount -= current_denomination * max_quantity
        return selected_denominations

    def dynamic_algorithm(self, amount: int) -> dict:
        """
         Динамический алгоритм выдачи суммы

         подсмотрено: https://github.com/codedokode/pasta/blob/master/algorithm/atm.md
        """
        available_denominations = self.get_allowed_denomination(amount)
        sorted_denominations = sorted(
            [denomination for denomination, quantity in available_denominations.items() for _ in range(quantity)],
            reverse=True)

        possible_sums = {0: 0}
        for denomination in sorted_denominations:
            new_sums = {}
            for current_sum in possible_sums.keys():
                new_sum = current_sum + denomination

                if new_sum > amount:
                    continue
                elif new_sum not in possible_sums.keys():
                    new_sums[new_sum] = denomination

            possible_sums.update(new_sums)
            if amount in possible_sums.keys():
                break

        remaining_amount = amount
        used_denominations = []

        try:
            while remaining_amount > 0:
                used_denominations.append(possible_sums[remaining_amount])
                remaining_amount -= possible_sums[remaining_amount]

            selected_denominations_count = {denomination: used_denominations.count(denomination)
                                            for denomination in used_denominations}

            return selected_denominations_count
        except KeyError:
            return {0: 0}

    @staticmethod
    def get_sum_currency(currency: dict):
        """
        Вычисляет общую сумму денежных средств в банкомате на основе данных о наличности.

        Args:
            currency (dict): Словарь, содержащий информацию о наличности в банкомате, где ключ - номинал купюры,
                             значение - количество купюр данного номинала.

        Returns:
            int: Общая сумма денежных средств в банкомате, вычисленная на основе данных о наличности.
        """
        return sum([denomination * quantity for denomination, quantity in currency.items()])

    def count_cash(self, amount: int) -> dict | None:
        """
           Подсчитывает минимальное количество монет для запрошенной суммы.

           Args:
               amount (int): Запрошенная сумма, для которой необходимо подсчитать минимальное количество монет.

           Returns:
               dict or None: Словарь, содержащий минимальное количество монет каждого номинала для суммы.
               Если подсчет невозможен, возвращается None.

           Метод сначала использует жадный алгоритм для подсчета минимального количества монет.
           Если жадный алгоритм не выдает нужную сумму, то применяется динамический алгоритм,
           который может вернуть необходимую сумму монет.
           В итоге возвращается результат с монетами, минимальное количество которых необходимо для указанной суммы.
           """
        greedy_result = self.greedy_algorithm(amount)
        result = greedy_result
        greedy_sum = self.get_sum_currency(greedy_result)
        if greedy_sum != amount:
            dynamic_result = self.dynamic_algorithm(amount)
            dynamic_sum = self.get_sum_currency(dynamic_result)
            if dynamic_sum == amount:
                result = dynamic_result

        if self.get_sum_currency(result) == amount:
            return dict(sorted(result.items(), reverse=True))

        return

    @staticmethod
    def show_withdrawn_money(withdrawn_money: dict) -> None:
        line = '-' * 24
        print(f'\n{line}\nВыданные купюры:')
        for denomination, quantity in withdrawn_money.items():
            print(f'{"":<5}{denomination:<6} |{"":>3} {quantity}')
        print(line)

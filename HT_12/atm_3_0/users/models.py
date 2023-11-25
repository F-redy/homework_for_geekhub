from datetime import datetime
from random import randint

from HT_12.atm_3_0.common.custom_messages import print_message
from HT_12.atm_3_0.users.utils import hash_password
from HT_12.atm_3_0.users.validators import UserValidator


class UserModel(UserValidator):
    def __init__(self, username: str, password: str, role: str = 'user', balance: int = 0, transactions=None,
                 user_id: int = None, created_at=None, updated_at=None, from_db: bool = False):
        self.user_id = user_id
        self.username = self.validate_username(username)
        self.role = self.validate_role(role)
        self.balance = self.validate_user_balance(balance)
        self.transactions = transactions
        self.created_at = created_at
        self.updated_at = updated_at

        if from_db:
            self.password = password
        else:
            self.password = hash_password(self.validate_password(password))

    def __str__(self):
        return (f'\nИмя Пользователя: {self.username}\n'
                f'Role: {self.role}'
                f'{self.show_user_balance()}'
                f'{self.show_user_transactions()}')

    def get_user_data(self):
        """
        Возвращает данные пользователя в виде словаря.

        Returns:
            dict: Словарь с данными пользователя в формате:
                  {'username': str, 'hashed_password': str, 'balance': int, 'role': str}
        """
        return {'username': self.username, 'hashed_password': self.password, 'balance': self.balance, 'role': self.role}

    def show_user_balance(self):
        message = f'На вашем счету:{"":>20}{self.balance}'
        return f'\n{"-" * len(message)}\n{message}\n{"-" * len(message)}\n'

    def show_user_transactions(self):
        text_user_transactions = ''

        if self.transactions:
            n = 50 // 2
            title = f'\nВсе транзакции для Пользователя: {self.username}'
            text_user_transactions += f'\n{title:^40}'
            for indx, transaction in enumerate(self.transactions, -len(self.transactions)):
                text_user_transactions += f"\n{'-' * n} {abs(indx)} {'-' * n}"
                text_user_transactions += f'\nТип Транзакции: {transaction["type_transaction"]}'
                text_user_transactions += f'\nСумма Транзакции: {transaction["amount"]}'
                text_user_transactions += f'\nДата Создания Транзакции: {transaction["created_at"]}'
                text_user_transactions += f"\n{'-' * (n * 2 + len(str(abs(indx))) + 2)}"

        else:
            text_user_transactions = '\nПользователь не совершил ни одной транзакции\n'

        return text_user_transactions

    def update_user_model(self, balance: int = None, transactions=None, user_id: int = None, created_at=None,
                          updated_at=None):
        """
               Обновляет модель пользователя.

               Args:
                   balance (int, optional): Новый баланс пользователя.
                   transactions (list, optional): Список транзакций пользователя.
                   user_id (int, optional): ID пользователя.
                   created_at (datetime, optional): Время создания пользователя.
                   updated_at (datetime, optional): Время последнего обновления данных о пользователе.

               Note:
                   Каждый аргумент представляет собой определенный аспект модели пользователя,
                   который можно обновить с помощью данного метода.

               Returns:
                   None
       """
        self.update_user_balance(balance)
        self.update_user_transactions(transactions)
        self.update_created_at(created_at)
        self.update_updated_at(updated_at)
        self.update_user_id(user_id)

    def update_user_balance(self, new_balance: int):
        """ Обновляет баланс пользователя. """
        if new_balance:
            self.balance = self.validate_user_balance(new_balance)

    def update_user_transactions(self, transactions: list):
        """ Обновляет транзакции пользователя. """
        if transactions:
            self.transactions = transactions

    def update_created_at(self, created_at: datetime):
        """ Обновляет время создания пользователя. """
        if created_at:
            self.created_at = created_at

    def update_updated_at(self, updated_at: datetime):
        """ Обновляет время последнего обновления данных о пользователе. """
        if updated_at:
            self.updated_at = updated_at

    def update_user_id(self, user_id: int):
        """ Обновляет идентификатор пользователя. """
        if user_id:
            self.user_id = user_id

    @staticmethod
    def get_bonus(current_user_balance: int) -> tuple[int, int]:
        """
        Получение бонуса для пользователя.

        Args:
            current_user_balance (int): Текущий баланс пользователя.

        Returns:
            tuple[int, int]: Кортеж из двух значений: величина бонуса и обновленный баланс.
                - Первый элемент кортежа: величина бонуса (если бонус был начислен).
                - Второй элемент кортежа: обновленный баланс после начисления бонуса или нулевого значения.

        """
        chance = randint(0, 100)

        if chance > 49:
            bonus = int(current_user_balance * 0.10)
            current_user_balance += bonus

            return bonus, current_user_balance
        return 0, current_user_balance

    def change_user_balance(self, user_db, amount: int, atm_model, atm_db, sub: bool = False) -> None:
        min_currency = min(atm_model.currencies)
        if sub:
            if (self.balance - amount) > -1:
                if atm_model.balance >= amount:
                    without_atm_currency = atm_model.count_cash(amount)
                    if without_atm_currency:
                        atm_model.show_withdrawn_money(without_atm_currency)
                        self.update_user_model(balance=self.balance - amount)
                        atm_model.change_atm_currency_data(without_atm_currency)
                        atm_db.update_atm_currencies(atm_id=atm_model.atm_id, new_currency_data=atm_model.currencies)
                        atm_db.update_atm_balance(atm_model.atm_id, atm_model.get_sum_currency(atm_model.currencies))
                    else:
                        print_message('Банкомат не может выдавать необходимую сумму.')
                        return
                else:
                    print_message('В банкомате не достаточно средств.')
                    return
            else:
                print_message('Не достаточно средств на вашем счете.')
                return
        else:

            if amount < min_currency:
                print_message(f'Минимальная сумма пополнения: {min_currency}')
                return
            else:
                change = amount % min_currency
                if change:
                    print(f"\nЗдача: {change}")
                amount -= change
                self.balance += amount

        if not amount:
            return

        user_db.update_user_balance(self.user_id, self.balance)
        user_db.create_user_transaction(self.user_id, ('deposit', 'withdrawal')[sub], amount)
        self.update_user_model(transactions=user_db.get_user_transactions(self.user_id))

        print(f'Операция прошла успешно.\n{"-" * 24}\n')

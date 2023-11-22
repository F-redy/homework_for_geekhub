from random import randint

from HT_11.atm_2_0.users.utils import hash_password
from HT_11.atm_2_0.users.validators import UserValidator


class UserModel(UserValidator):
    def __init__(self, username: str, password: str, role: str = 'user', balance: float = 0.0, transactions=None,
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
        return {'username': self.username, 'hashed_password': self.password, 'balance': self.balance, 'role': self.role}

    def show_user_balance(self):
        message = f'На вашем счету:{"":>20}{self.balance}'
        return (f'\n{"-" * len(message)}'
                f'\n{message}\n'
                f'{"-" * len(message)}\n')

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

    def update_user_model(self, balance: int | float = None, transactions=None, user_id: int = None, created_at=None,
                          updated_at=None):
        self.balance = balance
        self.transactions = transactions
        self.update_created_at(created_at)
        self.update_updated_at(updated_at)
        self.update_user_id(user_id)

    def update_user_balance(self, new_balance: int):
        self.balance = new_balance

    def update_created_at(self, created_at):
        if created_at:
            self.created_at = created_at

    def update_updated_at(self, updated_at):
        if updated_at:
            self.updated_at = updated_at

    def update_user_id(self, user_id):
        if user_id:
            self.user_id = user_id

    @staticmethod
    def get_bonus(balance):
        chance = randint(0, 100)

        if chance > 49:
            bonus = balance * 0.10
            balance += bonus

            return bonus, balance
        return 0, balance

    @staticmethod
    def process_transaction(amount: int, available_currencies: dict, sub: bool = False) -> int | None:
        min_currency = min(available_currencies)

        if amount % min_currency != 0:
            if sub:
                print(f'Банкомат может выдавать сумму кратную {min_currency}')
                return
            else:
                if amount < min_currency:
                    print(f'Минимальная сумма пополнения: {min_currency}')
                    return
                else:
                    change = amount % min_currency
                    print(f"\nЗдача: {change}")
                    amount -= change

        return amount  # сумма для зачисления

    def change_user_balance(self, user_db, value: int, atm_model, sub: bool = False) -> None:
        if sub:
            if (self.balance - value) > -1:
                if atm_model.balance >= value:
                    value = self.process_transaction(value, atm_model.currencies, sub=True)
                    if value:
                        self.balance -= value
                else:
                    print('\nВ банкомате не достаточно средств.\n')
                    return
            else:
                print('\nНе достаточно средств на вашем счете.\n')
                return
        else:
            value = self.process_transaction(value, atm_model.currencies)
            if value:
                self.balance += value

        if not value:
            return
        user_db.update_user_balance(self.user_id, self.balance)
        user_db.create_user_transaction(self.user_id, ('deposit', 'withdrawal')[sub], value)
        self.update_user_model(transactions=user_db.get_user_transactions(self.user_id))

        print('Операция прошла успешно.\n')

from HT_11.atm_2_0.custom_exceptions import (IncorrectPasswordError,
                                             UserExistsError,
                                             UserNotFoundError,
                                             ValidationError)
from HT_11.atm_2_0.users.models import UserModel
from HT_11.atm_2_0.users.utils import hash_password


class UserView:

    def __init__(self, user_db):
        self.user_db = user_db
        self.user_model = None

    def register_user(self, username: str, password: str, role: str = 'user', balance: int | float = 0.0,
                      silent: bool = False) -> UserModel | None:

        try:
            self.user_model = UserModel(username=username, password=password, role=role, balance=balance)
        except ValidationError as e:
            if not silent:
                print(f'\nОшибка во время регистрации: {e}\n')
                return

        if self.user_model:
            user_id = None
            try:
                user_id = self.user_db.add_user(**self.user_model.get_user_data())
                self.user_db.create_user_transaction(user_id, 'registration', balance)
            except UserExistsError as e:
                if not silent:
                    print(f'\nОшибка во время регистрации: {e}\n')
                    return

            if not silent:
                print(f'\nПользователь {username} успешно зарегистрирован!\n')

            bonus, balance = self.user_model.get_bonus(balance)

            if bonus:
                self.user_db.update_user_balance(user_id, balance)
                self.user_db.create_user_transaction(user_id, type_transaction='bonus', amount=bonus)

            user_from_db = self.user_db.get_user(username)
            transactions = self.user_db.get_user_transactions(user_id)

            self.user_model.update_user_model(user_id=user_id, balance=balance, transactions=transactions,
                                              created_at=user_from_db['created_at'],
                                              updated_at=user_from_db['updated_at'])
            print(f'\nДобро пожаловать {username}\n')
            return self.user_model

    def authenticate_user(self, entered_username: str, entered_password: str) -> UserModel | None:
        try:
            user = self.user_db.get_user(entered_username)
            if hash_password(entered_password) != user['password']:
                raise IncorrectPasswordError

        except UserNotFoundError as e:
            print(f'\nОшибка авторизации: {e}\n')
            return
        except IncorrectPasswordError:
            print('\nОшибка авторизации: не правильный пароль.\n')
            return

        transactions = self.user_db.get_user_transactions(user['user_id'])
        self.user_model = UserModel(**user, transactions=transactions, from_db=True)

        print(f'\nДобро пожаловать {user["username"]}\n')
        return self.user_model

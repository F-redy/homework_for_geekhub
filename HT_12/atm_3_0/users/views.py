from HT_12.atm_3_0.common.custom_messages import print_message
from HT_12.atm_3_0.custom_exceptions import (IncorrectPasswordError,
                                             UserExistsError,
                                             UserNotFoundError,
                                             ValidationError)
from HT_12.atm_3_0.users.db_operations.DBUser import DBUser
from HT_12.atm_3_0.users.models import UserModel
from HT_12.atm_3_0.users.utils import hash_password


class UserView:

    def __init__(self, ):
        self.user_db = DBUser()
        self.user_model = None

    def register_user(self, username: str, password: str, role: str = 'user', balance: int | float = 0.0,
                      silent: bool = False) -> UserModel | None:

        try:
            self.user_model = UserModel(username=username, password=password, role=role, balance=balance)
        except ValidationError as e:
            if not silent:
                print_message(f'Ошибка во время регистрации: {e}')
            return

        if self.user_model:
            try:
                user_id = self.user_db.add_user(**self.user_model.get_user_data())
                self.user_db.create_user_transaction(user_id, 'registration', balance)
            except UserExistsError as e:
                if not silent:
                    print_message(f'Ошибка во время регистрации: {e}')
                return

            if not silent:
                print_message(f'Пользователь {username} успешно зарегистрирован!')

            bonus, balance = self.user_model.get_bonus(balance)

            if bonus:
                self.user_db.update_user_balance(user_id, balance)
                self.user_db.create_user_transaction(user_id, type_transaction='bonus', amount=bonus)
                print_message(f'Поздравляем {username}, Вы получили бонус: {bonus} при регистрации.')

            user_from_db = self.user_db.get_user(username)
            transactions = self.user_db.get_user_transactions(user_id)

            self.user_model.update_user_model(user_id=user_id, balance=balance, transactions=transactions,
                                              created_at=user_from_db['created_at'],
                                              updated_at=user_from_db['updated_at'])
            if not silent:
                print_message(f'Добро пожаловать {username}')
            return self.user_model

    def authenticate_user(self, entered_username: str, entered_password: str) -> UserModel | None:
        try:
            user = self.user_db.get_user(entered_username)
            if hash_password(entered_password) != user['password']:
                raise IncorrectPasswordError

        except UserNotFoundError as e:
            print_message(f'Ошибка авторизации: {e}')
            return
        except IncorrectPasswordError:
            print_message('Ошибка авторизации: не правильный пароль.')
            return

        transactions = self.user_db.get_user_transactions(user['user_id'])
        self.user_model = UserModel(**user, transactions=transactions, from_db=True)

        print_message(f'Добро пожаловать {user["username"]}')
        return self.user_model

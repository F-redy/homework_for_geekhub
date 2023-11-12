from HT_09.task_3.users import custom_exceptions
from HT_09.task_3.users.validators import validate_password, validate_username
from HT_09.task_3.wallet.models import create_wallet


class CustomUser:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.wallet = {}

    def register_user(self) -> dict:
        try:
            self.validate_user()
        except custom_exceptions.ValidationError as e:
            print(f"Помилка під час реєстрації: {e}")
            return {}

        self.create_wallet()
        return {'username': self.username, 'password': self.password, 'wallet': self.wallet}

    def validate_user(self):
        # Реализуйте вашу логику валидации пользователя
        self.username = validate_username(self.username)
        self.password = validate_password(self.password)

    def create_wallet(self):
        # Реализуйте вашу логику создания кошелька
        self.wallet = create_wallet(self)

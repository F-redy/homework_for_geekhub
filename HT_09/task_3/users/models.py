from HT_09.task_3.users import custom_exceptions
from HT_09.task_3.users.utils import get_create_at
from HT_09.task_3.users.validators import validate_password, validate_username
from HT_09.task_3.wallet.models import create_wallet


def custom_user(username: str, password: str, start_amount: int | float) -> dict:
    user = {}
    try:
        user['username'] = validate_username(username)
        user['password_hash'] = validate_password(password)
    except custom_exceptions.ValidationError as e:
        print(f"Помилка під час реєстрації: {e}")
        return {}

    user = create_wallet(user, start_amount)
    user['create_at'] = get_create_at()
    return user

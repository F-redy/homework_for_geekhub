from HT_10.users.validators import validate_password
from HT_10.users.validators import validate_role
from HT_10.users.validators import validate_user_balance
from HT_10.users.validators import validate_username


def user_model(username: str, password: str, role: str = 'user', balance: float = 0.0) -> dict:
    user = {
        'username': validate_username(username),
        'hashed_password': validate_password(password),
        'role': validate_role(role),
        'balance': validate_user_balance(balance)
    }

    return user

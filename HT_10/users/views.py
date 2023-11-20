from HT_10.users.custom_exceptions import (IncorrectPasswordError,
                                           UserExistsError, UserNotFoundError,
                                           ValidationError)
from HT_10.users.database_operations.transaction_operations import \
    create_user_transaction
from HT_10.users.database_operations.user_operations import (
    add_user, get_user, update_user_balance)
from HT_10.users.models import user_model
from HT_10.users.utils import hash_password


def register_user(connect, username: str, password: str, role: str = 'user', balance: int | float = 0.0,
                  silent: bool = False) -> dict | None:
    new_user = None

    try:
        new_user = user_model(username, password, role, balance)
    except ValidationError as e:
        if not silent:
            print(f'\nОшибка во время регистрации: {e}\n')
            return

    if new_user:
        try:
            print(new_user)
            add_user(connect, **new_user)
        except UserExistsError as e:
            if not silent:
                print(f'\nОшибка во время регистрации: {e}\n')
                return

        if not silent:
            print(f'\nПользователь {username} успешно зарегистрирован!\n')

    return get_user(connect, username)


def authenticate_user(connect, entered_username: str, entered_password: str) -> dict | None:
    try:
        user = get_user(connect, entered_username)
        if hash_password(entered_password) != user['password']:
            raise IncorrectPasswordError

    except UserNotFoundError as e:
        print(f'\nОшибка авторизации: {e}\n')
        return
    except IncorrectPasswordError:
        print('\nОшибка авторизации: не правильный пароль.\n')
        return

    print(f'\nДобро пожаловать {user["username"]}\n')
    return dict(user)


def process_transaction(amount: int, available_currencies: list[int], sub: bool = False) -> int:
    min_currency = min(available_currencies)

    if amount % min_currency != 0:
        if sub:
            print('Невозможно выдать сумму наличными купюрами.')
            return 0
        else:
            change = amount % min_currency
            print(f"\nЗдача: {change}")
            amount -= change

    return amount  # сумма для зачисления


def change_user_balance(connect, user: dict, value: int, atm: dict, sub: bool = False) -> tuple[dict, dict]:
    user_balance = user['balance']
    available_currencies = atm['currencies']
    atm_balance = atm['balance']

    if sub:
        if (user_balance - value) > -1:
            if atm_balance >= value:
                value = process_transaction(value, available_currencies, sub=True)
                if value:
                    user_balance -= value
                    atm_balance -= value
                else:
                    return user, atm
            else:
                print('\nВ банкомате не достаточно средств.\n')
                return user, atm
        else:
            print('\nНе достаточно средств на вашем счете.\n')
            return user, atm
    else:
        value = process_transaction(value, available_currencies)
        user_balance += value

    update_user_balance(connect, user['id'], user_balance)
    create_user_transaction(connect, user['id'], ('deposit', 'withdrawal')[sub], value)

    user['balance'] = user_balance
    atm['balance'] = atm_balance
    print('Операция прошла успешно.\n')
    return user, atm

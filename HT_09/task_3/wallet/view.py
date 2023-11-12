from HT_09.task_3.errors.models import ErrorLogger
from HT_09.task_3.users.utils import get_create_at
from HT_09.task_3.wallet.database_operations import (change_transactions,
                                                     change_user_balance,
                                                     get_user_balance)
from HT_09.task_3.wallet.validators import (check_balance_for_transaction,
                                            validate_transaction_input)

logger = ErrorLogger()


def add_user_balance(user: dict, transaction_amount: int | float) -> dict:
    try:
        transaction_amount = validate_transaction_input(transaction_amount)
    except ValueError as e:
        print(e)
        return user

    user_balance = change_user_balance(user, transaction_amount)
    transaction = {
        'transaction': f'Поповнення балансу {transaction_amount}',
        'create_at': get_create_at()
    }
    change_transactions(user, transaction=transaction)
    user['balance'] = round(user_balance, 2)

    print(f"Баланс {user['username']} поповнено на {transaction_amount}.")

    return user


def sub_user_balance(user: dict, transaction_amount: int | float) -> dict:
    user_balance = get_user_balance(user)

    try:
        transaction_amount = validate_transaction_input(transaction_amount)
    except ValueError as e:
        print(e)
        return user

    try:
        check_balance_for_transaction(user_balance, transaction_amount)
    except ValueError as e:
        print(e)
        return user

    user_balance = change_user_balance(user, transaction_amount, sub=True)
    transaction = {
        'transaction': f'Виведення коштів {transaction_amount}',
        'create_at': get_create_at()
    }

    change_transactions(user, transaction=transaction)
    user['balance'] = user_balance

    print(f"Гроші в сумі {transaction_amount} було списано з рахунку користувача {user['username']}.")

    return user

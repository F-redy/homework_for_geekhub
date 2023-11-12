import json

from HT_09.task_3 import settings
from HT_09.task_3.errors.models import ErrorLogger
from HT_09.task_3.users.utils import get_create_at
from HT_09.task_3.wallet.utils import (get_path_to_user_balance,
                                       get_path_to_user_transactions)
from HT_09.task_3.wallet.validators import validate_transaction_input

logger = ErrorLogger()


def create_balance(user: dict, start_amount: int | float) -> dict | None:
    """ Create user file balance """
    path_to_user_balance = get_path_to_user_balance(user['username'])
    start_amount = validate_transaction_input(start_amount)

    user['path_to_user_balance'] = path_to_user_balance
    user['balance'] = start_amount

    try:
        with open(path_to_user_balance, 'w') as balance_file:
            balance_file.write(str(start_amount))
    except FileNotFoundError as e:
        print(settings.CONTACT_SUPPORT)
        logger.log_error(type(e).__name__, str(e))
        raise

    return user


def get_user_balance(user: dict) -> float | None:
    path_to_user_balance = user.get('path_to_user_balance')
    try:
        with open(path_to_user_balance) as balance_file:
            balance = balance_file.read()
    except FileNotFoundError as e:
        print(settings.CONTACT_SUPPORT)
        logger.log_error(type(e).__name__, str(e))
        raise

    try:
        balance = validate_transaction_input(balance)
    except ValueError as e:
        print(settings.CONTACT_SUPPORT)
        logger.log_error(type(e).__name__, str(e))
        raise

    return balance


def change_user_balance(user: dict, value: float = 0.0, sub: bool = False) -> float | None:
    """ Create user file balance """
    path_to_user_balance = user['path_to_user_balance']
    user_balance = get_user_balance(user)

    if sub:
        user_balance -= value
    else:
        user_balance += value

    try:
        with open(path_to_user_balance, 'w') as balance_file:
            balance_file.write(str(user_balance))
    except FileNotFoundError as e:
        print(settings.CONTACT_SUPPORT)
        logger.log_error(type(e).__name__, str(e))
        raise

    return user_balance


def create_transactions(user: dict, start_amount: float = None) -> dict:
    """ Create a transaction file and write an empty list """

    path_to_user_transactions = get_path_to_user_transactions(user['username'])

    transaction = [
        {
            'transaction': 'registration user',
            'create_at': get_create_at()
        },
    ]
    if start_amount:
        transaction.append(
            {
                'transaction': f'Поповнення балансу на сумму: {start_amount}',
                'create_at': get_create_at()
            }
        )

    with open(path_to_user_transactions, 'w', encoding='utf-8') as transactions_file:
        json.dump(transaction, transactions_file, ensure_ascii=False, indent=4)

    user['path_to_user_transactions'] = path_to_user_transactions

    return user


def get_user_transactions(user: dict) -> list:
    path_to_user_transactions = user.get('path_to_user_transactions')

    try:
        with open(path_to_user_transactions, 'r', encoding='utf-8') as transactions_file:
            transactions = json.load(transactions_file)
    except FileNotFoundError:
        create_transactions(path_to_user_transactions)
        transactions = []

    return transactions


def change_transactions(user: dict, transaction: dict):
    """ Append a new transaction entry to the file """
    path_to_user_transactions = user.get('path_to_user_transactions')
    transactions = get_user_transactions(user)

    transactions.append(transaction)

    try:
        with open(path_to_user_transactions, 'w', encoding='utf-8') as transactions_file:
            json.dump(transactions, transactions_file, ensure_ascii=False, indent=4)
            return True
    except FileNotFoundError as e:
        print(settings.CONTACT_SUPPORT)
        logger.log_error(type(e).__name__, str(e))
        raise

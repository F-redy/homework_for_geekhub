from os import path

from HT_09.task_3 import settings


def get_path_to_user_balance(username: str) -> str:
    return path.join(settings.DATABASE_BALANCE, f'{username}_balance.txt')


def get_path_to_user_transactions(username: str) -> str:
    return path.join(settings.DATABASE_TRANSACTIONS, f'{username}_transactions.json')

from HT_09.task_3.wallet.database_operations import (create_balance,
                                                     create_transactions)


def create_wallet(user: dict, start_amount: int | float) -> dict:
    user = create_balance(user, start_amount)
    user = create_transactions(user, start_amount)

    return user

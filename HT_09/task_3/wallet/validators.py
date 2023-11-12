def validate_transaction_input(value) -> float | None:
    """ Validator for money values """
    try:
        value = float(value)
    except ValueError:
        raise ValueError('Значення має бути числом.')

    if value < 0:
        raise ValueError('Значення має бути більше 0.')

    return value


def check_balance_for_transaction(user_balance: float, transaction_amount: float):
    if transaction_amount > user_balance:
        raise ValueError(f'Недостатньо грошей для виконання транзакції.\n'
                         f'Ваш баланс {user_balance}.')

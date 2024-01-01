from HT_10.atm.custom_exceptions import ATMBalanceError
from HT_10.atm.custom_exceptions import ATMCurrencyError
from HT_10.atm.custom_exceptions import ATMError
from HT_10.settings import ALLOWED_CURRENCY


def validate_atm_balance(value):
    try:
        balance = int(value)
    except ValueError:
        raise ATMBalanceError('Баланс банкомата должен быть целым числом.')

    if balance < 0:
        raise ATMBalanceError('Баланс банкомата должен быть положительным числом.')

    return balance


def validate_atm_currency(value):
    try:
        value = int(value)
    except ValueError:
        raise ATMCurrencyError('Купюры могут быть только целым числом.')

    if value not in ALLOWED_CURRENCY:
        raise ATMCurrencyError(f'{value} нет в списке разрешенных купюр: {list(ALLOWED_CURRENCY)}')

    return value


def validate_quantity_currency(value):
    try:
        value = int(value)
    except ValueError:
        raise ATMCurrencyError(f'{value} - может быть только числом.')

    if value < 1:
        raise ATMCurrencyError(f'{value} должно быть больше 0.')


def validate_atm_id(atm_id):
    try:
        atm_id = int(atm_id)
    except ValueError:
        raise ATMError(f'{atm_id} должно быть числом.')

    return atm_id

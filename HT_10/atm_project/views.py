from HT_10.atm_project.custom_exceptions import (ATMBalanceError,
                                                 ATMCurrencyError, ATMError)
from HT_10.atm_project.database_operations.atm_currency_operations import (
    create_atm_currency, delete_atm_currency, get_atm_currencies)
from HT_10.atm_project.database_operations.atm_operations import (
    create_atm, get_atm, update_atm_balance)
from HT_10.atm_project.models import atm_balance_model, atm_currency_model
from HT_10.atm_project.validators import validate_atm_currency, validate_atm_id
from HT_10.settings import ALLOWED_CURRENCY


def create_atm_currency_data(currency_data: dict):
    atm_currency_data = {}
    if currency_data is None:
        for denomination in ALLOWED_CURRENCY:
            atm_currency_data.update(atm_currency_model(denomination))
    else:
        for denomination, quantity in currency_data.items():
            atm_currency_data.update(atm_currency_model(denomination, quantity))

    return atm_currency_data


def create_new_atm(connect, balance: int = 100000, currency_data: dict = None):
    try:
        balance = atm_balance_model(balance)
        atm_currency_data = create_atm_currency_data(currency_data)

        atm_id = create_atm(connect, **balance)
        create_atm_currency(connect, atm_id, atm_currency_data)

    except (ATMBalanceError, ATMCurrencyError) as e:
        print(e)
        return

    atm = {
        'id': atm_id,
        'balance': balance['balance'],
        'atm_currencies': atm_currency_data
    }
    return atm


def get_all_atm_currencies(connect, atm_id: int) -> list[int] | None:
    try:
        atm_id = validate_atm_id(atm_id)
        all_atm_currencies = get_atm_currencies(connect, atm_id)
    except (ATMError, ATMCurrencyError) as e:
        print(e)
        return

    return [cur['denomination'] for cur in all_atm_currencies]


def get_atm_info(connect, atm_id: int) -> dict:
    atm_db = get_atm(connect, validate_atm_id(atm_id))
    all_atm_currencies = get_all_atm_currencies(connect, atm_id)
    atm_currencies = [currency for currency in all_atm_currencies]

    atm_info = {
        'id': atm_db['id'],
        'balance': atm_db['balance'],
        'currencies': atm_currencies,
        'created_at': atm_db['created_at'],
        'updated_at': atm_db['updated_at']
    }
    return atm_info


def change_atm_balance(connect, atm_id: int, new_balance: int):
    atm = update_atm_balance(connect, validate_atm_id(atm_id), atm_balance_model(new_balance)['balance'])
    return atm


def add_atm_currency(connect, atm_id: int, atm_currencies: list):
    atm_id = validate_atm_id(atm_id)
    for currency in atm_currencies:
        currency = atm_currency_model(currency)
        create_atm_currency(connect, atm_id, currency)

    print('Операция по добавлению новых номиналов, прошла успешно.')
    return True


def delete_atm_currencies(connect, atm_id: int, atm_currencies: list):
    atm_id = validate_atm_id(atm_id)
    for currency in atm_currencies:
        currency = validate_atm_currency(currency)
        delete_atm_currency(connect, atm_id, currency)

    print('Удаление прошло успешно.')
    return True

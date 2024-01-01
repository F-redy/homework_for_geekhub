from HT_10.atm.custom_exceptions import ATMBalanceError
from HT_10.atm.custom_exceptions import ATMCurrencyError
from HT_10.atm.custom_exceptions import ATMError
from HT_10.atm.database_operations.atm_balance import create_atm_balance
from HT_10.atm.database_operations.atm_balance import update_atm_balance
from HT_10.atm.database_operations.atm_currency_operations import create_atm_currency
from HT_10.atm.database_operations.atm_currency_operations import delete_atm_currency
from HT_10.atm.database_operations.atm_currency_operations import get_atm_currencies
from HT_10.atm.database_operations.atm_currency_operations import get_sum_atm_currency
from HT_10.atm.database_operations.atm_operations import create_atm
from HT_10.atm.database_operations.atm_operations import get_atm
from HT_10.atm.models import atm_balance_model
from HT_10.atm.models import atm_currency_model
from HT_10.atm.models import atm_model
from HT_10.atm.validators import validate_atm_currency
from HT_10.atm.validators import validate_atm_id
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


def create_new_atm(connect, currency_data: dict = None):
    try:
        atm_currency_data = create_atm_currency_data(currency_data)

        atm_id = create_atm(connect)
        create_atm_currency(connect, atm_id, atm_currency_data)
        atm_balance = get_sum_atm_currency(connect, atm_id)
        create_atm_balance(connect, atm_id, atm_balance)

    except (ATMBalanceError, ATMCurrencyError) as e:
        print(e)
        return

    return atm_model(atm_id, atm_balance, atm_currency_data)


def get_all_atm_currencies(connect, atm_id: int) -> list[dict] | None:
    try:
        atm_id = validate_atm_id(atm_id)
        all_atm_currencies = get_atm_currencies(connect, atm_id)
    except (ATMError, ATMCurrencyError) as e:
        print(e)
        return

    return [{'denomination': cur['denomination'], 'quantity': cur['quantity']} for cur in all_atm_currencies]


def get_atm_info(connect, atm_id: int) -> dict:
    atm_db = get_atm(connect, validate_atm_id(atm_id))
    atm_balance = get_sum_atm_currency(connect, atm_id)
    all_atm_currencies = get_all_atm_currencies(connect, atm_id)
    atm_currencies = [currency for currency in all_atm_currencies]

    atm_info = {
        'id': atm_db['id'],
        'balance': atm_balance,
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

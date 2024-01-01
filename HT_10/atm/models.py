from HT_10.atm.validators import validate_atm_balance
from HT_10.atm.validators import validate_atm_currency


def atm_balance_model(balance):
    return {'balance': validate_atm_balance(balance)}


def atm_currency_model(denomination, quantity_default=1000):
    return {validate_atm_currency(denomination): quantity_default}


def atm_model(atm_id, balance, currencies):
    atm = {
        'id': atm_id,
        'balance': balance,
        'currencies': currencies
    }

    return atm

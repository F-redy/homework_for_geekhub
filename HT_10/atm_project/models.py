from HT_10.atm_project.validators import (validate_atm_balance,
                                          validate_atm_currency)


def atm_balance_model(balance_default):
    return {'balance': validate_atm_balance(balance_default)}


def atm_currency_model(denomination, quantity_default=1000):
    return {validate_atm_currency(denomination): quantity_default}

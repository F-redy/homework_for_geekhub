from HT_14.atm_4_0.atms.DBATMCurrency import DataBaseATMCurrency
from HT_14.atm_4_0.atms.models import ATMModel
from HT_14.atm_4_0.common.custom_messages import print_message
from HT_14.atm_4_0.custom_exceptions import ATMBalanceError
from HT_14.atm_4_0.custom_exceptions import ATMCurrencyError


class ATMView:
    def __init__(self):
        self.atm_db = DataBaseATMCurrency()
        self.atm_model = self.create_atm_model()

    def create_atm_model(self):
        try:
            self.atm_db.create_atm_currency()
            atm_balance = self.atm_db.get_sum_atm_currency()
            atm_currency = self.atm_db.get_atm_currency()
        except (ATMBalanceError, ATMCurrencyError) as e:
            print_message(e)
            return

        return ATMModel(atm_balance, atm_currency)

    def update_denomination(self, denomination: int, quantity: int):
        if self.atm_model:
            self.atm_model.currency = {'denomination': denomination, 'quantity': quantity}
            self.atm_db.update_denomination(denomination, quantity)
            self.atm_model.balance = self.atm_db.get_sum_atm_currency()

    def update_currency_data(self, currency_data: dict):
        if self.atm_model:
            self.atm_model.update_currency_data(currency_data)
            currency_data = [(quantity, denomination) for denomination, quantity in self.atm_model.currency.items()]
            self.atm_db.update_currency_data(currency_data)
            self.atm_model.balance = self.atm_db.get_sum_atm_currency()


if __name__ == '__main__':
    atm = ATMView()
    atm.create_atm_model()
    print(atm.atm_model)

    cur_data = {
        10: 0,
        20: 6,
        50: 4,
        100: 1,
        200: 1,
        500: 0,
        1000: 0,
    }
    atm.update_currency_data(cur_data)
    print(atm.atm_model)

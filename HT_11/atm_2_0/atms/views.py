from HT_11.atm_2_0.atms.models import ATMModel
from HT_11.atm_2_0.custom_exceptions import ATMBalanceError
from HT_11.atm_2_0.custom_exceptions import ATMCurrencyError


class ATMView:
    def __init__(self, atm_db):
        self.atm_db = atm_db
        self.atm_model = None

    def create_new_atm(self, currency_data: dict = None):
        try:
            self.atm_model = ATMModel(currency_data=currency_data)

            atm_id = self.atm_db.create_atm()
            self.atm_db.create_atm_currency(atm_id, self.atm_model.currencies)
            atm_balance = self.atm_db.get_sum_atm_currency(atm_id)
            self.atm_db.create_atm_balance(atm_id, atm_balance)

        except (ATMBalanceError, ATMCurrencyError) as e:
            print(e)
            return

        self.atm_model.update_atm_data(self.atm_db, atm_id)

    def get_atm_model(self, atm_id):

        return ATMModel().update_atm_data(self.atm_db, atm_id)
    # def change_atm_balance(self, atm_id: int, new_balance: int):
    #     self.atm_db.update_atm_balance(self.atm_model.validate_atm_id(atm_id),
    #                                    self.atm_model.validate_atm_balance(new_balance))
    #     self.atm_model.update_atm_data(self.atm_db, atm_id)

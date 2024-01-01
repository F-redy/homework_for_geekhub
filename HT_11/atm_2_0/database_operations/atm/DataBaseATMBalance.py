from HT_11.atm_2_0.custom_exceptions.atm_exceptions import ATMBalanceError
from HT_11.atm_2_0.database_operations.BaseDataBase import BaseDataBase
from HT_11.atm_2_0.database_operations.BaseDataBase import sq


class DataBaseATMBalance(BaseDataBase):
    def create_atm_balance(self, atm_id: int, balance: int) -> None:
        query = """INSERT OR IGNORE INTO atm_balance (atm_id, balance) VALUES (?, ?)"""

        try:
            self.execute_query(query, (atm_id, balance), is_commit=True)
        except sq.Error as e:
            raise ATMBalanceError(f"Ошибка при добавлении баланса  для банкомата с ID {atm_id}: {e}")

    def update_atm_balance(self, atm_id: int, balance: int):
        query = """ UPDATE atm_balance SET balance = ? WHERE atm_id = ?"""

        try:
            self.execute_query(query, (balance, atm_id), is_commit=True)
        except sq.Error as e:
            raise ATMBalanceError(f"Ошибка при изменении баланса  для банкомата с ID {atm_id}: {e}")

from HT_12.atm_3_0.BaseDataBase import BaseDataBase, sq
from HT_12.atm_3_0.custom_exceptions.atm_exceptions import ATMCurrencyError


class DataBaseATMCurrency(BaseDataBase):
    ALLOWED_CURRENCY = {
        10: 0,
        20: 0,
        50: 0,
        100: 0,
        200: 0,
        500: 0,
        1000: 0
    }

    def create_atm_currency(self) -> None:
        """
        Добавляет записи о валюте в таблицу atm_currency.

        Raises:
            ATMCurrencyError: Если произошла ошибка при добавлении валюты в таблицу atm_currency.
        """

        query = """INSERT OR IGNORE INTO atm_currency (denomination, quantity) VALUES (?, ?)"""
        data_currency = [(denomination, quantity) for denomination, quantity in self.ALLOWED_CURRENCY.items()]

        try:
            self._execute_many_queries(query, data_currency, is_commit=True)
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при добавлении валюты: {e}")

    def get_atm_currency(self) -> list[dict]:
        """
            Получает данные о валюте банкомата.

            Returns:
                list[dict]: Список словарей с информацией о валюте.

            Keys: 'denomination', 'quantity'

            Raises:
                ATMCurrencyError: Если произошла ошибка при получении данных о валюте.
        """
        query = """SELECT denomination, quantity FROM atm_currency"""

        try:
            self._execute_query(query)
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при получении данных о валюте: {e}")

        return [dict(currency) for currency in self.cursor.fetchall()]

    def get_sum_atm_currency(self) -> int:
        """
       Получает сумму денег, основываясь на количестве и номинале купюр.

       Returns:
           int: Сумма денег, вычисленная на основе количества и номинала купюр.

       Raises:
           ATMCurrencyError: Если произошла ошибка при получении данных о валюте.
       """
        query = """SELECT SUM(denomination * quantity) FROM atm_currency"""

        try:
            self._execute_query(query)
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при получении данных о валюте: {e}")

        return sum(self.cursor.fetchone())

    def update_denomination(self, denomination: int, quantity: int) -> None:
        """
        Обновляет данные для конкретного номинала.

        Args:
            denomination (int): Номинал купюры для обновления.
            quantity (int): Количество купюр.

        Raises:
            ATMCurrencyError: Если произошла ошибка при обновлении данных о валюте.
        """
        query = """
           UPDATE atm_currency
           SET quantity = ?
           WHERE denomination = ?
           """

        try:
            self._execute_query(query, (quantity, denomination), is_commit=True)
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при обновлении валюты {denomination}: {e}")

    def update_currency_data(self, new_currency_data: list[tuple]) -> None:
        """
        Обновляет данные о валюте.

        Args:
            new_currency_data list[tuple]: Список кортежей (denomination, quantity) [(10, 100), (20, 50) ...].

        Raises:
            ATMCurrencyError: Если произошла ошибка при обновлении данных о валюте.
        """
        query = """
        UPDATE atm_currency
        SET quantity = ?
        WHERE denomination = ?
        """

        try:
            self._execute_many_queries(query, new_currency_data, is_commit=True)
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при обновлении валюты: {e}")

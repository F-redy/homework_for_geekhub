from HT_12.atm_3_0.custom_exceptions.atm_exceptions import ATMCurrencyError
from HT_12.atm_3_0.database_operations.BaseDataBase import BaseDataBase, sq


class DataBaseATMCurrency(BaseDataBase):

    def create_atm_currency(self, atm_id: int, currency_data: dict) -> None:
        """
        Добавляет записи о валюте в таблицу atm_currency для указанного банкомата.

        Args:
            atm_id (int): Идентификатор банкомата, для которого добавляется валюта.
            currency_data (dict): Словарь со значениями валюты в формате {denomination: quantity}.

        Returns: None

        Raises:
            ATMCurrencyError: Если произошла ошибка при добавлении валюты в банкомат.
        """

        query = """INSERT OR IGNORE INTO atm_currency (atm_id, denomination, quantity) VALUES (?, ?, ?)"""
        _denomination = None

        try:
            for denomination, quantity in currency_data.items():
                _denomination = denomination
                self.execute_query(query, (atm_id, denomination, quantity))
            self.connect.commit()
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при добавлении валюты {_denomination} для банкомата с ID {atm_id}: {e}")

    def get_atm_currencies(self, atm_id: int) -> list[sq.Row]:
        """
            Получает данные о валюте для указанного банкомата.

            Args:
                atm_id (int): Идентификатор банкомата, для которого нужно получить данные о валюте.

            Returns:
                list[sqlite3.Row]: Список строк sqlite3.Row с информацией о валюте для указанного банкомата.

            Keys: 'denomination', 'quantity'

            Raises:
                ATMCurrencyError: Если произошла ошибка при получении данных о валюте для банкомата.
        """
        query = """
        SELECT denomination, quantity
        FROM atm_currency
        WHERE atm_id = ?
        """

        try:
            self.execute_query(query, (atm_id,))
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при получении данных о валюте для банкомата: {e}")

        return self.cursor.fetchall()

    def get_sum_atm_currency(self, atm_id: int) -> int:
        query = """
            SELECT SUM(denomination * quantity)
            FROM atm_currency
            WHERE atm_id = ?
            """

        try:
            self.execute_query(query, (atm_id,))
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при получении данных о валюте для банкомата c ID{atm_id}: {e}")

        return sum(self.cursor.fetchone())

    def update_atm_currencies(self, atm_id: int, new_currency_data: dict) -> None:
        """
        Обновляет данные о валюте для указанного банкомата.

        Args:
            atm_id (int): Идентификатор банкомата, для которого нужно обновить данные о валюте.
            new_currency_data (dict): Словарь с обновленными значениями валюты в формате {denomination: quantity}.

        Raises:
            ATMCurrencyError: Если произошла ошибка при обновлении данных о валюте для банкомата.
        """
        query = """
        UPDATE atm_currency
        SET quantity = ?
        WHERE atm_id = ? AND denomination = ?
        """

        _denomination = None

        try:
            for denomination, quantity in new_currency_data.items():
                _denomination = denomination
                self.execute_query(query, (quantity, atm_id, denomination))
            self.connect.commit()

        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при обновлении валюты {_denomination} для банкомата с ID {atm_id}: {e}")

    def delete_atm_currency(self, atm_id: int, denominations_list: list) -> None:
        """
        Удаляет запись о валюте из таблицы atm_currency для указанного банкомата и номинала.

        Args:
            atm_id (int): Идентификатор банкомата, записи о валюте которого требуется удалить.
            denominations_list (list): Номиналы валюты, которые требуется удалить.

        Returns: None

        Raises:
            ATMCurrencyError: Если произошла ошибка при удалении валюты.
        """
        query = """DELETE FROM atm_currency WHERE atm_id = ? AND denomination = ?"""

        try:
            for denomination in denominations_list:
                self.execute_query(query, (atm_id, denomination))
            self.connect.commit()
        except sq.Error as e:
            raise ATMCurrencyError(f"Ошибка при удалении валюты для банкомата с ID {atm_id}: {e}")

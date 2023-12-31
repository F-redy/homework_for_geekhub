from HT_10.atm.custom_exceptions import ATMCurrencyError
from HT_10.database_operations import sq


def create_atm_currency(connect: sq.Connection, atm_id: int, currency_data: dict) -> None:
    """
    Добавляет записи о валюте в таблицу atm_currency для указанного банкомата.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        atm_id (int): Идентификатор банкомата, для которого добавляется валюта.
        currency_data (dict): Словарь со значениями валюты в формате {denomination: quantity}.

    Returns: None

    Raises:
        ATMCurrencyError: Если произошла ошибка при добавлении валюты в банкомат.
    """

    query = """INSERT OR IGNORE INTO atm_currency (atm_id, denomination, quantity) VALUES (?, ?, ?)"""
    cursor = connect.cursor()
    _denomination = None

    try:
        for denomination, quantity in currency_data.items():
            _denomination = denomination
            cursor.execute(query, (atm_id, denomination, quantity))
        connect.commit()

    except sq.Error as e:
        connect.rollback()
        raise ATMCurrencyError(f"Ошибка при добавлении валюты {_denomination} для банкомата с ID {atm_id}: {e}")


def get_atm_currencies(connect: sq.Connection, atm_id: int) -> list[sq.Row]:
    """
        Получает данные о валюте для указанного банкомата.

        Args:
            connect (sqlite3.Connection): Объект соединения с базой данных.
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
    cursor = connect.cursor()

    try:
        cursor.execute(query, (atm_id,))
        currencies = cursor.fetchall()

    except sq.Error as e:
        raise ATMCurrencyError(f"Ошибка при получении данных о валюте для банкомата: {e}")

    return currencies


def get_sum_atm_currency(connect: sq.Connection, atm_id: int) -> int:
    query = """
        SELECT SUM(denomination * quantity)
        FROM atm_currency
        WHERE atm_id = ?
        """
    cursor = connect.cursor()
    try:
        balance = cursor.execute(query, (atm_id,)).fetchone()
    except sq.Error as e:
        raise ATMCurrencyError(f"Ошибка при получении данных о валюте для банкомата c ID{atm_id}: {e}")

    return sum(balance)


def update_atm_currencies(connect: sq.Connection, atm_id: int, new_currency_data: dict) -> None:
    """
    Обновляет данные о валюте для указанного банкомата.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
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
    cursor = connect.cursor()

    _denomination = None

    try:
        for denomination, quantity in new_currency_data.items():
            _denomination = denomination
            cursor.execute(query, (quantity, atm_id, denomination))
        connect.commit()

    except sq.Error as e:
        connect.rollback()
        raise ATMCurrencyError(f"Ошибка при обновлении валюты {_denomination} для банкомата с ID {atm_id}: {e}")


def delete_atm_currency(connect: sq.Connection, atm_id: int, denominations_list: list) -> bool:
    """
    Удаляет запись о валюте из таблицы atm_currency для указанного банкомата и номинала.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        atm_id (int): Идентификатор банкомата, записи о валюте которого требуется удалить.
        denominations_list (list): Номиналы валюты, которые требуется удалить.

    Returns:
        bool: Возвращает True, если операция удаления выполнена успешно.

    Raises:
        ATMCurrencyError: Если произошла ошибка при удалении валюты.
    """
    query = """DELETE FROM atm_currency WHERE atm_id = ? AND denomination = ?"""
    cursor = connect.cursor()

    try:
        for denomination in denominations_list:
            cursor.execute(query, (atm_id, denomination))
        connect.commit()
    except sq.Error as e:
        connect.rollback()
        raise ATMCurrencyError(f"Ошибка при удалении валюты для банкомата с ID {atm_id}: {e}")

    return True

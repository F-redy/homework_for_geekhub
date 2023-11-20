from HT_10.atm_project.custom_exceptions import ATMCurrencyError
from HT_10.database_operations import sq


def manage_atm_currency(connect: sq.Connection, query, atm_id: int, currency_data: dict,
                        is_update: bool = False) -> bool:
    """
    Добавляет или обновляет записи о валюте в таблице atm_currency для указанного банкомата.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        atm_id (int): Идентификатор банкомата, для которого добавляется или обновляется валюта.
        query (str): SQL-запрос для добавления или обновления данных в таблице atm_currency.
        currency_data (dict): Словарь со значениями валюты в формате {denomination: quantity}.
        is_update (bool, optional): Флаг, указывающий на операцию обновления. По умолчанию False (операция вставки).

    Returns:
        bool: Возвращает True, если операция выполнена успешно.

    Raises:
        ATMCurrencyError: Если произошла ошибка при добавлении или обновлении валюты в банкомате.
    """
    cursor = connect.cursor()
    _denomination = None

    try:
        for denomination, quantity in currency_data.items():
            _denomination = denomination
            cursor.execute(query, (quantity, atm_id, denomination))
        connect.commit()
        return True

    except sq.Error as e:
        connect.rollback()
        action = "обновления" if is_update else "добавления"
        raise ATMCurrencyError(f"Ошибка при {action} валюты {_denomination} для банкомата с ID {atm_id}: {e}")


def create_atm_currency(connect: sq.Connection, atm_id: int, currency_data: dict) -> bool:
    """
    Добавляет записи о валюте в таблицу atm_currency для указанного банкомата.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        atm_id (int): Идентификатор банкомата, для которого добавляется валюта.
        currency_data (dict): Словарь со значениями валюты в формате {denomination: quantity}.

    Returns:
        bool: Возвращает True, если операция добавления выполнена успешно.

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

    return True


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
    SELECT denomination
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


def update_atm_currencies(connect: sq.Connection, atm_id: int, new_currency_data: dict) -> True:
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
    SET denomination = ?, quantity = ?
    WHERE atm_id = ?
    """
    cursor = connect.cursor()

    _denomination = None

    try:
        for denomination, quantity in new_currency_data.items():
            _denomination = denomination
            cursor.execute(query, (denomination, quantity, atm_id))
        connect.commit()

    except sq.Error as e:
        connect.rollback()
        raise ATMCurrencyError(f"Ошибка при обновлении валюты {_denomination} для банкомата с ID {atm_id}: {e}")

    return True


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

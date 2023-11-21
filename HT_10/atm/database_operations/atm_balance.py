from HT_10.atm.custom_exceptions import ATMBalanceError
from HT_10.database_operations import sq


def create_atm_balance(connect: sq.Connection, atm_id: int, balance: int) -> None:
    query = """INSERT OR IGNORE INTO atm_balance (atm_id, balance) VALUES (?, ?)"""
    cursor = connect.cursor()

    try:
        cursor.execute(query, (atm_id,balance))
        connect.commit()
    except sq.Error as e:
        connect.rollback()
        raise ATMBalanceError(f"Ошибка при добавлении баланса  для банкомата с ID {atm_id}: {e}")


def update_atm_balance(connect: sq.Connection, atm_id: int, balance: int):
    query = """ UPDATE atm_balance SET balance = ? WHERE atm_id = ?"""
    cursor = connect.cursor()

    try:
        cursor.execute(query, (balance, atm_id))
    except sq.Error as e:
        connect.rollback()
        raise ATMBalanceError(f"Ошибка при изменении баланса  для банкомата с ID {atm_id}: {e}")

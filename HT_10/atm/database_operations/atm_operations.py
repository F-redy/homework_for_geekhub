from HT_10.atm.custom_exceptions import ATMError
from HT_10.database_operations import sq


def create_atm(connect: sq.Connection) -> int | None:
    query = """INSERT INTO atm DEFAULT VALUES"""
    cursor = connect.cursor()

    try:
        cursor.execute(query, )
        connect.commit()
        print(f'Новый банкомат c ID {cursor.lastrowid} создан')
        return cursor.lastrowid  # Возвращаем ID только что созданной записи
    except sq.Error as e:
        raise ATMError(f"Ошибка при создании банкомата: {e}")


def get_atm(connect: sq.Connection, atm_id: int) -> sq.Row | None:
    """'keys: id', 'created_at', 'updated_at'"""

    query = """
    SELECT id, created_at, updated_at
    FROM atm
    WHERE id = ?
    """
    cursor = connect.cursor()
    cursor.execute(query, (atm_id,))

    atm = cursor.fetchone()
    if not atm:
        raise ATMError(f'Банкомат с ID {atm_id} не найден.')

    return atm


def delete_atm(connect: sq.Connection, id_atm: int):
    query = """DELETE FROM atm WHERE id = ?"""
    cursor = connect.cursor()
    try:
        cursor.execute(query, (id_atm,))
        connect.commit()
        print(f'Банкомат под номером {id_atm} - был успешно удален.')
    except sq.Error as e:
        raise sq.Error(f"Ошибка при удалении банкомата: {e}")

    return True

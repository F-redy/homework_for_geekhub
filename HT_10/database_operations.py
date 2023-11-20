import sqlite3 as sq

from HT_10 import settings


def connect_db() -> sq.Connection:
    try:
        with sq.connect(settings.DB_PATH) as connect:
            connect.row_factory = sq.Row  # -> <class 'sqlite3.Row'>
            return connect
    except sq.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise


def execute_sql_script(connect) -> None:
    cursor = connect.cursor()

    with open(settings.SCHEMA_FILE_PATH, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    connect.commit()

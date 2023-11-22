import sqlite3 as sq

from HT_11.atm_2_0 import settings


class BaseDataBase:
    connect: sq.Connection = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if cls.connect is None:
            cls.connect = cls.connect_db()
            cls.cursor = cls.connect.cursor()
        cls.execute_sql_script()
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def connect_db() -> sq.Connection:
        try:
            with sq.connect(settings.DB_PATH) as connect:
                connect.row_factory = sq.Row  # -> <class 'sqlite3.Row'>
                return connect
        except sq.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    @classmethod
    def execute_sql_script(cls) -> None:
        with open(settings.SCHEMA_FILE_PATH, 'r', encoding='utf-8') as schema:
            sql_script = schema.read()

        cls.cursor.executescript(sql_script)
        cls.connect.commit()

    @classmethod
    def execute_query(cls, query: str, params: tuple = None, is_commit: bool = False):
        try:
            if params is None:
                cls.cursor.execute(query)
            else:
                cls.cursor.execute(query, params)
        except sq.Error:
            cls.connect.rollback()
            raise
        if is_commit:
            cls.connect.commit()

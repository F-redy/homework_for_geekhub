import sqlite3 as sq

from HT_12.atm_3_0 import settings


class BaseDataBase:
    """
    Класс для взаимодействия с базой данных SQLite.

    Attributes:
        connect (sqlite3.Connection): Объект подключения к базе данных.
        cursor: Объект курсора для выполнения запросов.
    """

    connect: sq.Connection = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if cls.connect is None:
            cls.connect = cls.connect_db()
            cls.cursor = cls.connect.cursor()
        cls._execute_sql_script()
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def connect_db() -> sq.Connection:
        """
        Устанавливает соединение с базой данных.

        Returns:
            sqlite3.Connection: Объект подключения к базе данных SQLite.
        """
        try:
            with sq.connect(settings.DB_PATH) as connect:
                connect.row_factory = sq.Row  # -> <class 'sqlite3.Row'>
                return connect
        except sq.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    @classmethod
    def _execute_sql_script(cls) -> None:
        """
        Выполняет SQL-скрипт для инициализации базы данных.
        """
        with open(settings.SCHEMA_FILE_PATH, 'r', encoding='utf-8') as schema:
            sql_script = schema.read()

        cls.cursor.executescript(sql_script)
        cls.connect.commit()

    @classmethod
    def _execute_query(cls, query: str, params: tuple = None, is_commit: bool = False):
        """
        Выполняет SQL-запрос к базе данных.

        Args:
            query (str): SQL-запрос для выполнения.
            params (tuple, optional): Параметры для SQL-запроса.
            is_commit (bool, optional): Флаг для фиксации изменений в базе данных.

        Raises:
            sqlite3.Error: В случае ошибки при выполнении запроса.

        Notes:
            Если `is_commit` установлен в `True`, изменения фиксируются в базе данных.
        """
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

    @classmethod
    def _execute_many_queries(cls, query: str, data: list[tuple], is_commit: bool = False):
        """
        Выполняет массовую операцию SQL-запросов к базе данных.

        Args:
            query (str): SQL-запрос для выполнения.
            data (list): Список кортежей с параметрами для SQL-запроса.
            is_commit (bool, optional): Флаг для фиксации изменений в базе данных.

        Raises:
            sqlite3.Error: В случае ошибки при выполнении запроса.

        Notes:
            Если `is_commit` установлен в `True`, изменения фиксируются в базе данных.
        """
        try:
            cls.cursor.executemany(query, data)
        except sq.Error:
            cls.connect.rollback()
            raise
        if is_commit:
            cls.connect.commit()

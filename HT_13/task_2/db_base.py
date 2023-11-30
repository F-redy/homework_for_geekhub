import sqlite3 as sq

from HT_13.task_2 import settings


class DBManager:
    """ Класс для взаимодействия с базой данных SQLite. """

    def __init__(self):
        self.connect = None
        self.cursor = None

    def connect_db(self):
        """ Устанавливает соединение с базой данных. """
        try:
            with sq.connect(settings.DB_PATH) as connect:
                connect.row_factory = sq.Row  # -> <class 'sqlite3.Row'>

        except sq.Error as e:
            print(f"Error db connect: {e}")
            raise

        self.connect = connect
        self.cursor = self.connect.cursor()

        self._execute_sql_script()

    def _execute_sql_script(self) -> None:
        """
        Выполняет SQL-скрипт для инициализации базы данных.
        """
        if self.connect is None:
            raise ValueError('No connection to the database')

        with open(settings.PATH_TO_SCHEMA, 'r', encoding='utf-8') as schema:
            sql_script = schema.read()

        self.cursor.executescript(sql_script)
        self.connect.commit()

    def execute_query(self, query: str, params: tuple = None, is_commit: bool = False):
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
        if self.connect is None:
            raise ValueError('No connection to the database')

        try:
            if params is None:
                self.cursor.execute(query)

            else:
                self.cursor.execute(query, params)
        except sq.Error:
            self.connect.rollback()
            raise

        if is_commit:
            self.connect.commit()

    def execute_many_queries(self, query: str, data: list[tuple], is_commit: bool = False):
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
        if self.connect is None:
            raise ValueError('No connection to the database')

        try:
            self.cursor.executemany(query, data)
        except sq.Error:
            self.connect.rollback()
            raise

        if is_commit:
            self.connect.commit()

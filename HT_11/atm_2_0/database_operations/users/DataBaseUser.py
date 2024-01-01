from HT_11.atm_2_0.custom_exceptions.users_exceptions import UserBalanceUpdateError
from HT_11.atm_2_0.custom_exceptions.users_exceptions import UserExistsError
from HT_11.atm_2_0.custom_exceptions.users_exceptions import UserNotFoundError
from HT_11.atm_2_0.database_operations.BaseDataBase import BaseDataBase
from HT_11.atm_2_0.database_operations.BaseDataBase import sq


class DataBaseUser(BaseDataBase):
    def add_user(self, username: str, hashed_password: str, role: str, balance: float = 0.0) -> int | None:
        """
            Создает нового пользователя в базе данных.

            Args:
                username (str): Имя пользователя.
                hashed_password (str): Захешированный пароль с использованием алгоритма hashlib.sha256.
                role (str, optional): Роль пользователя. (user или collector)
                balance (float): Стартовый балас пользователя.

            Returns:
                int | None: Возвращает идентификатор (ID) только что созданного пользователя в базе данных (lastrowid),
                        если пользователь успешно создан, в противном случае возвращает None.

            Keys:

            Raises:
                UserExistsError: Если пользователь с таким именем уже существует в базе данных.
        """
        query = """INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)"""

        try:
            self.execute_query(query, (username, hashed_password, role, balance), is_commit=True)
        except sq.IntegrityError:
            raise UserExistsError(f"Пользователь {username.capitalize()} уже существует!")

        return self.cursor.lastrowid

    def get_user(self, username: str) -> dict | None:
        """
            Получает информацию о пользователе из базы данных.

            Args:
                username (str): Имя пользователя, информацию о котором нужно получить.

            Returns:
                dict | None: Возвращает информацию о пользователе в виде словопря, если пользователь существует.

            Keys:
            'id';'username';'password';'role';'balance';'created_at';'updated_at'

            Raises:
                UserNotFoundError: Если пользователь с указанным именем не найден в базе данных.
        """

        query = """SELECT id, username, password, role, balance, created_at, updated_at FROM users WHERE username = ?"""
        self.execute_query(query, (username,))

        user = self.cursor.fetchone()

        if not user:
            raise UserNotFoundError(f'Пользователь с username "{username}" не существует!')

        user = dict(user)
        user_id = user.pop('id')
        user['user_id'] = user_id

        return user

    def update_user_balance(self, user_id: int, new_balance: float):
        """
        Обновляет баланс пользователя.

        Args:
            user_id (int): ID пользователя, чей баланс необходимо обновить.
            new_balance (float): Новое значение баланса для пользователя.

        Returns: None

        Raises:
            UserBalanceUpdateError: Если произошла ошибка при обновлении баланса пользователя.
        """

        query = """
        UPDATE users
        SET balance = ?
        WHERE id = ?
        """

        try:
            self.execute_query(query, (new_balance, user_id), is_commit=True)
        except sq.Error as e:
            raise UserBalanceUpdateError(f"Ошибка при обновлении баланса пользователя с ID {user_id}: {e}")

    def delete_user(self, user_id: int):
        """
        Удаляет пользователя из базы данных.

        Args:
            user_id (int): ID пользователя, которого необходимо удалить.

        Returns: None
        """
        query = """
        DELETE FROM users
        WHERE id = ?
        """

        try:
            self.execute_query(query, (user_id,), is_commit=True)
        except sq.Error as e:
            raise UserNotFoundError(f"Ошибка при удалении пользователя с ID {user_id}: {e}")

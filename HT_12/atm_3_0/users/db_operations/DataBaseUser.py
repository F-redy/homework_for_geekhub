from HT_12.atm_3_0.BaseDataBase import BaseDataBase, sq
from HT_12.atm_3_0.custom_exceptions.users_exceptions import (
    UserBalanceUpdateError, UserExistsError, UserNotFoundError)


class DataBaseUser(BaseDataBase):
    def add_user(self, username: str, hashed_password: str, role: str, balance: int) -> int | None:
        """
            Создает нового пользователя в базе данных.

            Args:
                username (str): Имя пользователя.
                hashed_password (str): Захешированный пароль с использованием алгоритма hashlib.sha256.
                role (str, optional): Роль пользователя. (user или collector)
                balance (int): Стартовый балас пользователя.

            Returns:
                int | None: Возвращает идентификатор (ID) только что созданного пользователя в базе данных (lastrowid),
                        если пользователь успешно создан, в противном случае возвращает None.

            Raises:
                UserExistsError: Если пользователь с таким именем уже существует в базе данных.
        """
        query = """INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)"""

        try:
            self._execute_query(query, (username, hashed_password, role, balance), is_commit=True)
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
        self._execute_query(query, (username,))

        user = self.cursor.fetchone()

        if not user:
            raise UserNotFoundError(f'Пользователь с username "{username}" не существует!')

        user = dict(user)
        user_id = user.pop('id')
        user['user_id'] = user_id

        return user

    def update_user_balance(self, user_id: int, new_balance: int):
        """
        Обновляет баланс пользователя.

        Args:
            user_id (int): ID пользователя, чей баланс необходимо обновить.
            new_balance (int): Новое значение баланса для пользователя.

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
            self._execute_query(query, (new_balance, user_id), is_commit=True)
        except sq.Error as e:
            raise UserBalanceUpdateError(f"Ошибка при обновлении баланса пользователя с ID {user_id}: {e}")

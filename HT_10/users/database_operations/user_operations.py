from HT_10.database_operations import sq
from HT_10.users.custom_exceptions import UserBalanceUpdateError
from HT_10.users.custom_exceptions import UserExistsError
from HT_10.users.custom_exceptions import UserNotFoundError
from HT_10.users.database_operations.transaction_operations import create_user_transaction


def add_user(connect: sq.Connection, username: str, hashed_password: str, role: str,
             balance: float = 0.0) -> int | None:
    """
        Создает нового пользователя в базе данных.

        Args:
            connect (sqlite3.Connection): Объект соединения с базой данных.
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
    cursor = connect.cursor()

    try:
        cursor.execute(query, (username, hashed_password, role, balance))
        connect.commit()
        create_user_transaction(connect, cursor.lastrowid, 'registration', balance)
    except sq.IntegrityError:
        raise UserExistsError(f"Пользователь {username.capitalize()} уже существует!")

    return cursor.lastrowid


def get_user(connect: sq.Connection, username: str) -> dict | None:
    """
        Получает информацию о пользователе из базы данных.

        Args:
            connect (sqlite3.Connection): Объект соединения с базой данных.
            username (str): Имя пользователя, информацию о котором нужно получить.

        Returns:
            dict | None: Возвращает информацию о пользователе в виде словопря, если пользователь существует.

        Keys:
        'id';'username';'password';'role';'balance';'created_at';'updated_at'

        Raises:
            UserNotFoundError: Если пользователь с указанным именем не найден в базе данных.
    """

    query = """SELECT id, username, password, role, balance, created_at, updated_at FROM users WHERE username = ?"""
    cursor = connect.cursor()

    user = cursor.execute(query, (username,)).fetchone()

    if not user:
        raise UserNotFoundError(f'Пользователь с username "{username}" не существует!')

    return dict(user)


def update_user_balance(connect: sq.Connection, user_id: int, new_balance: float) -> bool:
    """
    Обновляет баланс пользователя.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        user_id (int): ID пользователя, чей баланс необходимо обновить.
        new_balance (float): Новое значение баланса для пользователя.

    Returns:
        bool: Возвращает True, если обновление баланса выполнено успешно.

    Raises:
        UserBalanceUpdateError: Если произошла ошибка при обновлении баланса пользователя.
    """

    query = """
    UPDATE users
    SET balance = ?
    WHERE id = ?
    """
    cursor = connect.cursor()

    try:
        cursor.execute(query, (new_balance, user_id))
        connect.commit()
        return True
    except sq.Error as e:
        connect.rollback()
        raise UserBalanceUpdateError(f"Ошибка при обновлении баланса пользователя с ID {user_id}: {e}")


def delete_user(connect: sq.Connection, user_id: int) -> bool:
    """
    Удаляет пользователя из базы данных.

    Args:
        connect (sqlite3.Connection): Объект соединения с базой данных.
        user_id (int): ID пользователя, которого необходимо удалить.

    Returns:
        bool: Возвращает True, если пользователь успешно удален, иначе False.
    """
    query = """
    DELETE FROM users
    WHERE id = ?
    """
    cursor = connect.cursor()

    try:
        cursor.execute(query, (user_id,))
        connect.commit()

    except sq.Error as e:
        connect.rollback()
        raise UserNotFoundError(f"Ошибка при удалении пользователя с ID {user_id}: {e}")

    return True

from HT_10.database_operations import sq


def create_user_transaction(connect: sq.Connection, user_id: int, type_transaction: str, amount: int | float = None):
    """
        Создает транзакцию пользователя.

        Args:
            connect (sqlite3.Connection): Объект соединения с базой данных.
            user_id (int): ID пользователя, для которого создается транзакция.
            type_transaction (str): Тип транзакции, может быть 'deposit' или 'withdrawal' или 'registration'.
            amount (int | float): Сумма транзакции.

        Returns:
            None

        Note:
            type_transaction:
            Должно быть 'deposit' для пополнения или 'withdrawal' для снятия или registration при регистрации.
    """

    query = """INSERT INTO transactions (user_id, type_transaction, amount) VALUES (?,?,?)"""
    cursor = connect.cursor()

    cursor.execute(query, (user_id, type_transaction, amount))
    connect.commit()


def get_user_transactions(connect: sq.Connection, user_id: int) -> list[sq.Row]:
    """
        Получает все транзакции пользователя из базы данных.

        Args:
            connect (sqlite3.Connection): Объект соединения с базой данных.
            user_id (int): ID пользователя, транзакции которого необходимо получить.

        Returns:
            list[sqlite3.Row]: Транзакций пользователя из базы данных, отсортированный по времени создания
                                в порядке убывания (от последней к первой).

        Keys: 'id';'user_id';'type_transaction';'amount';'created_at'
    """

    query = """
    SELECT id, user_id, type_transaction, amount, created_at
    FROM transactions
    WHERE user_id = ?
    ORDER BY created_at DESC
    """
    cursor = connect.cursor()

    all_user_transactions = cursor.execute(query, (user_id,)).fetchall()

    return all_user_transactions

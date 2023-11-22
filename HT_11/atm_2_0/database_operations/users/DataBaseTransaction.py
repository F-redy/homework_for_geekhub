from HT_11.atm_2_0.database_operations.BaseDataBase import BaseDataBase


class DataBaseTransaction(BaseDataBase):

    def create_user_transaction(self, user_id: int, type_transaction: str, amount: int | float = None):
        """
            Создает транзакцию пользователя.

            Args:
                user_id (int): ID пользователя, для которого создается транзакция.
                type_transaction (str): Тип транзакции, может быть 'deposit' или 'withdrawal' или 'registration'.
                amount (int | float): Сумма транзакции.


            Note:
                type_transaction:
                Должно быть 'deposit или 'withdrawal' или 'registration' или 'bonus'.
        """

        query = """INSERT INTO transactions (user_id, type_transaction, amount) VALUES (?,?,?)"""
        self.execute_query(query, (user_id, type_transaction, amount), is_commit=True)

    def get_user_transactions(self, user_id: int) -> list:
        """
            Получает все транзакции пользователя из базы данных.

            Args:
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
        self.execute_query(query, (user_id,))
        return self.cursor.fetchall()

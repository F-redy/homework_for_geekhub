from HT_11.atm_2_0.custom_exceptions.atm_exceptions import ATMError
from HT_11.atm_2_0.database_operations.BaseDataBase import BaseDataBase, sq


class DataBaseATM(BaseDataBase):
    def create_atm(self) -> int | None:
        query = """INSERT INTO atm DEFAULT VALUES"""

        try:
            self.execute_query(query, is_commit=True)
            print(f'Новый банкомат c ID {self.cursor.lastrowid} создан')
        except sq.Error as e:
            raise ATMError(f"Ошибка при создании банкомата: {e}")

        return self.cursor.lastrowid

    def get_atm(self, atm_id: int) -> sq.Row | None:
        """'keys: id', 'created_at', 'updated_at'"""

        query = """
        SELECT id, created_at, updated_at
        FROM atm
        WHERE id = ?
        """
        self.execute_query(query, (atm_id,))
        atm = self.cursor.fetchone()

        if not atm:
            raise ATMError(f'Банкомат с ID {atm_id} не найден.')

        return atm

    def delete_atm(self, id_atm: int):
        query = """DELETE FROM atm WHERE id = ?"""

        try:
            self.execute_query(query, (id_atm,), is_commit=True)
            print(f'Банкомат под номером {id_atm} - был успешно удален.')
        except sq.Error as e:
            raise sq.Error(f"Ошибка при удалении банкомата: {e}")

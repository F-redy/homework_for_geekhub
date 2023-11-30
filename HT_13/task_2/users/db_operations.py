import sqlite3

from HT_13.task_2.users.custom_exceptions import (CheckoutBookError,
                                                  UserExistsError,
                                                  UserNotFoundError)


class DBUserManager:
    def __init__(self, db):
        self.db = db

    def add_user(self, name: str, hashed_password: str, role: str) -> int | None:
        """ Создает нового пользователя в базе данных. """
        query = """INSERT INTO users (name, password, role) VALUES ( ?, ?, ?)"""

        try:
            self.db.execute_query(query, (name, hashed_password, role), is_commit=True)
        except sqlite3.IntegrityError:
            raise UserExistsError(f"Пользователь с {name} уже существует!")

        return self.db.cursor.lastrowid

    def get_user(self, name: str) -> dict | None:
        """ Получает информацию о пользователе из базы данных. """

        query = """SELECT id, name, password, role, created_at FROM users WHERE name = ?"""
        self.db.execute_query(query, (name,))

        user = self.db.cursor.fetchone()

        if not user:
            raise UserNotFoundError(f'Пользователь с именем "{name}" не существует!')

        user = dict(user)
        user_id = user.pop('id')
        user['user_id'] = user_id

        return user

    def checkout_book(self, user_id, book_id):

        query = """INSERT INTO library_cards (status, book_id, user_id) VALUES (?, ?, ?)"""

        try:
            self.db.execute_query(query, ('взял', book_id, user_id), is_commit=True)
        except sqlite3.IntegrityError:
            raise CheckoutBookError('\nВы уже взяли эту книгу ранее.')

    def checkout_or_return_book(self, status, user_id, book_id):
        query = """
        UPDATE library_cards
        SET status = ?
        WHERE user_id = ? AND book_id = ?
        """

        self.db.execute_query(query, (status, user_id, book_id), is_commit=True)

    def get_status_user_book(self, user_id, book_id):
        select_query = """
            SELECT id, status, book_id, created_at, created_at, updated_at
            FROM library_cards
            WHERE user_id = ? AND book_id = ?
            """
        self.db.execute_query(select_query, (user_id, book_id))
        status = self.db.cursor.fetchone()
        if status:
            return status

    def check_user_debts(self, user_id: int):
        query = """
                SELECT books.title, books.author, categories.title as category, library_cards.updated_at
                FROM library_cards
                INNER JOIN books ON library_cards.book_id = books.id
                INNER JOIN categories ON books.category_id = categories.id
                WHERE library_cards.user_id = ? AND library_cards.status = 'взял'
                ORDER BY library_cards.updated_at DESC
            """
        self.db.execute_query(query, (user_id,))
        return self.db.cursor.fetchall()

    def get_all_user_history(self, user_id: int):
        query = "SELECT status, book_id, user_id FROM library_cards WHERE user_id = ?"
        try:
            self.db.cursor.execute(query, (user_id,))
        except sqlite3.Error as e:
            print(f'\nОшибка получения истории: {e}')

        histories = self.db.cursor.fetchall()
        return [dict(history) for history in histories]

    def check_all_user_debts(self):
        query = """
            SELECT users.name, users.role, users.created_at,
                   books.title, books.author, categories.title AS category, library_cards.updated_at
            FROM library_cards
            JOIN users ON library_cards.user_id = users.id
            JOIN books ON library_cards.book_id = books.id
            JOIN categories ON books.category_id = categories.id
            WHERE library_cards.status = 'взял'
            ORDER BY users.name
            """
        self.db.execute_query(query)
        results = self.db.cursor.fetchall()
        if results:
            return [dict(result) for result in results]

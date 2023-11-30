import sqlite3


class DBBookManager:
    def __init__(self, db):
        self.db = db

    def add_book(self, title, author, category_id):
        try:
            query = """INSERT INTO books (title, author, category_id) VALUES (?, ?, ?)"""
            self.db.execute_query(query, (title, author, category_id), is_commit=True)
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError('\nТакая книга уже есть')

    def get_book(self, title, author, category_id):
        query = """
        SELECT id, title, author,  category_id
        FROM books
        WHERE (title = ? OR author = ?) AND category_id = ?
        """
        self.db.execute_query(query, (title, author, category_id))
        book = self.db.cursor.fetchone()
        if book is None:
            raise ValueError('\nТакой книги не найдено.')
        return dict(book)

    def get_all_book(self):
        query = """
        SELECT books.title, books.author,  categories.title AS category
        FROM books
        JOIN categories ON books.category_id = categories.id
        ORDER BY category
        """
        self.db.execute_query(query)
        books = self.db.cursor.fetchall()
        if books:
            return books

    def update_book(self, title, author, category):
        ...

    def delete_book(self, book_id):
        query = """DELETE FROM books WHERE id = ?"""
        self.db.execute_query(query, (book_id,), is_commit=True)

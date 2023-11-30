class DBCategoryManager:
    def __init__(self, db):
        self.db = db

    # CATEGORIES
    def add_new_category(self, title):
        query = """INSERT INTO categories (title) VALUES (?)"""
        self.db.execute_query(query, (title,), is_commit=True)

    def get_category(self, title):
        query = """SELECT id, title FROM categories WHERE title = ?"""
        self.db.execute_query(query, (title,))
        category = self.db.cursor.fetchone()
        if not category:
            raise ValueError('\nТакой категории нет.')
        return dict(category)

    def get_all_categories(self):
        query = """SELECT title FROM categories"""
        self.db.execute_query(query)
        categories = self.db.cursor.fetchall()
        if categories:
            return categories

    def update_category(self, title, category_id):
        query = """
        UPDATE categories
        SET title = ?
        WHERE id = ?"""

        self.db.execute_query(query, (title, category_id), is_commit=True)

    def delete_category(self, category_id):
        query = """DELETE FROM categories WHERE id = ?"""
        self.db.execute_query(query, (category_id,), is_commit=True)

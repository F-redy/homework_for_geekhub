class Category:
    def __init__(self, db, title):
        self.db = db
        self.title = self.__validate_title(title)

    def __str__(self):
        return f'Category: {self.title}'

    @staticmethod
    def __validate_title(title) -> str | None:
        if not title:
            raise ValueError('\nНазвание категории не может быть пустой строкой\n')
        return title.lower()

    def add_new_category(self):
        self.db.add_new_category(self.title)

    def get_category(self):
        return self.db.get_category(self.title)

    def update_title_category(self, new_title):
        category = self.get_category()
        self.db.update_category(new_title.lower(), category['id'])

    def delete_category(self):
        category = self.get_category()
        self.db.delete_category(category['id'])


class Shelf:
    def __init__(self, category):
        self.category = category
        self.books = []

    def add_book(self, book):
        self.books.append(book)

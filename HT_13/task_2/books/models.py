from HT_13.task_2.categories.models import Category


class BookValidator:

    @staticmethod
    def validate_title(title):
        if not title:
            raise ValueError('\nНазвание книги не может быть пустым.')
        return title

    @staticmethod
    def validate_author(author):
        if not isinstance(author, Author):
            raise ValueError('\nauthor должен быть экземпляром класса Author')
        return author

    @staticmethod
    def validate_category(category):
        if not isinstance(category, Category):
            raise ValueError('\ncategory должна быть экземпляром класса Category')
        return category


class Book(BookValidator):
    def __init__(self, db, title, author, category):
        self.db = db
        self.title = self.validate_title(title)
        self.author = self.validate_author(author)
        self.category = self.validate_category(category)

    def __str__(self):
        return f'Книга: {self.title} | {self.author} | {self.category}'

    def create_book(self):
        cat = self.db.get_category(self.category.title.lower())
        self.db.add_book(self.title.lower(), self.author.name.lower(), category_id=cat['id'])
        return True

    def get_book(self):
        cat = self.db.get_category(self.category.title)
        book = self.db.get_book(self.title, self.author.name, cat['id'])
        if book:
            return book

    def delete_book(self):
        book = self.get_book()
        if book:
            self.db.delete_book(book['id'])
            return True


class Author:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Author:  {self.name.capitalize()}'

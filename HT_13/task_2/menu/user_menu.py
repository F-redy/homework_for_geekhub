import sqlite3

from HT_13.task_2.books.models import Author
from HT_13.task_2.books.models import Book
from HT_13.task_2.categories.models import Category
from HT_13.task_2.menu.utils import get_user_choose_menu
from HT_13.task_2.users.custom_exceptions import CheckoutBookError
from HT_13.task_2.users.custom_exceptions import IncorrectPasswordError
from HT_13.task_2.users.custom_exceptions import UserNotFoundError
from HT_13.task_2.users.custom_exceptions import ValidationError
from HT_13.task_2.users.models import Person


class UserMenu:
    MENU = [
        '\nВыберите действие:',
        'Авторизация',
        'Регистрация',
        'Выход\n',
    ]

    USER_MENU = [
        '\nВыберите действие:',
        'Взять книгу',
        'Вернуть книгу',
        'Посмотреть какие книги надо вернуть',
        'Посмотреть все книги',
        'Выход\n',
    ]

    LIBRARIAN_MENU = [
        'Посмотреть всех должников',
        'Добавить новую книгу',
        'Удалить книгу',
        'Добавить новую категорию',
        'Посмотреть все категории'
    ]

    def __init__(self, db):
        self.db = db
        self.user_model = None

    def login(self):
        user = None
        while user is None:
            try:
                entered_name = input('Введите имя пользователя: ')
                entered_password = input('Введите пароль пользователя: ')
                user = Person(self.db).login(entered_name, entered_password)
            except (ValidationError, IncorrectPasswordError, UserNotFoundError) as e:
                print(e)

        self.user_model = user
        print(f'\nДобро пожаловать {self.user_model.name}')
        return user

    def registration_user(self):
        roles_menu = ['Укажите ваш статус: ', '1. Студент', '2. Учитель', '3. Библиотекарь']
        roles = ['студент', 'учитель', 'библиотекарь']
        user = None
        while user is None:
            try:
                entered_username = input('Введите имя пользователя: ')
                entered_password = input('Введите пароль пользователя: ')
                entered_role = roles[int(get_user_choose_menu(roles_menu))]

                user = Person(self.db).registration(entered_username, entered_password, entered_role)
            except ValidationError as e:
                print(e)

        self.user_model = user
        print(f'\nДобро пожаловать {self.user_model.name}')
        return user

    def get_user(self):
        user_input = get_user_choose_menu(menu=self.MENU)

        while self.user_model is None:

            match user_input:
                case '1':
                    self.user_model = self.login()
                case '2':
                    self.user_model = self.registration_user()
                case '3':
                    return

    def user_input_book(self):
        book = None
        while book is None:
            try:
                entered_title = input('Введите название книги: ')
                entered_author = input('Введите автора книг: ')
                entered_category = input('Введите категорию книги: ')
                book = Book(self.db,
                            entered_title,
                            Author(entered_author),
                            Category(self.db, entered_category)
                            )

            except ValidationError as e:
                print(e)

        return book

    def get_book(self):
        book = self.user_input_book()
        if book:
            try:
                book = book.get_book()
                if self.user_model.get_book(book['id']):
                    print(f'\nКнига: {book["title"]}\nБыла выдана пользователю {self.user_model.name}\n')
            except (CheckoutBookError, ValueError) as e:
                print(e)

        return book

    def return_book(self):
        book = self.user_input_book()
        if book:
            try:
                book = book.get_book()
            except ValueError as e:
                print(e)
                return
        if book and self.db.get_status_user_book(self.user_model.user_id, book['id']):

            if self.user_model.return_book(book['id']):
                print(f'\nВы вернули книгу: {book["title"]}\n')
        else:
            print('\nВы не брали эту книгу.\n')

    def create_book(self):
        book = self.user_input_book()
        if book:
            try:
                if book.create_book():
                    print('\nНовая книга была создана\n')
            except sqlite3.IntegrityError as e:
                print(e)

    def delete_book(self):
        book = self.user_input_book()
        if book:
            if book.delete_book():
                print('\nКнига успешно удалена.\n')

    def create_category(self):
        while True:
            try:
                title = input('\nВведите название категории: ')
                cat = Category(self.db, title)
                cat.add_new_category()
                print('\nНовая категория была создана.\n')
                return
            except ValueError as e:
                print(e)
            except sqlite3.IntegrityError:
                print('\nТакая категория уже есть.\n')

    def show_all_books(self):
        books = self.db.get_all_book()
        if books:
            print(f'\n{"-" * 60}\nВсе книги:\n')
            for book in books:
                print(f'Название {book["title"]} | Автор: {book["author"]} | Категория: {book["category"]}')
            print(f'\n{"-" * 60}\n')

    def show_all_categories(self):
        categories = self.db.get_all_categories()
        if categories:
            print(f'\n{"-" * 40}\nВсе категории:\n')
            for category in categories:
                print(category['title'])
            print(f'\n{"-" * 40}\n')

    def check_user_debts(self):
        debts = self.user_model.check_user_debts()
        if debts:

            for indx, debt in enumerate(debts, 1):
                print(f'\n{"-" * 60}'
                      f'\nКнига №{indx}:'
                      f'\nНазвание: "{debt["title"]}"'
                      f'\nАвтор: "{debt["author"]}"'
                      f'\nКатегория: "{debt["category"]}"'
                      f'\nВыдана: "{debt["updated_at"]}"'
                      f'\n{"-" * 60}'
                      )
        else:
            print('\nУ вас нет долгов по книгам.\n')

    def user_menu(self):
        choose_menu = self.USER_MENU
        dict_functions = {
            '1': self.get_book,
            '2': self.return_book,
            '3': self.check_user_debts,
            '4': self.show_all_books,
            '5': exit
        }
        if not self.user_model:
            return

        match self.user_model.role:
            case 'студент':
                ...

            case 'учитель':
                ...

            case 'библиотекарь':
                choose_menu = self.USER_MENU[:-1] + [item for item in self.LIBRARIAN_MENU] + self.USER_MENU[-1:]
                dict_functions = {
                    '1': self.get_book,
                    '2': self.return_book,
                    '3': self.check_user_debts,
                    '4': self.show_all_books,
                    '5': self.user_model.check_all_user_debts,
                    '6': self.create_book,
                    '7': self.delete_book,
                    '8': self.create_category,
                    '9': self.show_all_categories,
                    '10': exit
                }

        while True:
            user_input = get_user_choose_menu(choose_menu)
            res = dict_functions.get(user_input, '')
            if res and callable(res):
                res()
            else:
                print(res)

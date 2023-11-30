if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[2]))

import sqlite3
from random import randint

from HT_13.task_2.books.db_operations import DBBookManager
from HT_13.task_2.books.models import Author
from HT_13.task_2.categories.db_operations import DBCategoryManager
from HT_13.task_2.db_base import DBManager
from HT_13.task_2.menu.user_menu import UserMenu
from HT_13.task_2.users.db_operations import DBUserManager
from HT_13.task_2.users.models import Person


class CombinedDBManager(DBUserManager, DBCategoryManager, DBBookManager):
    pass


def create_test_data(db_connect):
    users = [
        {'name': 'user_1', 'password': 'password_1', 'role': 'библиотекарь'},
        {'name': 'user_2', 'password': 'password_2', 'role': 'учитель'},
        {'name': 'user_3', 'password': 'password_3', 'role': 'студент'},
        {'name': 'user_4', 'password': 'password_4', 'role': 'студент'},
        {'name': 'user_5', 'password': 'password_5', 'role': 'студент'},
    ]

    person = Person(db_connect)
    try:
        for i in range(1, 11):
            db_connect.add_new_category(title=f'category_{i}')
        for user_data in users:
            person = person.registration(**user_data)
    except sqlite3.IntegrityError:
        pass

    for i in range(1, 101):
        cats = list(range(1, 11))
        numbers = list(range(1, 101))
        cat_id = cats[randint(0, len(cats) - 1)]
        db_connect.add_book(
            f'book_{numbers[randint(0, 99)]}',
            Author(f'author_{numbers[randint(0, 99)]}').name,
            category_id=cat_id)


def start():
    db = DBManager()
    db.connect_db()
    db_connect = CombinedDBManager(db)

    # create_test_data(db_connect)

    menu = UserMenu(db_connect)
    menu.get_user()
    menu.user_menu()


if __name__ == '__main__':
    start()

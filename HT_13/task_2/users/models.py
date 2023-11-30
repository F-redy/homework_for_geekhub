from HT_13.task_2.users.custom_exceptions import IncorrectPasswordError
from HT_13.task_2.users.utils import hash_password
from HT_13.task_2.users.validators import UserValidator


class Person(UserValidator):
    def __init__(self, db):
        self.db = db
        self.user_id = None
        self.name = None
        self.password = None
        self.role = None
        self.created_at = None

    def __str__(self):
        return (f'\nName: {self.name}'
                f'\nRole: {self.role}'
                f'\nRegistration: {self.created_at}')

    def registration(self, name: str, password: str, role: str):
        self.name = self.validate_name(name)
        self.password = hash_password(self.validate_password(password))
        self.role = self.validate_role(role)

        self.db.add_user(name=self.name, hashed_password=self.password, role=self.role)
        return self.login(self.name, password)

    def login(self, name: str, password: str):
        name = self.validate_name(name)
        hashed_password = hash_password(password)

        user = self.db.get_user(name=name)
        if user['password'] != hashed_password:
            raise IncorrectPasswordError('Не правильный пароль')

        return self.create_user_model(user_data=user)

    def create_user_model(self, user_data):
        match user_data['role']:
            case 'учитель':
                return Teacher(self.db, user_data)
            case 'студент':
                return Student(self.db, user_data)
            case 'библиотекарь':
                return Librarian(self.db, user_data)
            case _:
                raise ValueError('Недопустимая роль пользователя')

    def get_book(self, book_id: int):
        status = self.db.get_status_user_book(self.user_id, book_id)
        if status and status['status'] == 'вернул':
            self.db.checkout_or_return_book('взял', self.user_id, book_id)
        else:
            self.db.checkout_book(self.user_id, book_id)
        return True

    def return_book(self, book_id: int):
        self.db.checkout_or_return_book('вернул', self.user_id, book_id)
        return True

    def check_user_debts(self):
        return self.db.check_user_debts(self.user_id)


class Teacher(Person):
    def __init__(self, db, user_data):
        super().__init__(db)
        self.user_id = user_data['user_id']
        self.name = user_data['name']
        self.password = user_data['password']
        self.role = user_data['role']
        self.created_at = user_data['created_at']

    def write_book(self, title: str, author: str, category: str):
        ...


class Student(Person):
    def __init__(self, db, user_data):
        super().__init__(db)
        self.user_id = user_data['user_id']
        self.name = user_data['name']
        self.password = user_data['password']
        self.role = user_data['role']
        self.created_at = user_data['created_at']


class Librarian(Person):
    def __init__(self, db, user_data):
        super().__init__(db)
        self.user_id = user_data['user_id']
        self.name = user_data['name']
        self.password = user_data['password']
        self.role = user_data['role']
        self.created_at = user_data['created_at']

    def add_book_to_library(self, title: str, author: str, category_id: int):
        ...

    def remove_book_from_library(self, title: str, author: str, category_id: int):
        ...

    def update_book_info(self, title: str, author: str, category_id: int):
        self.db.add_book()

    def check_all_user_debts(self):
        all_user_debts = self.db.check_all_user_debts()

        if all_user_debts:
            print(f'\n{"*" * 120}')
            data_debts = {}
            for data in all_user_debts:
                headers = ['Название: ', 'Автор: ', 'Категория: ', 'Взята: ']
                values = [data['title'], data['author'], data['category'], data['updated_at']]
                data_debts.setdefault(
                    f'Имя: {data["name"]} | Статус:  {data["role"]} | Дата регистрации: {data["created_at"]}',
                    []).append(' | '.join(f"{head}{value}" for head, value in zip(headers, values)))

            for user_info, books in data_debts.items():
                print(f'{user_info}\nКниги:')
                for book in books:
                    print(book)

                print('-' * 120)
        print(f'\n{"*" * 120}\n')

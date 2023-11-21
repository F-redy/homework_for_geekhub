# 2. Створити клас Person, в якому буде присутнім метод __init__ який буде приймати якісь аргументи,
# які зберігатиме в відповідні змінні.
# - Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
# - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession
# (його не має інсувати під час ініціалізації).

class Person:
    def __init__(self, name: str, sex: str, age: int):
        self.name = name
        self.sex = sex
        self.age = age

    def print_name(self):
        print(f'Name: {self.name}')

    def print_sex(self):
        print(f'Sex: {self.sex}')

    def show_age(self):
        print(f'Age: {self.age}')

    def show_all_information(self):
        self.print_name()
        self.print_sex()
        self.show_age()


if __name__ == '__main__':

    person_1 = Person('Эмилия', 'Female', 21)
    person_2 = Person('Лукас', 'Male', 75)

    data = [
        (person_1, 'Садовник'),
        (person_2, 'Архитектор')
    ]

    for i, (person, profession) in enumerate(data, start=1):
        print('-' * 50)
        person.show_all_information()
        print(f'before: attribute "profession" in person_{i}: {hasattr(person, "profession")}')
        person.profession = profession
        print(f'after: attribute "profession" in person_{i}: {person.profession}')

# task 3.
# Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.

class Counter:
    __COUNT = 0

    def __new__(cls, *args, **kwargs):
        cls.__COUNT += 1
        return cls

    @classmethod
    def show_counter(cls):
        print(cls.__COUNT)


if __name__ == '__main__':
    obj_1 = Counter()
    obj_2 = Counter()
    obj_3 = Counter()

    obj_1.show_counter()
    Counter.show_counter()

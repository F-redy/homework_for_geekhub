# task 3.
# Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.

class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1


if __name__ == '__main__':
    obj_1 = Counter()
    obj_2 = Counter()
    obj_3 = Counter()

    print(obj_1.count)
    print(obj_2.count)
    print(obj_3.count)

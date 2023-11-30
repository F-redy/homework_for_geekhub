# task 4.
# Create 'list'-like object, but index starts from 1 and index of 0 raises error.
# Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
# але індексація повинна починатись із 1

class CustomList(list):
    def __getitem__(self, item):
        if not item:
            raise IndexError('Бо не можна!')
        return super().__getitem__(item - 1)


if __name__ == '__main__':
    lst = CustomList(range(20))
    print(lst)
    tmp = lst.pop()
    lst[5] = 'халабуда'
    print(lst)
    lst[0] = tmp
    print(lst)
    lst[5] = lst.pop(7)
    print(lst)
    try:
        print(lst[0])
    except IndexError as e:
        print(e)

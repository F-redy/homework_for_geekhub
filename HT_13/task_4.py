# task 4.
# Create 'list'-like object, but index starts from 1 and index of 0 raises error.
# Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
# але індексація повинна починатись із 1

class CustomList(list):
    def __getitem__(self, index):
        if not index:
            raise IndexError('Call __getitem__. Бо не можна!')
        return super().__getitem__((index, index - 1)[index > 0])

    def __setitem__(self, index, value):
        if not index:
            raise IndexError('Call __setitem__. Бо не можна!')
        return super().__setitem__((index, index - 1)[index > 0], value)

    def __delitem__(self, index):
        if not index:
            raise IndexError('Call __delitem__. Бо не можна!')
        return super().__delitem__((index, index - 1)[index > 0])


if __name__ == '__main__':
    lst = CustomList(range(20))
    print(lst)
    print(lst[-1])
    tmp = lst.pop()
    lst[5] = 'халабуда'
    print(lst)
    lst[5] = lst.pop(7)
    print(lst)
    lst.insert(-1, 20)
    print(lst)
    try:
        print(lst[0])
    except IndexError as e:
        print(e)
    try:
        lst[0] = tmp
    except IndexError as e:
        print(e)
    try:
        del lst[0]
    except IndexError as e:
        print(e)
    print(lst)
    print(len(lst))

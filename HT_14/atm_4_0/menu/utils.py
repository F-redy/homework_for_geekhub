def print_menu(memu):
    for item in memu:
        print(item)


def get_user_choose_menu(menu):
    while True:
        print_menu(menu)
        user_input = input('Введите ваш выбор: ')
        if user_input in map(str, range(1, len(menu))):
            return user_input
        else:
            print('\nНе правильный выбор.')
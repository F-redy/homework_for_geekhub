def print_menu(memu):
    for indx, item in enumerate(memu[1:], 1):
        print(f'{indx}. {item}')


def get_user_choose_menu(menu):
    while True:
        print_menu(menu)
        user_input = input('Введите ваш выбор: ')
        if user_input in map(str, range(1, len(menu) + 1)):
            return user_input

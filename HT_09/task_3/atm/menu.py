USER_MENU = [
    '1. Авторизація',
    '2. Реєстрація',
]

ATM_MENU = [
    '1. Продивитись баланс',
    '2. Поповнити баланс',
    '3. Зняти кошти',
    '4. Вихід',
]


def menu(atm_menu: bool = False):
    lst = USER_MENU

    if atm_menu:
        lst = ATM_MENU

    message = 'Введіть дію(цифрою): \n' + '\n'.join(lst)
    keys = list(map(str, range(1, len(lst) + 1)))

    user_input = input(f'\n{message}\n')

    while user_input not in keys:
        user_input = input(f'\nНе вірний вибір\n\n{message}\n')

    return user_input

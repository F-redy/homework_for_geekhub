from HT_10.atm.views import change_atm_balance
from HT_10.atm.views import get_atm_info


def print_menu(memu):
    for item in memu:
        print(item)


def get_user_choose_menu(menu):
    while True:
        print_menu(menu)
        user_input = input('Введите ваш выбор: ')
        if user_input in map(str, range(1, len(menu) + 1)):
            return user_input


def withdrawal_user_balance(connect, atm: dict):
    new_balance_atm = atm['balance']
    change_atm_balance(connect, atm['id'], new_balance_atm)
    atm = get_atm_info(connect, atm['id'])
    return atm

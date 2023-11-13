if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent.parent))

from HT_09.task_3.atm.menu import menu
from HT_09.task_3.atm.view import login, registration
from HT_09.task_3.users.view import register_user
from HT_09.task_3.wallet.database_operations import get_user_balance
from HT_09.task_3.wallet.validators import validate_transaction_input
from HT_09.task_3.wallet.view import add_user_balance, sub_user_balance


def create_base_client():
    """ Registration of test users """
    users = [
        {'username': 'user_1', 'password': 'password_1', 'start_amount': 1200},
        {'username': 'user_2', 'password': 'password_2', 'start_amount': 12000},
        {'username': 'user_3', 'password': 'password_3', 'start_amount': 700},
        {'username': 'user_4', 'password': 'password_4'}
    ]

    for user in users:
        register_user(**user, silence=True)


def start():
    create_base_client()
    user_input = menu()

    if user_input == '1':
        user = login()
    else:
        user = registration()

    if user:
        while True:
            user_input = menu(atm_menu=True)

            if user_input == '4':
                print('Роботу завершено.')
                return 'Роботу завершено.'

            if user_input == '1':
                print(f'Кошти на рахунку: {get_user_balance(user)}')

            if user_input in ('2', '3'):

                while True:
                    try:
                        transaction_amount = validate_transaction_input(input('\nВведіть сумму: '))
                        break
                    except ValueError as e:
                        print(e)

                if user_input == '2':
                    user = add_user_balance(user, transaction_amount)
                if user_input == '3':
                    user = sub_user_balance(user, transaction_amount)


if __name__ == '__main__':
    start()

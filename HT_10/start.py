if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))

from HT_10.atm.views import create_new_atm, get_atm_info
from HT_10.database_operations import connect_db, execute_sql_script
from HT_10.menu.collector_menu import CollectorMenu
from HT_10.menu.user_menu import UserMenu
from HT_10.menu.utils import get_user_choose_menu
from HT_10.users.custom_exceptions import UserExistsError
from HT_10.users.database_operations.user_operations import add_user
from HT_10.users.utils import hash_password


def create_base_users_and_admin(connect):
    users = [
        {'username': 'admin', 'hashed_password': hash_password('admin'), 'role': 'collector'},
        {'username': 'user_1', 'hashed_password': hash_password('password_1'), 'role': 'user'},
        {'username': 'user_2', 'hashed_password': hash_password('password_2'), 'role': 'user'},
        {'username': 'user_3', 'hashed_password': hash_password('password_3'), 'role': 'user'},
        {'username': 'user_4', 'hashed_password': hash_password('password_4'), 'role': 'user'},
        {'username': 'user_5', 'hashed_password': hash_password('password_5'), 'role': 'user'}
    ]
    for userdata in users:
        try:
            add_user(connect, **userdata)
        except UserExistsError:
            pass


def create_base_atm(connect):
    return create_new_atm(connect)['id']


def start(new_atm=False):
    connect = connect_db()
    execute_sql_script(connect)
    create_base_users_and_admin(connect)

    if new_atm:
        atm_id = create_base_atm(connect)
    else:
        atm_id = 1

    atm = get_atm_info(connect, atm_id)
    menu = UserMenu()
    menu_collector = CollectorMenu()

    user = menu.get_user(connect)
    if user is None:
        print('Работа завершена')
        return

    match user['role']:
        case 'collector':
            user_input = get_user_choose_menu(menu_collector.CHOOSE_MENU)
            if user_input == '1':
                menu_collector.collector_menu(connect, atm)
            else:
                menu.user_menu(connect, user, atm)
        case 'user':
            menu.user_menu(connect, user, atm)


if __name__ == '__main__':
    start(new_atm=False)

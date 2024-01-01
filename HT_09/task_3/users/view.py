from HT_09.task_3.users import custom_exceptions
from HT_09.task_3.users.database_operations import get_user
from HT_09.task_3.users.database_operations import read_users
from HT_09.task_3.users.database_operations import write_user
from HT_09.task_3.users.models import custom_user
from HT_09.task_3.users.validators import does_user_exist


def register_user(username: str, password: str, start_amount: int | float = 0.0, silence: bool = False) -> dict | None:
    """
    Register a new user with the provided username and password.

    Parameters:
    - username (str): The username for the new user.
    - password (str): The password for the new user.
    - start_amount (int or float, optional): The initial amount for the user's balance. Default is 0.0.
    - silence (bool, optional): If True, suppresses error messages and registration success message. Default is False.

    Returns:
    - dict or None: If the user is successfully registered, returns a dictionary with user information.
                   If the user already exists, returns None.

    Raises:
    - custom_exceptions.UserExistsError: Raised if the specified username already exists.
    """

    users = read_users()
    new_user = None

    try:
        does_user_exist(username, users)
        new_user = custom_user(username, password, start_amount)
    except custom_exceptions.UserExistsError as e:
        if not silence:
            print(e)

    if new_user:
        write_user(new_user)

        if not silence:
            print(f'Користувач {username} успішно зареєстрований!')

    return new_user


def authenticate_user(request: dict, entered_username: str, entered_password: str) -> dict:
    """
    Authenticate a user with the provided username and password.

    Parameters:
    - request (dict): A dictionary containing information about the authentication request.
    - entered_username (str): The username entered by the user for authentication.
    - entered_password (str): The password entered by the user for authentication.

    Returns:
    - dict: A dictionary containing updated information about the authentication request.
            It includes the authenticated user, error message, remaining attempts, and other details.

    Raises:
    - custom_exceptions.UserNotFoundError: Raised if the specified username is not found.
    - custom_exceptions.IncorrectPasswordError: Raised if the entered password is incorrect.
    """
    user = None
    error = ''
    attempts: int = request['attempts']
    attempts_break: int = request['attempts_break']

    try:
        user = get_user(entered_username, entered_password)
        request['authenticate'] = f'\nВітаю {user["username"]}'
    except custom_exceptions.UserNotFoundError as e:
        error = str(e)
    except custom_exceptions.IncorrectPasswordError as e:
        error = str(e)
        attempts_break -= 1

    attempts -= 1

    if attempts:
        message = f'\nЗалишилось {attempts} спроб{("а", "и")[attempts > 1]}.'
    else:
        message = '\nНевдала спроба авторизації. Сеанс завершено.'

    if not attempts_break:
        message = '\nЗафіксовано спробу злому!\nКартку заблоковано.Зверніться в службу підтримки.'

    request.update(
        {
            'user': user,
            'message': error + message,
            'attempts': attempts,
            'attempts_break': attempts_break
        }
    )
    return request

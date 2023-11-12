import csv

from HT_09.task_3 import settings
from HT_09.task_3.errors.models import ErrorLogger
from HT_09.task_3.users import custom_exceptions
from HT_09.task_3.users.utils import hash_password

logger = ErrorLogger()


def create_database_users():
    with open(settings.DATABASE_USERS, 'w') as file:
        csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)


def read_users() -> list[dict]:
    """ Read user data from the CSV file. """
    users = []
    try:
        with open(settings.DATABASE_USERS) as file:
            reader: csv.DictReader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)

            for row in reader:
                users.append(dict(row.items()))

    except FileNotFoundError:
        create_database_users()
    except csv.Error as e:
        error_message = f"Error reading CSV file: {str(e)}"
        logger.log_error(type(e).__name__, error_message)
        print(settings.CONTACT_SUPPORT)
        raise

    except ValueError as e:
        error_message = f"Error converting data: {str(e)}"
        logger.log_error(type(e).__name__, error_message)
        print(settings.CONTACT_SUPPORT)
        raise

    return users


def write_user(data_user):
    """ Write user data to the CSV file. """

    file_path = settings.DATABASE_USERS
    try:

        with open(file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data_user.keys(), quoting=csv.QUOTE_NONNUMERIC)

            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data_user)

    except FileNotFoundError:
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data_user.keys(), quoting=csv.QUOTE_NONNUMERIC)

            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data_user)

    except PermissionError as e:
        logger.log_error(type(e).__name__, f"Error: Permission denied - {file_path}")
        print(settings.CONTACT_SUPPORT)
        raise

    except csv.Error as e:
        logger.log_error(type(e).__name__, f"CSV Error: {str(e)}")
        print(settings.CONTACT_SUPPORT)
        raise

    return True


def get_user(username: str, password: str):
    """ Get user data """
    users = read_users()
    hashed_password = hash_password(password)

    for user in users:

        if user['username'] == username:
            if user['password_hash'] == hashed_password:
                return user
            else:
                raise custom_exceptions.IncorrectPasswordError('\nНе вірний пароль!')

    raise custom_exceptions.UserNotFoundError(f"\nКористувач {username} - не існує!")


if __name__ == "__main__":
    print(create_database_users())

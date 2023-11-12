from HT_09.task_3 import settings
from HT_09.task_3.users.custom_exceptions import (UserExistsError,
                                                  ValidationError)
from HT_09.task_3.users.utils import hash_password


def validate_username(username: str) -> str | None:
    """Validate the username."""

    letters = len(list(filter(str.isalpha, username)))
    digits = len(list(filter(str.isdigit, username)))

    if letters < digits:
        raise ValidationError("Некоректне ім'я користувача. Ім'я має складатися переважно з букв!")

    if len(username) < settings.MIN_LENGTH_USERNAME:
        raise ValidationError(f'Ім’я користувача має містити принаймні {settings.MIN_LENGTH_USERNAME} символів!')

    if len(username) > settings.MAX_LENGTH_USERNAME:
        raise ValidationError(f'Ім’я користувача має містити не більше {settings.MAX_LENGTH_USERNAME} символів!')
    return username


def validate_password(password: str) -> str | None:
    """Validate the password."""
    if not any(map(str.isdigit, password)):
        raise ValidationError('Пароль повинен містити хоча б одну цифру!')

    if len(list(filter(str.isalpha, password))) < settings.MIN_LETTERS_PASSWORD:
        raise ValidationError(f'Пароль має містити не менше {settings.MIN_LETTERS_PASSWORD} літер!')

    if len(password) < settings.MIN_LENGTH_PASSWORD:
        raise ValidationError(f'Пароль має містити принаймні {settings.MIN_LENGTH_PASSWORD} символів!')
    return hash_password(password)


def does_user_exist(username: str, users: list[dict]):
    for user in users:
        if username == user['username']:
            raise UserExistsError(f'{username} - вже існує!')

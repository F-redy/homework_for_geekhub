from HT_10.users.custom_exceptions import ValidationError
from HT_10.users.utils import hash_password

# users
ATTEMPTS = 3
MIN_LENGTH_USERNAME = 3
MAX_LENGTH_USERNAME = 20

MIN_LETTERS_PASSWORD = 1
MIN_LENGTH_PASSWORD = 8


def validate_username(username: str) -> str | None:
    """ Валидация username """

    letters = len(list(filter(str.isalpha, username)))
    digits = len(list(filter(str.isdigit, username)))

    if letters < digits:
        raise ValidationError('Неправильное имя пользователя. Имя должно состоять преимущественно из букв!')

    if len(username) < MIN_LENGTH_USERNAME:
        raise ValidationError(f'Имя пользователя должно содержать по крайней мере {MIN_LENGTH_USERNAME} символов!')

    if len(username) > MAX_LENGTH_USERNAME:
        raise ValidationError(f'Имя пользователя должно содержать не более {MAX_LENGTH_USERNAME} символов!')
    return username


def validate_password(password: str) -> str | None:
    """ Валидация password. """
    if not any(map(str.isdigit, password)):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру!')

    if len(list(filter(str.isalpha, password))) < MIN_LETTERS_PASSWORD:
        raise ValidationError(f'Пароль должен содержать не менее {MIN_LETTERS_PASSWORD} букв!')

    if len(password) < MIN_LENGTH_PASSWORD:
        raise ValidationError(f'Пароль должен содержать по крайней мере {MIN_LENGTH_PASSWORD} символов!')
    return hash_password(password)


def validate_role(role: str) -> str | None:
    allowed_roles = ('user', 'collector')
    if role not in allowed_roles:
        raise ValidationError(f'Неверное значение роли: {role}. Роль должна быть {" или ".join(allowed_roles)}.')
    return role


def validate_user_balance(value) -> float | None:
    """ Валидатор для balance """
    try:
        value = float(value)
    except ValueError:
        raise ValidationError('Значение должно быть числом.')

    if value < 0:
        raise ValidationError('Значение должно быть больше 0.')

    return value

from HT_11.atm_2_0.custom_exceptions import ValidationError


class UserValidator:
    __MIN_LENGTH_USERNAME = 3
    __MAX_LENGTH_USERNAME = 20

    __MIN_LETTERS_PASSWORD = 1
    __MIN_LENGTH_PASSWORD = 8

    __ALLOWED_ROLES = ('user', 'collector')

    @classmethod
    def validate_username(cls, username: str) -> str | None:
        """ Валидация username """

        letters = len(list(filter(str.isalpha, username)))
        digits = len(list(filter(str.isdigit, username)))

        if letters < digits:
            raise ValidationError('Неправильное имя пользователя. Имя должно состоять преимущественно из букв!')

        if len(username) < cls.__MIN_LENGTH_USERNAME:
            raise ValidationError(f'Имя пользователя должно содержать минимум {cls.__MIN_LENGTH_USERNAME} символов!')

        if len(username) > cls.__MAX_LENGTH_USERNAME:
            raise ValidationError(f'Имя пользователя должно содержать не более {cls.__MAX_LENGTH_USERNAME} символов!')
        return username

    @classmethod
    def validate_password(cls, password: str) -> str | None:
        """ Валидация password. """
        if not any(map(str.isdigit, password)):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру!')

        if len(list(filter(str.isalpha, password))) < cls.__MIN_LETTERS_PASSWORD:
            raise ValidationError(f'Пароль должен содержать не менее {cls.__MIN_LETTERS_PASSWORD} букв!')

        if len(password) < cls.__MIN_LENGTH_PASSWORD:
            raise ValidationError(f'Пароль должен содержать по крайней мере {cls.__MIN_LENGTH_PASSWORD} символов!')
        return password

    @classmethod
    def validate_role(cls, role: str) -> str | None:
        if role not in cls.__ALLOWED_ROLES:
            raise ValidationError(f'Неверное значение роли: "{role}".'
                                  f'\nРоль должна быть {" или ".join(cls.__ALLOWED_ROLES)}.')
        return role

    @staticmethod
    def validate_user_balance(value) -> float | None:
        """ Валидатор для balance """
        try:
            value = float(value)
        except ValueError:
            raise ValidationError('Значение должно быть числом.')

        if value < 0:
            raise ValidationError('Значение должно быть больше 0.')

        return value

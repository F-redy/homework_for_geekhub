from HT_13.task_2.users.custom_exceptions import ValidationError


class UserValidator:
    __MIN_LENGTH_USERNAME = 3
    __MAX_LENGTH_USERNAME = 20

    __MIN_LETTERS_PASSWORD = 1
    __MIN_LENGTH_PASSWORD = 5

    __ALLOWED_ROLES = ('учитель', 'студент', 'библиотекарь')

    @classmethod
    def validate_name(cls, name: str) -> str | None:
        """ Валидация name """

        letters = len(list(filter(str.isalpha, name)))
        digits = len(list(filter(str.isdigit, name)))

        if letters < digits:
            raise ValidationError('Неправильное имя пользователя. Имя должно состоять преимущественно из букв!')

        if len(name) < cls.__MIN_LENGTH_USERNAME:
            raise ValidationError(f'Имя пользователя должно содержать минимум {cls.__MIN_LENGTH_USERNAME} символов!')

        if len(name) > cls.__MAX_LENGTH_USERNAME:
            raise ValidationError(f'Имя пользователя должно содержать не более {cls.__MAX_LENGTH_USERNAME} символов!')
        return name

    @classmethod
    def validate_password(cls, password: str) -> str | None:
        """ Валидация password. """
        if not any(map(str.isdigit, password)):
            if password == 'admin':
                return password
            else:
                raise ValidationError('Пароль должен содержать хотя бы одну цифру!')

        if len(list(filter(str.isalpha, password))) < cls.__MIN_LETTERS_PASSWORD:
            raise ValidationError(f'Пароль должен содержать не менее {cls.__MIN_LETTERS_PASSWORD} букв!')

        if len(password) < cls.__MIN_LENGTH_PASSWORD:
            raise ValidationError(f'Пароль должен содержать по крайней мере {cls.__MIN_LENGTH_PASSWORD} символов!')
        return password

    @classmethod
    def validate_role(cls, role: str) -> str | None:
        if role.lower() not in cls.__ALLOWED_ROLES:
            raise ValidationError(f'Неверное значение роли: "{role}".'
                                  f'\nРоль должна быть {" или ".join(cls.__ALLOWED_ROLES)}.')
        return role

    @staticmethod
    def validate_phone(phone: str) -> str | None:
        if len(phone) != 10:
            raise ValidationError('Не правильный формат телефона. Введите номер телефона в формате: "0991112233"')

        return phone

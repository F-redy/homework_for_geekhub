class ValidationError(Exception):
    """ Исключение возникает из-за ошибок проверки. """
    pass


class UserExistsError(Exception):
    """ Исключение возникает при попытке зарегистрировать существующего пользователя. """
    pass


class UserNotFoundError(Exception):
    """ Исключение возникает, когда пользователь не найден во время аутентификации. """


class IncorrectPasswordError(Exception):
    """ Исключение возникает, когда во время аутентификации указан неправильный пароль. """


class UserBalanceUpdateError(Exception):
    """ Исключение возникает, при обновлении баланса пользователя. """
    pass

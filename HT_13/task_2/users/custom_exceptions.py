class ValidationError(Exception):
    """ Исключение возникает из-за ошибок проверки. """
    pass


class UserExistsError(Exception):
    """ Исключение возникает при попытке зарегистрировать существующего пользователя. """
    pass


class UserNotFoundError(Exception):
    """ Исключение возникает, когда пользователь не найден во время аутентификации. """
    pass


class IncorrectPasswordError(Exception):
    """ Исключение возникает, когда во время аутентификации указан неправильный пароль. """
    pass


class CheckoutBookError(Exception):
    """ Исключение возникает когда пользователь пытается взять повторно книгу которую ещё не сдал. """
    pass

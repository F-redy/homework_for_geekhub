class ATMError(Exception):
    """ Базовое исключение для ошибок, связанных с банкоматом. """
    pass


class ATMCurrencyError(Exception):
    """  Исключение для ошибок, связанных с валютой банкомата. """
    pass


class ATMBalanceError(Exception):
    """ Исключение для ошибок, связанных с балансом банкомата. """
    pass

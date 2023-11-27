from HT_12.atm_3_0.custom_exceptions import ATMBalanceError, ATMCurrencyError
from HT_12.atm_3_0.settings import ALLOWED_CURRENCY


class ATMValidator:
    """ Класс, предоставляющий методы для валидации данных, связанных с банкоматом. """

    @staticmethod
    def validate_atm_balance(atm_balance) -> int:
        """
        Проверяет корректность баланса банкомата.

        Args:
            atm_balance: Значение баланса банкомата.

        Returns:
            int: Баланс банкомата.

        Raises:
            ATMBalanceError: Если баланс не является положительным целым числом.
        """
        try:
            atm_balance = int(atm_balance)
        except ValueError:
            raise ATMBalanceError('Баланс банкомата должен быть целым числом.')

        if atm_balance < 0:
            raise ATMBalanceError('Баланс банкомата должен быть положительным числом.')

        return atm_balance

    @staticmethod
    def validate_denomination(denomination) -> int:
        """
        Проверяет корректность номинала купюр.

        Args:
            denomination: Номинал купюр.

        Returns:
            int: Номинал купюр.

        Raises:
            ATMCurrencyError:
            Если номинал не является положительным целым числом или не находится в списке разрешенных номиналов.
        """
        try:
            denomination = int(denomination)
        except ValueError:
            raise ATMCurrencyError('Купюры могут быть только целым числом.')

        if denomination not in ALLOWED_CURRENCY:
            raise ATMCurrencyError(f'Данного номинала "{denomination}" нет в списке разрешенных номиналов купюр.'
                                   f'\nРазрешенный список номиналов: {ALLOWED_CURRENCY}')

        return denomination

    @staticmethod
    def validate_quantity(quantity) -> int:
        """
        Проверяет корректность количества купюр.

        Args:
            quantity: Количество купюр.

        Returns:
            int: Количество купюр.

        Raises:
            ATMCurrencyError: Если количество купюр не является положительным целым числом.
        """
        try:
            quantity = int(quantity)
        except ValueError:
            raise ATMCurrencyError('Количество купюр должно быть целым числом.')

        if quantity < 0:
            raise ATMCurrencyError('Количество купюр должно быть больше или равно 0')
        return quantity

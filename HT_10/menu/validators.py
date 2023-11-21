from HT_10.menu.custom_exceptions import ValidationError
from HT_10.settings import ALLOWED_CURRENCY


def is_integer(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidationError('Значение должно быть числом.')

    if value < 1:
        raise ValidationError('Значение должно быть больше 0.')

    return value


def validate_denomination(denomination: str) -> int | None:
    try:
        denomination = int(denomination)
    except ValueError:
        raise ValidationError('Наминал купюры должен быть целым числом.')

    if denomination not in ALLOWED_CURRENCY:
        raise ValidationError(f'Данного наминала "{denomination}" нет в списке разрешенный номиналов купюр.'
                              f'\nРазрешенный список номиналов: {ALLOWED_CURRENCY}')

    return denomination


def validate_quantity(quantity: str) -> int | None:
    try:
        quantity = int(quantity)
    except ValueError:
        raise ValidationError('Количество купюр должно быть целым числом.')

    if quantity < 0:
        raise ValidationError('Количество купюр должно быть больше или равно 0')

    return quantity

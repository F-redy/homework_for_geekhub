from HT_10.menu.custom_exceptions import ValidationError


def is_integer(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidationError('Значение должно быть числом.')

    if value < 0:
        raise ValidationError('Значение должно быть больше 0.')

    return value


def validate_currencies(denominations_list: list[int]) -> list[int] | None:
    valid_denominations_list = []
    for denomination in denominations_list:
        try:
            denomination = int(denomination)
            valid_denominations_list.append(denomination)
        except ValueError:
            raise ValidationError('Наминал должен быть целым числом.')

    return valid_denominations_list

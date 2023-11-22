from HT_11.atm_2_0.custom_exceptions import ValidationError


def is_integer(value):
    try:
        value = int(value)
    except ValueError:
        raise ValidationError('Значение должно быть целым числом.')

    if value < 1:
        raise ValidationError('Значение должно быть больше 0.')

    return value

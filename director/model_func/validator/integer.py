from django.core.exceptions import ValidationError
from .. .base_data import validator_map

def int_0_p(value):
    if value < 0:
        raise ValidationError(
            '%(value)s 不是正整数',
            params={'value': value},
        )

validator_map.update({
    int_0_p:'integer(+0)'
})
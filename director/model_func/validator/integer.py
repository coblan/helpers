from django.core.exceptions import ValidationError

class Int0P(object):
    def __call__(self,value):
        if value < 0:
            raise ValidationError(
                '%(value)s 不是正整数',
                params={'value': value},
            )

    def get_validate_str(self):
        return 'integer(+0)'

int_0_p=Int0P()
    

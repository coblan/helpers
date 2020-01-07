from django.core.exceptions import ValidationError

class int_0_p(object):
    
    @staticmethod
    def __call__(value):
        if value < 0:
            raise ValidationError(
                '%(value)s 不是正整数',
                params={'value': value},
            )
    
    @classmethod
    def get_validate_str(cls):
        return 'integer(+0)'
    

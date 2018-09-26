from helpers.func.random_str import get_str
from .models import PhoneCode
from django.utils import timezone

def make_phone_validate_code(phone, length = 6): 
    code = get_str(length)
    PhoneCode.objects.create(code = code, valid = True, phone = phone)
    return code

def validate_phone_code(phone, code, span = timezone.timedelta(minutes = 3)): 
    try:
        obj = PhoneCode.objects.get(phone = phone, code = code)
        now = timezone.now()
        valide = False
        if obj.create_time - now < span:
            valide = True
        obj.delete()
        return valide
    except PhoneCode.DoesNotExist:
        return False

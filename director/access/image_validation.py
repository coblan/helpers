from helpers.authuser.validate_code import code_and_url
from helpers.director.shortcut import director_view
from helpers.director.kv import set_value,get_value,clear_value,KVModel
from helpers.func.random_str import short_uuid
from django.utils import timezone

@director_view('gen/validate_image')
def gen_code():
    code,url = code_and_url()
    uuid = short_uuid()
    set_value('_validat_code_%s'% uuid,code)
    return {
        'key':uuid,
        'image':url
    }


def validate_code(key,code):
    tm = timezone.now() - timezone.timedelta(minutes=5)
    KVModel.objects.filter(key__startswith='_validat_code_',update__lte = tm).delete()
    real_key = '_validat_code_%s'%key
    ss = get_value(real_key)
    if ss == code:
        clear_value(real_key)
        return True
    else:
        return False
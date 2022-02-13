def is_lazy_label(obj):
    return obj.__class__.__name__ =='__proxy__' and obj.__module__=='django.utils.functional'

def str_lazy_label(obj):
    if is_lazy_label(obj):
        return str(obj)
    elif isinstance(obj,list):
        return ';\n'.join(obj)
    else:
        return obj
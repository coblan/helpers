def is_lazy_label(obj):
    return obj.__class__.__name__ =='__proxy__' and obj.__module__=='django.utils.functional'

def str_lazy_label(obj):
    if is_lazy_label(obj):
        return str(obj)
    elif isinstance(obj,list):
        return ';\n'.join(obj)
    else:
        return obj


def path_to_field(model,field_path):
    if '__' in field_path:
        ls = field_path.split('__')
        current_model = model
        for ii in ls[:-1]:
            foreign_field = current_model._meta.get_field(ii)
            target_field = foreign_field.target_field
            current_model = target_field.model
        return current_model._meta.get_field(ls[-1])
    else:
        return model._meta.get_field(field_path)
    
    
            
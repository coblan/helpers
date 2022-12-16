from django.db import models
from helpers.director.model_func.cus_fields.cus_picture import PictureField
from helpers.director.model_func.cus_fields.multi_picture import MultiPictureField
from helpers.director.model_func.cus_fields.multichoice import MultiChoiceField,MultiChoiceTextField

def to_excel(model):
    print('字段名\t字段label\t字段类型说明')
    fmap = {
        PictureField:'单张图片类型',
        MultiPictureField:'多张图片类型,以数组形式上传.["图片1","图片2"]',
        models.DateField:'日期类型,请按照格式上传:年-月-日,如2022-10-01',
        models.DateTimeField:'时间类型,格式:年-月-日 时:分:秒,如2022-10-01 12:10:01',
    }
    for field in model._meta.fields:
        if fmap.get(field.__class__):
            ftype = fmap.get(field.__class__)
        elif isinstance(field,MultiChoiceField) or isinstance(field,MultiChoiceTextField):
            ftype = f'多选,上传一个数组[1,2,3]'
        elif isinstance(field,models.CharField) or isinstance(field,models.TextField):
            ftype='字符串'
        elif isinstance(field,models.BooleanField):
            ftype='Boolen布尔类型'
        elif isinstance(field,models.IntegerField):
            if field.choices:
                ftype=f'选择类型,选项为 {field.choices}'
            else:
                ftype='integer整数类型'
        elif isinstance(field,models.DecimalField):
            ftype = 'decimal小数类型'
        elif isinstance(field,models.FloatField):
            ftype = '浮点数小数类型'
        elif isinstance(field,models.ForeignKey):
            out_model = field.related_model
            ftype='外键,一般是一个整数, 指向表%s主键'% out_model._meta.model_name
        elif isinstance(field,models.ManyToManyField):
            out_model = field.related_model
            ftype ='多对多，一般是一个[1,2,3]数组, 指向表%s主键'% out_model._meta.model_name
        else:
            ftype =''
        print(f'{field.name}\t{field.verbose_name}\t{ftype}')

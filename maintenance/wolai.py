template = '''
|字段|标签|类型|说明|
|-|-|-|-|
'''
from django.db.models.fields import related
from helpers.director.model_func.cus_fields.snow_flake  import SnowFlakeField
from django.db import models

def table_doc(model_table):
    model_table.nolimit=True
    model_table_inst = model_table()
    heads = model_table_inst.get_heads()
    return heads
    

def fields_doc(model_form,pk_field='id',model_table=None,crt_user=None):
    model_form.nolimit = True
    model_form_inst = model_form(crt_user=crt_user)
    ctx = model_form_inst.get_head_context()
    heads = ctx.get('heads')
    fields_names = [head['name'] for head in heads]
    
    #print(heads)
    table_str = template
    
    if pk_field:
        fields_names.append(pk_field)
        
        id_inst = model_form_inst.instance._meta.get_field(pk_field)
        pk_field_type = ''
        if isinstance(id_inst,SnowFlakeField):
            pk_field_type = '字符串'
            pk_field_help = '雪花算法bigint型,为了兼容性转换为字符串返回'
        else:
            pk_field_type = 'int型'
            pk_field_help = id_inst.help_text or '数据的唯一标识值'
        table_str += f"|{pk_field}|{id_inst.verbose_name}|{pk_field_type}|{pk_field_help}|\n"
        table_str += f"|pk|数据库主键|唯一|与{pk_field}值一致。|\n"
    
    if hasattr(model_form,'Meta'):
        field_name_list = [field.name for field in model_form.Meta.model._meta.get_fields()]
    else:
        field_name_list = []
    for head in heads:
        if head['name'] ==pk_field:
            continue
        
        #required_str = ' 必填' if head.get('required',False)  else ''
        if head['name'] in field_name_list:
            field = model_form.Meta.model._meta.get_field(head['name'])
            required_str = ''
            if not field.blank:
                required_str = ' 必填'
            if field.default != models.fields.NOT_PROVIDED:
                required_str += f' 默认值:{field.default}'
        else:
            required_str = ' 必填' if head.get('required',False)  else ''
        table_str += f"|{head.get('name')}|{head.get('label')}|{com_to_type(head,model_form_inst)}|{head.get('help_text','')}{required_str}|\n"
    
    if  model_table:
        model_table.nolimit =True
        for head in table_doc(model_table):
            if head['name'] not in fields_names:
                table_str += f"|{head.get('name')}|{head.get('label')}| {table_to_type(head)}|{head.get('help_text','')} |\n"
    print(table_str)

def table_to_type(head):
    if head.get('options'):
        return f'选择类型{head["options"]}'
    return ''

def com_to_type(head,model_form_inst):
    if head['editor'] =='com-field-linetext':
        if head.get("maxlength"):
            return f'字符串(长度{head.get("maxlength")})'
        else:
            return '字符串'
    if head['editor'] =='com-field-blocktext':
        return '无限长字符串'
    if head['editor'] =='com-field-bool':
        return 'bool型'
    if head['editor'] =='com-field-location':
        return '格式为:lat,lng 的经纬度字符串'
    if head['editor']=='com-field-richtext':
        return 'com-field-richtext 富文本'
    if head['editor'] in ['com-field-table-select','com-field-select','com-field-cascader',
                          'com-field-checkbox',
                          'com-field-single-checkbox',
                          'com-field-radio']:
        try:
            field = model_form_inst.instance._meta.get_field(head['name'])
        except:
            if head.get('multiple') or head['editor']=='com-field-checkbox':
                return f'[多选]选择类型:{head.get("options")}'
            return f'选择类型:{head.get("options")}'
        if  isinstance( field,related.ManyToManyField) or isinstance(field,related.ForeignKey):
            rt= f'关联表:{field.related_model._meta.verbose_name}的pk值'
        else:
            rt=  f'选择类型:{head.get("options")}'
        if head.get('multiple'):
            return f'[多选]{rt}'
        else:
            return rt
    else:
        field = model_form_inst.instance._meta.get_field(head['name'])
        if  isinstance( field,related.ManyToManyField) or isinstance(field,related.ForeignKey):
            rt= f'关联表:{field.related_model._meta.verbose_name}的pk值'
            if head.get('multiple'):
                return f'[多选]{rt}'
            else:
                return rt
            
    if head['editor'] =='com-field-picture':
        return '字符串代表的图片地址'
    if head['editor'] =='com-field-multi-picture':
        return '图片数据.如:["1.png","2.png"]'
    if head['editor'] =='com-field-datetime':
        return '时间格式为:2020-01-31 23:59:59'
    if head['editor'] =='com-field-int':
        return '整数型'
    return head['editor']
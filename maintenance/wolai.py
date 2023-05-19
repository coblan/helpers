template = '''
|字段|标签|类型|说明|
|-|-|-|-|
'''
from django.db.models.fields import related
from helpers.director.model_func.cus_fields.snow_flake  import SnowFlakeField

def table_doc(model_table):
    model_table.nolimit=True
    model_table_inst = model_table()
    heads = model_table_inst.get_heads()
    return heads
    

def fields_doc(model_form,pk_field='id',model_table=None):
    model_form.nolimit = True
    model_form_inst = model_form()
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
        
    for head in heads:
        table_str += f"|{head.get('name')}|{head.get('label')}|{com_to_type(head,model_form_inst)}|{head.get('help_text','')}|\n"
    
    if  model_table:
        model_table.nolimit =True
        for head in table_doc(model_table):
            if head['name'] not in fields_names:
                table_str += f"|{head.get('name')}|{head.get('label')}| | |\n"
    print(table_str)

def com_to_type(head,model_form_inst):
    if head['editor'] =='com-field-linetext':
        if head.get("maxlength"):
            return f'字符串(长度{head.get("maxlength")})'
        else:
            return '字符串'
    if head['editor'] =='com-field-blocktext':
        return '无现长字符串'
    if head['editor'] =='com-field-bool':
        return 'bool型'
    if head['editor'] =='com-field-location':
        return '格式为:lat,lng 的经纬度字符串'
    if head['editor'] in ['com-field-table-select','com-field-select']:
        field = model_form_inst.instance._meta.get_field(head['name'])
        if  isinstance( field,related.ManyToManyField) or isinstance(field,related.ForeignKey):
            return f'关联表:{field.related_model._meta.verbose_name}的pk值'
        else:
            return f'选择类型{head.get("options")}'
    if head['editor'] =='com-field-picture':
        return '字符串代表的图片地址'
    if head['editor'] =='com-field-multi-picture':
        return '图片数据.如:["1.png","2.png"]'
    if head['editor'] =='com-field-datetime':
        return '时间格式为:2020-01-31 23:59:59'
    return head['editor']
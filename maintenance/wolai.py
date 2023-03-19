template = '''
|字段|标签|类型|说明|
|-|-|-|-|
'''
from django.db.models.fields import related

def fields_doc(model_form_inst):
    #table_inst.nolimit = True
    ctx = model_form_inst.get_head_context()
    heads = ctx.get('heads')
    #print(heads)
    table_str = template
    
    for head in heads:
        table_str += f"|{head.get('name')}|{head.get('label')}|{com_to_type(head,model_form_inst)}|{head.get('help_text','')}|\n"
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
    if head['editor'] in ['com-field-table-select','com-field-select']:
        field = model_form_inst.instance._meta.get_field(head['name'])
        if  isinstance( field,related.ManyToManyField) or isinstance(field,related.ForeignKey):
            return f'关联表:{field.related_model._meta.verbose_name}'
        else:
            return f'选择类型{head.get("options")}'
    if head['editor'] =='com-field-picture':
        return '字符串代表的图片地址'
    return head['editor']
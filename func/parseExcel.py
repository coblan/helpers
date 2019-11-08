from openpyxl import load_workbook
from helpers.director.shortcut import director_view
from django.conf import settings
import os

@director_view('func.get_excel_head')
def get_excel_head(url):
    path = url2path(url)
    wb = load_workbook(filename=path)
    
    sheets = wb.get_sheet_names()   # 获取所有表格(worksheet)的名字
    sheet0 = sheets[0]  # 第一个表格的名称
    ws = wb.get_sheet_by_name(sheet0) # 获取特定的 worksheet
    heads_names = [x.value.strip() for x in next(ws.rows)]
    
    #heads = [x.value for x in next(ws.rows)]
    
    return heads_names

def url2path(url):
    path = os.path.join( os.path.dirname(settings.BASE_DIR),url[1:] )
    return path

def get_match_index(head_name,heads):
    if head_name in heads:
        return heads.index(head_name)
    #for head in form_heads:
    return None

def parser_excel(url,dispatch_head,valid_row=[]):
    path = url2path(url)
    wb = load_workbook(filename=path,data_only=True)
    
    sheets = wb.get_sheet_names()   # 获取所有表格(worksheet)的名字
    sheet0 = sheets[0]  # 第一个表格的名称
    ws = wb.get_sheet_by_name(sheet0) # 获取特定的 worksheet
    count =0
    for row in ws.rows:
        if count >0:
            dc={}
            for k,v in dispatch_head.items():
                if not k.startswith(('_','meta_')) and v:
                    index = int(v)
                    if row[index].value is not None:
                        dc[k]=row[index].value
            
            is_valid = True
            for ff in valid_row:
                if not dc.get(ff):
                    is_valid=False
                    break
            if is_valid:
                yield dc
            else:
                continue
        else:
            count =1
from helpers.director.model_func.func import str_lazy_label
from ..base_data import director

class JsonToExcel(object):
    @classmethod
    def gen_from_search_args(cls,search_args):
        
        return JsonToExcel(**search_args)
    
    def __init__(self,heads=[],rows=[]):
        self.heads = heads
        self.rows = rows
    def get_excel(self):
        from openpyxl import Workbook
        

        self.is_export_excel = True
        
        heads = self.heads
        rows =  self.rows
        out_rows = []
        excel_row = []
        # 第一行是 头
        for head in heads:
            excel_row.append(head['label'])
            if 'options' in head and head['options']:
                head['options_dict'] = {}
                for opt in head['options']:
                    head['options_dict'][opt['value']] = opt['label'] 
        out_rows.append(excel_row)
        
        # 这里开始写数据
        for row in rows:
            excel_row = []
            for head in heads:
                label = '_%s_label' % head['name']
                if label in row:
                    excel_row.append( row.get(label) )
                elif 'options_dict' in head:
                    value = row.get(head['name'])
                    find_label = head['options_dict'].get(value, '')
                    excel_row.append( find_label )
                else:
                    excel_row.append( row.get(head['name']) )
            out_rows.append(excel_row)
        
        wb = Workbook()
        ws = wb.active
        for row in out_rows:
            #ws.append(row)
            # 有可能是models.py lazy翻译的
            ws.append([str_lazy_label(x)  for x in row ])        
        
        return wb
    
director.update({
    'json-to-excel':JsonToExcel
})
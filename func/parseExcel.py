#from openpyxl import load_workbook
from helpers.director.shortcut import director_view,get_request_cache
from django.conf import settings
import os
from helpers.director.shortcut import Fields,ModelFields
import xlrd

class ExcelFields(ModelFields):
    '''
    需要自定义  
    
    def save_form()
    '''
    def __init__(self,  *args, **kw):
        super().__init__(*args, **kw)
        self.set_named_ctx()
    
    def set_named_ctx(self):
        director_name = self.get_director_name()
        named_ctx = get_request_cache()['named_ctx']
        if director_name not in named_ctx:
            named_ctx.update({
                director_name:self.get_head_context()
            })
    
    def _clean_dict(self, dc):
        return dc
    
    def is_valid(self):
        return True
    def clean(self):
        pass
    
    def get_front_action(self,):
        """
        发送到前端执行的代码。
        `ctx.row.par_row_pk = scope.ps.vc.par_row.pk` 用于从前端环境提取变量信息，可以overwrite该行代码,
        如果由主界面table点击row跳转到tab.table再进行导出，可能会用到这个字段
        """
        self_director_name = self.get_director_name()

        #{
        #if(scope.ps.vc.par_row){
           #return ex.director("%(director_name)s").call("parse_excel_head",{url:resp[0],par_row:scope.ps.vc.par_row.pk})
        #}else{
           #return ex.director("%(director_name)s").call("parse_excel_head",{url:resp[0]}) 
        #} }


        return '''
        var ctx = named_ctx["%(director_name)s"]
        ex.uploadfile({accept:".xlsx, .xls, .csv"})
            .then((resp)=>{
               if(scope.ps.vc.par_row){
                  return ex.director("%(director_name)s").parse_excel_head({url:resp[0],par_row:scope.ps.vc.par_row.pk})
               }else{
                  return ex.director("%(director_name)s").parse_excel_head({url:resp[0]}) 
               } })
            .then((resp)=>{ 
                ex.each(ctx.heads,head=>{head.options=resp.options});
                ctx.row=resp.row;
                if(scope.ps.vc.par_row){
                   ctx.row.par_row_pk = scope.ps.vc.par_row.pk
                }
                return cfg.pop_vue_com('com-form-one',ctx,{title:'请选择正确的对应字段(系统预设名<--->excel首行字段名)'})
            }).then((resp)=>{
               scope.ps.search()
               
               if(resp.messages){
                  cfg.pop_vue_com('com-message-rows',resp,{title:'导入结果'})
               }
            })
        '''%{'director_name':self_director_name}
    
    def parse_excel_head(self,url,**kws):
        excelHeads = get_excel_head(url)
        heads =[]
        for index,name in enumerate(excelHeads):
            heads.append({'value':index,'label':'excel:%s'%name.strip(),})
        
        row ={
            '_director_name':self.get_director_name(),
            'meta__url':url
        }
        for head in self.get_heads():
            index = self.get_match_index(head, excelHeads)
            if index is not None:
                row[head['name']] = index
        return {
            'options':heads,
            'row':row
            }
    
    def get_match_index(self,head,excelHeads):
        """
        @head:  列选项头  {'name': 'InvoiceCode', 'label': '发票代码','editor':'com-field-select' ....}
        @excelHeads: ['col_name1','col_name2','col_name3']
        """
        if head['label'] in excelHeads:
            return excelHeads.index(head['label'])
        #for head in form_heads:
        return None    
    
    def dict_head(self, head):
        "这里会修改modelfields原来的field editor"
        head['editor']='com-field-select'
        head['group']='1'
        head['fv_rule']=''
        head['option_show'] = '''
        (function(){
            var heads = scope.ps.vc.heads
            for(var i=0;i<heads.length;i++){
                var head = heads[i]
               if( head.group != '1')continue
               var key = head.name
               if(key !=scope.vc.head.name && scope.row[key] ==scope.option.value){
                  return false
               }
             }
           return true
        })()
        '''
        return head
    
    def parser_excel(self,url,dispatch_head,valid_row=[]):
        '''
        @valid_row: list  每行，必须要有该字段才算是有效行 
        '''
        return parser_excel(url, dispatch_head,valid_row)
    
    def save_form(self):
        """ 普通的报错逻辑 , 如果有 par_row_pk 字段的话，需要重写 save_form 的row数据"""
        url = self.kw.pop('meta__url')
     
        out_list = []
        model = self._meta.model
        for row in self.parser_excel(url,self.kw):
            out_list.append(model(**row))

        try:
            model.objects.bulk_create(out_list)
        except Exception as e:
            raise UserWarning(str(e))
    


@director_view('func.get_excel_head')
def get_excel_head(url):
    '''
    xlrd 可以解析 xls和xlsx,所以这里用xlrd来读取文件，不用openpyxl
    '''
    path = url2path(url)
    if path.endswith('.csv'):
        return parse_csv_head(path)
    else:
        return parse_xls_head(path)

def parse_xls_head(path):
    # 2021/12/19，由于解析 .xls 报错，所以增加 encoding_override='gbk'。
    # [TODO] 后面看看效果，如果解析其他excel报错，这里可能需要用try进行一定判断
    if path.endswith('.xls'):
        data = xlrd.open_workbook(path,encoding_override='gbk')
    else:
        data = xlrd.open_workbook(path)
    return data.sheets()[0].row_values(0)

def parse_csv_head(path):
    import csv
    with open(path,newline='') as csvfile:
        spamreader = csv.reader(csvfile) #, delimiter=' ', quotechar='|')
        for row in spamreader:
            return row
        

def parse_xlsx_heads(path):
    'openpyxl读取第一个作为头 ； 暂时用xlrd替代'
    wb = load_workbook(filename=path)
    sheets = wb.get_sheet_names()   # 获取所有表格(worksheet)的名字
    sheet0 = sheets[0]  # 第一个表格的名称
    ws = wb.get_sheet_by_name(sheet0) # 获取特定的 worksheet
    heads_names = [x.value.strip() if x.value else '' for x in next(ws.rows) ]
    
    return heads_names

def url2path(url):
    path = os.path.join( os.path.dirname(settings.BASE_DIR),url[1:] )
    return path



def parser_excel(url,dispatch_head,valid_row=[]):
    '''
    @valid_row : 标识哪些列是必须的，否则改行为无效行
    '''
    path = url2path(url)
    if path.endswith('.csv'):
        rows = parse_csv(path)
    else:
        rows = parse_xls(path)
    #if path.endswith('.xls'):
        #rows = parse_xls(path)
    #else:
        #rows = parse_xlsx(path)
    #wb = load_workbook(filename=path,data_only=True)
    
    #sheets = wb.get_sheet_names()   # 获取所有表格(worksheet)的名字
    #sheet0 = sheets[0]  # 第一个表格的名称
    #ws = wb.get_sheet_by_name(sheet0) # 获取特定的 worksheet
    #count =0
    for row in rows[1:]:
        #if count >0:
        dc={}
        for k,v in dispatch_head.items():
            if not k.startswith(('_','meta_')) and v!='':
                index = int(v)
                
                dc[k]=row[index]
                #if row[index].value is not None:
                    #dc[k]=row[index].value
        
        is_valid = True
        for ff in valid_row:
            if dc.get(ff,None) in [None,'']:
                is_valid=False
                break
        if is_valid:
            yield dc
        else:
            continue
        #else:
            #count =1

def parse_xlsx(path):
    wb = load_workbook(filename=path,data_only=True)
    
    sheets = wb.get_sheet_names()   # 获取所有表格(worksheet)的名字
    sheet0 = sheets[0]  # 第一个表格的名称
    ws = wb.get_sheet_by_name(sheet0) # 获取特定的 worksheet
    rows = [[x.value for x in row] for row in  ws.rows]
    return rows[1:]

def parse_xls(path):
    data = xlrd.open_workbook(path,encoding_override='gbk')
    table = data.sheets()[0]
    ls =[]
    for i in range(0,table.nrows):
        rowList =[]
        rowListObj = table.row(i)
        for obj in rowListObj:
            if obj.value and str(obj).startswith('xldate'):
                rt = xlrd.xldate.xldate_as_datetime(obj.value, xlrd.Book.datemode)
                rowList.append(rt . strftime('%Y-%m-%d'))
            elif str(obj).startswith('number'):
                # 排除 123 解析成 123.0 这种问题
                if int(obj.value) == obj.value:
                    rowList.append(int( obj.value))
                else:
                    rowList.append(obj.value)
            else:
                rowList.append(obj.value)
        ls.append(rowList)
        #ls.append(table.row_values(i))
    return ls

def parse_csv(path):
    import csv
    rows = []
    with open(path,newline='') as csvfile:
        spamreader = csv.reader(csvfile) #, delimiter=' ', quotechar='|')
        for row in spamreader:
            rows.append( row )
    return rows[1:]
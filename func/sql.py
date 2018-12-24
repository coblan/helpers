from django.db import connection

def qn(s):  
    """这个函数不好用，还是用自带的转换函数吧"""
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]  
    for stuff in dirty_stuff:  
        s = s.replace(stuff,"")  
    #return "'"+s+"'"  
    return s 


def exec_sql(sql,lower_key=True):
    cursor = connection.cursor()
    cursor.execute(sql )
    
    rows=[]
    for row in cursor:
        row_dc ={}
        for col_data, col in zip(row, cursor.description):
            row_dc[col[0]]=col_data
        rows.append(row_dc)
    
    return rows 
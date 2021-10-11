def split_list(dstlist,every_num):
    """ 将dstlist分批次返回。
    
    [1,2,3,4,5,6]  返回成 [1,2],[3,4],[5,6]
    """
    count=0
    while len(dstlist) > count*every_num:
        yield dstlist[every_num*count:every_num*(count+1)]
        count += 1

def left_join(left,right,func):
    """以left为参照，将right 链接起来。
    
    left = [{name:'dog',age:18}]
    right = [{name:'dog',weight:80}]
    func = lamda l,r : l.name==r.name
    
    返回: [{name:'dog',age:18,weight:80}]
    """
    for row in left:
        for ds in right:
            if func(row,ds):
                row.update(ds)
                right.remove(ds)
                break

def complement(srcList,rows,extrac_fun,default=0):
    """以srcList为参照，返回补全的数组
    
    用在chart图表补全数据
    Args:
    srcList = ['2021-07-20','2021-07-21']
    rows =[{'date':'2021-07-20','count':12}]
    extrac_fun = lamda row,target: row if row['date']==target else None
    返回:
    [{date:'2021-07-20','count':12},{date:'2021-07-21','count':0}]
    """
    outlist = [default] * len( srcList )
    for index,item in enumerate( srcList):
        rt = _find_dc_item(rows,item,extrac_fun)
        if rt:
            outlist[index]=rt
    return outlist

def _find_dc_item(rows,target, extrac_fun):
    for row in rows:
        rt = extrac_fun(row,target)
        if rt:
            return rt
    return None
    
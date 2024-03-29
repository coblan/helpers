import random
import logging
general_log = logging.getLogger('general_log')
from django.db import close_old_connections
import copy

def split_list(dstlist,every_num):
    """ 将dstlist分批次返回。
    
    [1,2,3,4,5,6]  返回成 [1,2],[3,4],[5,6]
    """
    count=0
    while len(dstlist) > count*every_num:
        yield dstlist[every_num*count:every_num*(count+1)]
        count += 1

def left_join(left,right,func,merge_fun=None):
    """以left为参照，将right 链接起来。
    
    left = [{name:'dog',age:18}]
    right = [{name:'dog',weight:80}]
    func = lambda l,r : l['name']==r['name']
    
    返回: [{name:'dog',age:18,weight:80}]
    
    如果merge_fun为空，则会使用dict.update合并。如果不为空，就会保留merge_fun返回的元素
    merge_fun = lambda l,r : {'name':l['name'],'count':l.get('count',0)+r.get('count',0)}
    """
    left1= copy.deepcopy(left)
    rigth1 = copy.deepcopy(right)
    for row in left1:
        for ds in rigth1:
            if func(row,ds):
                if merge_fun: # 如果有融合函数
                    row.update(merge_fun(row,ds))
                else:
                    row.update(ds)
                rigth1.remove(ds)
                break
    return left1

def out_join(left,right,func,merge_fun=None):
    """
    参考left_join的说明
    """
    left1= copy.deepcopy(left)
    rigth1 = copy.deepcopy(right)
    for row in left1:
        for ds in rigth1:
            if func(row,ds):
                if merge_fun: # 如果有融合函数
                    row.update(merge_fun(row,ds))
                else:
                    row.update(ds)
                rigth1.remove(ds)
                break
    return left1 + rigth1

def multiply_array(arry1,arry2):
    for a1 in arry1:
        for a2 in arry2:
            yield a1,a2

def complement(srcList,rows,extrac_fun,default=0):
    """以srcList为参照，返回补全的数组
    
    用在chart图表补全数据
    Args:
    srcList = ['2021-07-20','2021-07-21']
    rows =[{'date':'2021-07-20','count':12}]
    extrac_fun = lamda row,target: row if row['date']==target else None
    defaut:没有找到的key返回的值
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

def split_iter(iteration,count,name='unnamed'):
    """
    分批来处理一个可迭代器。适合一次处理不了，需要分批来处理大的collection的情况。
    [1,2,3,4,5]
    返回
    [[1,2,3],[4,5,6]]
    """
    current_count = 0
    ls = []
    for inst in iteration:
        ls.append(inst)
        current_count += 1
        if current_count >=count:
            current_count = 0
            yield ls
            general_log.debug(f'分批查询{name} index={current_count}...')
            ls =[]
       
    if ls:
        general_log.debug(f'分批查询{name} count={len(ls)}...')
        yield ls

def split_db_query(query,count,name='unnamed',read_in_memery=False,every_time_close_db=False):
    """透明化的处理query查询迭代，只要支持[start:end]这种查询集。
    已知支持 django.query, mongoengin库
    """
    index =0
    while True:
        #print(f'分批查询 index={index}...')
        general_log.debug(f'分批查询{name} index={index}...')
        if every_time_close_db:
            close_old_connections()        
        this_count = 0
        if read_in_memery:
            ls = list(query[index:index+count])
        else:
            ls = query[index:index+count]
        for inst in ls:
            this_count +=1
            yield inst
            
        index += count
       
        if this_count < count:
            break
        


def slite_query(query,batch_count):
    current_index = 0

    while True:
        ls = []
        for inst in query[current_index:current_index+batch_count]:
            ls.append(inst)
        current_index += batch_count      
        if ls:
            yield ls
        else:
            break
       
    

def slice_names(names,start,end):
    """
    @names:['name1','name2','name3','name4']
    @start: name2
    @end:   name4
    
    返回 :[name2,name3,name4]
    """
    out =[]
    inn = False
    for name in names:
        if name ==start:
            inn = True
        if inn:
            out.append(name)
        if name ==end:
            inn =False
            break
    return out

def random_sample(collection,count):
    if len(collection) <= count:
        return collection
    else:
        return random.sample(collection,count)

def jump_fetch(ls,span=3):
    """
    """
    table_fields =[]
    length= len(ls)
    current_index=0
    while True:
        if current_index >=length:
            break
        last_ls = [ ls[current_index] ]
        if current_index+span < length:
            last_ls.append(
                ls[current_index +span]
            )
        table_fields.append(last_ls)
        if (current_index+span+1)%(2*span) ==0:
            current_index +=(span+1)
        else:
            current_index +=1   
    return table_fields
# encoding:utf-8
from __future__ import unicode_literals
import inspect
import copy


"""
>->helpers/container.rst>
========
容器
========

evalue_container
-----------------
接收dict或者list对象，对里面的'visible'属性进行计算。
<-<

"""

def evalue_container(container,**kw):
    """
    use to evalue dict or list ,that has some callable element
    
    Example:
    dc={'name':lambda user:user.username}
    
    dc = evalue_container(dc,user=request.user)
    
    """
    if isinstance(container,dict):
        return evalue_dict(container,**kw)
    elif isinstance(container,(tuple,list)):
        return evalue_list(container,**kw)
    elif inspect.isfunction(container):
        args=inspect.getargspec(container).args
        real_kw={}
        for k,v in kw.items():
            if k in args:
                real_kw[k]=v
            
        return container(**real_kw)
    else:
        return container

def evalue_dict(dc,**kw):
    out_dc={}
    for k,v in dc.items():
        if k !='visible':
            out_dc[k]=evalue_container(v,**kw)
        else:
            out_dc[k]=v
    return out_dc

def evalue_list(ls,**kw):
    new_ls=[]
    for item in ls:
        # 先evalue子孙元素，再计算是否显示。而且只有在list中，visible属性才起作用
        #tmp = copy.deepcopy(item)  # deepcopy 有性能问题
        #tmp=evalue_container(tmp,**kw)
        
        # 先运行一下 visible 排除那些 不需要的运算
        if isinstance(item,dict) and 'visible' in item:
            visible= item.get('visible')
            if inspect.isfunction(visible):
                visible=run_func(visible,liveitem=item,**kw)
            if not visible:
                continue  
        # 再求职 dict
        tmp=evalue_container(item,**kw)
        
        # 再运行一下 visible ，考虑到那些 需要 检查 len(children) ==0 需要 求值后才能判断
        if isinstance(tmp,dict) and 'visible' in tmp:
            visible= tmp.get('visible')
            if inspect.isfunction(visible):
                visible=run_func(visible,liveitem=tmp,**kw)
            if not visible:
                continue  
            tmp.pop('visible',None)
        new_ls.append(tmp)
    return new_ls

def run_func(func,liveitem,**kw):
    args=inspect.getargspec(func).args
    real_kw={}
    for k,v in kw.items():
        if k in args:
            real_kw[k]=v  
    if 'liveitem' in args:
        real_kw['liveitem'] = liveitem
    return func(**real_kw)

def find_one(collection,dc):
    for doc in collection:
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            return doc

def find_one_r(collection,dc):
    item=find_one(collection, dc)
    if item:
        return item
    else:
        for doc in collection:
            for k,v in doc.items():
                if isinstance(v,(list,tuple)):
                    item= find_one_r(v,dc)
                    if item:
                        return item
                
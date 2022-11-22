def findone(collection,dc):
    for doc in collection:
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            return doc

def filter_all(collection,dc):
    out = []
    for doc in collection:
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            out.append(doc)
    return out   

def find_index(collection,dc):
    count =0
    for doc in collection:
        count += 1
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            return count
    return -1

def locate(path):
    ls = path.split('.')
    try:
        mod=None
        for k in range(len(ls)):
            mod=__import__('.'.join(ls[:k+1]))
        return mod
    except Exception as e:
        return reduce(lambda obj,prop:getattr(obj,prop,None), ls[k:], mod)


def assign_object(dst,src,item_match=None,child=['items','childrens']):
    """把src的值赋予dst
    
    Args:
    item_match : callable对象,返回 src中 与 dst.item 相匹配的项
    """
    if isinstance(dst,list):
        for item in dst:
            src_item = item_match(item,src)
            if src_item:
                assign_object(item,src_item,item_match,child)
    elif isinstance(dst,dict):
        for key in dst:
            if not src.get(key):
                continue
            if key in child:
                assign_object(dst[key],src[key],item_match,child)
            else:
                dst[key] = src[key]


def default_assign( dst,src,key):
    v = dst[key]
    if v.endswith('.jpg') or v.endswith('.png'):
        dst[key] = src[key]

def assign_collection(dst,src,item_match=None,assign_fun=default_assign,):
    """把src的值赋予dst
    
    Args:
    item_match : callable对象,在list中相匹配的项，如果不传，则按照index来匹配
    
    """
    if isinstance(dst,list):
        index = -1 
        for item in dst:
            index +=1
            if item_match:
                src_item = item_match(item,src)
            else:
                if len(src)>index:
                    src_item = src[index]
                else:
                    continue
            if src_item:
                assign_collection(item,src_item,item_match,assign_fun)
    elif isinstance(dst,dict):
        for key in dst:
            next_dst = dst[key]
            next_src = src.get(key)
            if isinstance(next_dst,dict) and isinstance(next_src,dict):
                assign_collection(next_dst,next_src,item_match,assign_fun)
            elif isinstance(next_dst,list) and isinstance(next_src,list):
                assign_collection(next_dst,next_src,item_match,assign_fun)
            else:
                assign_fun(dst,src,key)
                #dst[key] = src[key]
def findone(collection,dc):
    for doc in collection:
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            return doc

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
    
    @item_match : callable对象,返回 src中 与 dst.item 相匹配的项
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
                
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
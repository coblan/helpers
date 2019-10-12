def find_one(obj_list, pattern_dc): 
    for obj in obj_list:
        find = True
        for k, v in pattern_dc.item():
            if obj.get(k) != v:
                find = False
        if find:
            return obj

def sort_by_name(obj_list,namelist,keep=True):
    ls = []
    extra_ls = []
    for obj in obj_list:
        if obj['name'] in namelist:
            ls.append(obj)
        else:
            extra_ls .append(obj)
    ls.sort(key= lambda x: namelist.index(x['name']))
    if keep:
        ls += extra_ls
    return ls
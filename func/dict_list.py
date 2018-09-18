def find_one(obj_list, pattern_dc): 
    for obj in obj_list:
        find = True
        for k, v in pattern_dc.item():
            if obj.get(k) != v:
                find = False
        if find:
            return obj
                
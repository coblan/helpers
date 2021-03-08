from helpers.director.model_func.dictfy import sim_dict

def table_rows(src_query,model):
    ls = []
    for inst in src_query:
        dc = inst.__dict__ #sim_dict(inst,include_pk=False)
        rm_keys=[]
        for k in dc:
            if k.startswith('_'):
                rm_keys.append(k) 
        for key in rm_keys:
            dc.pop(key)
        ls.append(model(**dc))
        if len(ls) > 2000:
            yield ls
            ls =[]
    yield ls
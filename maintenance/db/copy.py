from helpers.director.model_func.dictfy import sim_dict

def table_rows(src_query,model):
    ls = []
    for inst in src_query:
        dc = sim_dict(inst,include_pk=False)
        ls.append(model(**dc))
        if len(ls) > 2000:
            yield ls
            ls =[]
    yield ls
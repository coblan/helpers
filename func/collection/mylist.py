def split_list(dstlist,every_num):
    count=0
    while len(dstlist) > count*every_num:
        yield dstlist[every_num*count:every_num*(count+1)]
        count += 1

def left_join(left,right,func):
    for row in left:
        for ds in right:
            if func(row,ds):
                row.update(ds)
                right.remove(ds)
                break
def split_list(dstlist,every_num):
    count=0
    while len(dstlist) > count*every_num:
        yield dstlist[every_num*count:every_num*(count+1)]
        count += 1

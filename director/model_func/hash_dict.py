def hash_dict(dc,keys=None):
    ls =[]
    for k,v in dc.items():
        if keys:
            if k not in keys:
                continue
        if k.startswith('_'):
            continue
        ls.append("%s:%s"%(k,v))
    ls = sorted(ls)
    return hash(';'.join(ls))
    #return ls

from base64 import b64encode
def hashCode (strin):
    strin= b64encode(strin)
    h=0
    off=0
    length = len(strin)
    for i in range(length):
        h = 31* h + ord(strin[off])
        off +=1
    t=-2147483648*2
    while h>2147483647:
        h+=t
    return h
    
    #{
            #var h = 0, off = 0;
            #var len = str.length;
            #for(var i = 0; i < len; i++){
                #h = 31 * h + str.charCodeAt(off++);
            #}
            #var t=-2147483648*2;
            #while(h>2147483647){
                #h+=t
            #}
            #return h;
        #}
# encoding:utf-8
from __future__ import unicode_literals
from hashlib import md5
#from sha import md5
from base64 import b64encode
import json

def hash_dict(dc,keys=None):
    ls =[]
    for k,v in dc.items():
        if keys:
            if k not in keys:
                continue
        if k.startswith('_'):
            continue
        if v is True:
            v= 'true'
        if v is False:
            v='false'
        if v is None:
            v='null'
        ls.append("%s:%s"%(k,v))
    ls = sorted(ls)
    code= ';'.join(ls)
    return md5(code.encode('utf-8')).hexdigest() 
    #return ls

#from base64 import b64encode
#def hashCode (strin):
    #strin= b64encode(strin)
    #h=0
    #off=0
    #length = len(strin)
    #for i in range(length):
        #h = 31* h + ord(strin[off])
        #off +=1
    #t=-2147483648*2
    #while h>2147483647:
        #h+=t
    #return h
    
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
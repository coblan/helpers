import hashlib

def md5(data):
    md5 = hashlib.md5()
    if isinstance(data,str):
        md5.update(data.encode('utf-8'))
    else:
        md5.update(data)
    return  md5.hexdigest()
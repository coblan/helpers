import hashlib

def md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return  md5.hexdigest()
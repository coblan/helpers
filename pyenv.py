
def u(text):
    if isinstance(text,str):
        return text.decode('utf-8')
    else:
        return unicode(text)


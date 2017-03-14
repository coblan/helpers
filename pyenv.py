
def u(text):
    try:
        return unicode(text)
    except UnicodeDecodeError:
        return text.decode('utf-8')

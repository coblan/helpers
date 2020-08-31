
def adapt_date_splash(value,name):
    "未完成！！！ 将 2020/6/1  转换为 2020-06-01"
    if value:
        ls = value.split('/')
        return '-'.join(ls)
    else:
        return value
from decimal import Decimal

def adapt_date_splash(value,name):
    "未完成！！！ 将 2020/6/1  转换为 2020-06-01"
    if value:
        ls = value.split('/')
        return '-'.join(ls)
    else:
        return value

def decimal_round(digits=2):
    def _fun(value,name):
        if value:
            aa = Decimal(value)
            return round(aa,digits)
        else:
            return value
    return _fun
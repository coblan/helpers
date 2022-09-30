import requests
from requests.auth import HTTPBasicAuth

def get_queue(domain,user,pswd,vhost='',name_reg='',page_size=100):
    """
    获取rabbitmq的queue列表，
    @domain:管理的域名入http://www.123.com,主要不要斜线结尾
    @user:用户
    @pswd:密码
    @name_reg:名称正则表达式，如: mqtt-subscription-*   表示mqtt-subscription-开始的
    
    """
    crt_page = 1
    while True:
        if vhost:
            url = f'{domain}/api/queues/{vhost}?page={crt_page}&page_size={page_size}&name={name_reg}&use_regex=true&pagination=true'
        else:
            url = f'{domain}/api/queues?page={crt_page}&page_size={page_size}&name={name_reg}&use_regex=true&pagination=true'
        rt2 = requests.get(url, auth=HTTPBasicAuth(user,pswd))
        rt_dc = rt2.json()
        items = rt_dc.get('items',[])
        if items:
            for item in items:
                yield item
        else:
            break
        if rt_dc.get('page_count') <=rt_dc.get('page'):
            break
        else:
            crt_page +=1
        
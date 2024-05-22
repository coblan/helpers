from .dot_dict import read_dict_path
from django.conf import settings
from fabric import Connection
import invoke

local = invoke.Context()
def server_context_run_cmd(cmd):
    """
    在docker容器内，以宿主环境执行命令
    
    配置示例:
    
    DOCKER_SETTING= {
    'host':'172.17.0.1',
    'user':'ubuntu',
    #'password':'root123456',
    'key_filename':'/pypro/media_convert/media/007_key.pem'
    
}
    
    """
    if read_dict_path(settings,'DOCKER_SETTING.user',None):
        host = read_dict_path(settings,'DOCKER_SETTING.host')
        user = read_dict_path(settings,'DOCKER_SETTING.user')
        if read_dict_path(settings,'DOCKER_SETTING.password'):
            password = read_dict_path(settings,'DOCKER_SETTING.password')
            server = Connection(f'{user}@{host}',connect_kwargs={'password':password})
        else:
            key_filename = read_dict_path(settings,'DOCKER_SETTING.key_filename')
            server = Connection(f'{user}@{host}',connect_kwargs={'key_filename':key_filename})            
        return server.run(cmd)
    else:
        return local.run(cmd)
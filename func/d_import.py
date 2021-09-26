import importlib
import re

def import_element(element_path):
    """以字符串的形式导入模块类的函数或者类
    
    Args:
    element_path:a.b.c;  .c 是类或者函数
    """
    ls = element_path.split('.')
    pkg_path = '.'.join(ls[:-1])
    pkg = importlib.import_module(pkg_path)
    return getattr(pkg,ls[-1])
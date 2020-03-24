import importlib
import re

def import_element(element_path):
    ls = element_path.split('.')
    pkg_path = '.'.join(ls[:-1])
    pkg = importlib.import_module(pkg_path)
    return getattr(pkg,ls[-1])
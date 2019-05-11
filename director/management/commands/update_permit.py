# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import site_cfg
from helpers.director.models import PermitModel

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        permit_options = site_cfg.get('permit.options')()
        depend_chain={}
        # 生成依赖dict
        for opt in permit_options:
            for dc in self.parse_item(opt):
                if dc['key'] in depend_chain:
                    raise UserWarning('%s 重复了，请检查 permit 设置'%dc['key'])
                depend_chain[dc['key']] = dc['depend']
                
        # 根据依赖dict 去修正 PermitModel的每行数据
        for pg in PermitModel.objects.all():
            ls = pg.names.split(';')
            ls = [x for x in ls if x in depend_chain]
            out_ls=[]
            last_out_len = 0
            while True:
                for pname in ls:
                    if pname in depend_chain:
                        out_ls.append(pname)
                        out_ls += depend_chain[pname]
                out_ls = list( set(out_ls) )
                ls = list( out_ls)
                if len(out_ls) == last_out_len:
                    break
                else:
                    last_out_len = len(out_ls)
            pg.names = ';'.join(out_ls)
            pg.save()
        print('更新权限依赖关系完成。')
                    
            
    def parse_item(self,item):
        if item.get('value'):
            yield {'key':item.get('value'),'depend': item.get('depend',[]) }
        if item.get('children'):
            for child in item.get('children'):
                for dc in self.parse_item(child):
                    yield dc
    
    

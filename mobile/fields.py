from helpers.director.shortcut import ModelFields

class ModelFieldsMobile(ModelFields):
    def get_operations(self):
        if self.permit.changeable_fields():
            return [
                { 'name':'save','editor':'com-op-submit','label':'确定', 
                  'action':'scope.ps.vc.submit().then(row=>{cfg.toast("保存成功"); ex.vueAssign(scope.ps.vc.par_row,row)})'}
            ]
        else:
            return []

from helpers.director.shortcut import ModelFields,Fields

class ModelFieldsMobile(ModelFields):
    
    #'init_express':'ex.director_call("%(director_name)s",{}).then((resp)=>{ex.vueAssign(scope.row,resp.row)})'%{'director_name':self.get_director_name()}
    
    def dict_head(self, head):
        if head['editor'] =='com-field-picture':
            head['maxspan'] = 1200
        return head
    
    def get_operations(self):
        if self.permit.changeable_fields():
            return [
                { 'name':'save',
                  'editor':'com-op-submit',
                  'label':'确定', 
                  'default_after_save':'''cfg.toast("保存成功");
                  if(scope.ps.vc.par_row){
                     ex.vueAssign(scope.ps.vc.par_row,row)
                    } 
                    ''',
                  'action':'''if(!scope.ps.vc.ctx.after_save){scope.ps.vc.ctx.after_save=scope.head.default_after_save}; scope.ps.vc.submit()'''}
                
                #.then(row=>{
                       #cfg.toast("保存成功"); 
                       #if(scope.ps.vc.par_row){
                            #ex.vueAssign(scope.ps.vc.par_row,row)
                            #} 
                       #})
            ]
        else:
            return []

class FieldsMobile(Fields):
    def get_operations(self):
        return [
            { 'name':'save',
              #'editor':'com-op-submit',
              'editor':'com-btn',
              'label':'确定', 
              'default_after_save':'''cfg.toast("保存成功");
              if(scope.ps.vc.par_row){
                    ex.vueAssign(scope.ps.vc.par_row,row)
                    } 
              ''',
              'click_express':'if(!scope.ps.vc.ctx.after_save){scope.ps.vc.ctx.after_save=scope.head.default_after_save}; scope.ps.vc.submit()'}              
              #'action':'if(!scope.ps.vc.ctx.after_save){scope.ps.vc.ctx.after_save=scope.head.default_after_save}; scope.ps.vc.submit()'}
        ]

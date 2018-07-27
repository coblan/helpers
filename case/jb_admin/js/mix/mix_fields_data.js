var mix_fields_data ={
    data:function(){
        return {
            op_funs:{
            }
        }
    },
    mounted:function(){
        var self=this
        ex.assign(this.op_funs,{
            save:function(){
                self.save()
            }
        })
    },
    methods:{
        on_operation:function(op){
            var fun_name = op.fun || op.name
            this.op_funs[fun_name](op.kws)
        },
        on_field_event:function(kws){
            var fun_name = kws.fun || kws.name
            this.op_funs[fun_name](kws)
        },
        get_data:function(){
            this.data_getter(this)
        },
        setErrors:function(errors){
            ex.each(this.heads,function(head){
                if(errors[head.name]){
                    Vue.set(head,'error',errors[head.name].join(';'))
                }else if(head.error){
                    //delete head.error
                    Vue.delete(head,'error')
                    //Vue.set(head,'error',null)
                }
            })
        },
        dataSaver:function(callback){
            var post_data=[{fun:'save_row',row:this.row}]
            ex.post('/d/ajax',JSON.stringify(post_data),function (resp) {
                callback(resp.save_row)
            })
        },
        save:function () {
            var self =this;

            this.setErrors({})
            //eventBus.$emit('sync_data')
            ex.vueBroadCall('commit')

            if(self.before_save() == 'break'){
                return
            }
            //var loader = layer.load(2)
            cfg.show_load()
            self.dataSaver(function(rt){
                if( rt.errors){
                    cfg.hide_load()
                    self.setErrors(rt.errors)
                    self.showErrors(rt.errors)
                }else{
                    cfg.hide_load(2000)
                    self.after_save(rt.row)
                    self.setErrors({})
                }
            })
        },
        before_save:function(){
            return 'continue'
        },
        afterSave:function(resp){

        },
        after_save:function(new_row){
            ex.assign(this.row,new_row)
        },
        showErrors:function(errors){
            // 落到 nice validator去

            //var str = ""
            //for(var k in errors){
            //    var head = ex.findone(this.heads,{name:k})
            //    str += head.label + ':' + errors[k] +'<br>'
            //}
            //
            //layer.confirm(str,{title:['错误','color:white;background-color:red']})
        },
        clear:function(){
            this.row={}
            this.set_errors({})
        },

    }
}

window.mix_fields_data = mix_fields_data
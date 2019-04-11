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
                //self.save()
                self.submit()
            },
            submit:function(){
                self.submit()
            }
        })
        self.setErrors({})
    },
    created:function(){
        ex.each(this.heads,function(head){
            if(typeof head.readonly=='string'){
                head._org_readonly=head.readonly
                head.readonly=ex.eval(head._org_readonly,{row:self.row})
            }
            if(typeof head.required=='string'){
                head._org_required=head.required
                head.required=ex.eval(head._org_required,{row:self.row})
            }
            //if(typeof head.show=='string'){
            //    head._org_show=head.show
            //    head.show=ex.eval(head._org_show,{row:self.row})
            //}
        })
    },
    computed:{
        normed_heads:function(){
            var self=this
            ex.each(self.heads,function(head){
                if( head._org_readonly){
                    head.readonly=ex.eval(head._org_readonly,{row:self.row})
                }
                if( head._org_required){
                    head.required=ex.eval(head._org_required,{row:self.row})
                }
            })

            // 准备用下面两个替换前面所有逻辑
            var heads = ex.filter(self.heads,function(head){
                if(head.show){
                    return ex.eval(head.show,{row:self.row})
                }else{
                    return true
                }
            })

            ex.each(self.heads,function(head){
                if(head.express){
                    ex.vueAssign(head, ex.eval(head.express,{row:self.row}) )
                }
            })

            return heads

        }
    },
    methods:{
        get_row:function(director_name,data){
            // 后端可以控制，直接更新row数据
            cfg.show_load()
            ex.director_call(director_name,data).then(resp=>{
                cfg.hide_load()
                ex.vueAssign(this.org_row,resp)
                ex.vueAssign(this.row,resp)
            })
        },
        on_operation:function(op){
            if(op.action){
                ex.eval(op.action,{vc:this,row:this.row,head:this.head})
            }else{
                var fun_name = op.fun || op.name
                this.op_funs[fun_name](op.kws)
            }
        },
        on_field_event:function(kws){
            var fun_name = kws.fun || kws.name
            this.op_funs[fun_name](kws)
        },
        get_data:function(){
            this.data_getter(this)
        },
        setErrors:function(errors){
            // errors:{field:['xxx','bbb']}
            var errors=ex.copy(errors)
            if(!this.heads){
                return
            }
            ex.each(this.heads,function(head){
                if(errors[head.name]){
                    Vue.set(head,'error',errors[head.name].join(';'))
                    delete errors[head.name]
                }else if(head.error){
                    //delete head.error
                    Vue.delete(head,'error')
                    //Vue.set(head,'error',null)
                }
            })

            if(!ex.isEmpty(errors)){
                layer.alert(
                    JSON.stringify(errors)
                )
            }

        },
        dataSaver:function(callback){
            // 该函数已经被废弃
            var post_data=[{fun:'save_row',row:this.row}]
            ex.post('/d/ajax',JSON.stringify(post_data),function (resp) {
                callback(resp.save_row)
            })
        },
        submit:function(){
            var self =this;
            this.setErrors({})
            ex.vueBroadCall(self,'commit')
            Vue.nextTick(function(){
                if(!self.isValid()){
                    return
                }
                self.save()
            })

        },
        save:function () {
            var self=this
            cfg.show_load()
            var post_data=[{fun:'save_row',row:this.row}]
            this.old_row=ex.copy(this.row)
            ex.post('/d/ajax',JSON.stringify(post_data),function (resp) {
                var rt = resp.save_row
                if(rt.errors){
                    cfg.hide_load()
                    self.setErrors(rt.errors)
                    self.showErrors(rt.errors)
                }else{
                    if(resp.msg){
                        cfg.hide_load()
                    }else{
                        cfg.hide_load(2000)
                    }
                    ex.vueAssign(self.row,rt.row)
                    self.after_save(rt.row)
                    self.setErrors({})
                    self.$emit('finish',rt.row)
                }
            })
        },

        after_save:function(new_row){
            //ex.assign(this.row,new_row)
            //TODO 配合 table_pop_fields ，tab-fields 统一处理 after_save的问题
            if(this.tab_head){
                // 如果表单在一个tab 下,
                if(this.tab_head.after_save ){
                    if(typeof this.tab_head.after_save =='string'){
                        ex.eval(this.tab_head.after_save,{vc:this,})
                    } else{
                        // 为了兼容老的
                        if(this.tab_head.after_save){
                            if(this.parStore){
                                this.parStore.update_or_insert(new_row)
                            }
                        }
                        ex.vueAssign(this.org_row,new_row)
                    }
                }
                // 老的调用名字，新的后端调用名全部用 after_save
                else if(this.tab_head.after_save_express){
                    ex.eval(this.tab_head.after_save_express,{vc:this,})
                }
            }

        },
        showErrors:function(errors){
            // 落到 nice validator去
        },
        clear:function(){
            this.row={}
            this.set_errors({})
        },

    }
}

window.mix_fields_data = mix_fields_data
export  var mix_fields_data ={
    data:function(){
        return {
            before_submit:[],
            op_funs:{
            }
        }
    },
    mounted:function(){
        var self=this

        // TODO 把这段代码去掉
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
        if(this.head){
            // TODO 以后吧 style 代码去掉
            if(this.head.style){
                ex.append_css(this.head.style)
            }
            if(this.head.css){
                ex.append_css(this.head.css)
            }
            var mounted_express = this.head.mounted_express || this.head.init_express
            if (mounted_express){
                ex.eval(mounted_express,{row:this.row,ps:this.parStore,cs:this.childStore,vc:this,par_row:this.par_row})
            }
            //if(this.head.mounted_express){
            //    ex.eval(this.head.mounted_express,{row:this.row,ps:this.parStore,cs:this.childStore,vc:this})
            //}else if(this.head.init_express){
            //    ex.eval(this.head.init_express,{row:this.row,ps:this.parStore,cs:this.childStore,vc:this})
            //}
            ex.vueEventRout(this,this.head.event_slots)
        }
    },
    created:function(){
        var self=this
        ex.each(this.heads,function(head){
            if(typeof head.readonly=='string'){
                head._org_readonly=head.readonly
                //var is_readonly = ex.eval(head._org_readonly,{row:self.row})
                //Vue.set(head,'readonly',is_readonly)
            }
            if(typeof head.required=='string'){
                head._org_required=head.required
                //head.required=ex.eval(head._org_required,{row:self.row})
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
                    var is_readonly = ex.eval(head._org_readonly,{row:self.row,head:head})
                    Vue.set(head,'readonly',is_readonly)
                }
                if( head._org_required){
                    head.required=ex.eval(head._org_required,{row:self.row,head:head})
                }

                // 新的 readonly 动态判断
                if(head.readonly_express){
                    var is_readonly = ex.eval(head.readonly_express,{row:self.row,head:head})
                    Vue.set(head,'readonly',is_readonly)
                }
                if( head.required_express){
                    var required=ex.eval(head.required_express,{row:self.row,head:head})
                    Vue.set(head,'required',required)
                }
                if(head.help_text_express){
                    var help_text=ex.eval(head.help_text_express,{row:self.row,head:head})
                    Vue.set(head,'help_text',help_text)
                }
            })

            // 准备用下面两个替换前面所有逻辑
            var heads = ex.filter(self.heads,function(head){
                if (head.sublevel){
                    return false
                }else if(head.show || head.show_express){
                    var show_express = head.show_express || head.show
                    return ex.eval(show_express,{row:self.row,head:head,par_vc:self})
                }else{
                    return true
                }
            })

            // head.express  用来干啥?
            ex.each(self.heads,function(head){
                if(head.express){
                    ex.vueAssign(head, ex.eval(head.express,{row:self.row}) )
                }
            })
            return heads
        },
        normed_ops(){
            return ex.filter(this.ops,op=>{
                if(op.show || op.show_express){
                    var show_express= op.show_express || op.show
                    return ex.eval( show_express ,{vc:this})
                }else{
                    return true
                }
            })
        }
    },
    methods:{
        //updateRowBk:function(director_name,data){
        //    // 后端可以控制，直接更新row数据
        //    // 该函数废弃，替换为 直接调用 ex.director_call .then
        //
        //    cfg.show_load()
        //    ex.director_call(director_name,data).then(resp=>{
        //        cfg.hide_load()
        //        if(this.par_row){
        //            ex.vueAssign(this.par_row,resp.row)
        //        }
        //        ex.vueAssign(this.row,resp.row)
        //    })
        //},
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
            var self=this
            var errors=ex.copy(errors)
            if(!this.heads){
                return
            }
            ex.each(this.heads,function(head){
                if(errors[head.name]){
                    if(typeof errors[head.name] =='string' ){
                        var error_msg =errors[head.name]
                    }else{
                        var error_msg = errors[head.name].join(';')
                    }
                    Vue.set(head,'error',error_msg )
                    delete errors[head.name]

                }else if(head.error){
                    //delete head.error
                    //Vue.delete(head,'error')
                    Vue.set(head,'error','')
                    $(self.$el).find(`[name=${head.name}]`).trigger("hidemsg")
                    //Vue.set(head,'error',null)
                }
            })

            if(!ex.isEmpty(errors)){
                cfg.showMsg(  JSON.stringify(errors)  )
            }

        },
        dataSaver:function(callback){
            // 该函数已经被废弃
            var post_data=[{fun:'save_row',row:this.row}]
            ex.post('/d/ajax',JSON.stringify(post_data),function (resp) {
                callback(resp.save_row)
            })
        },
        async beforeSubmit(){
           return  await Promise.all( ex.map(this.before_submit,fun=>{return fun()}  )  )
        },
        submit(){
            var self =this;
            this.setErrors({})
            ex.vueBroadCall(self,'commit')
            return new Promise( function(resolve,reject){
                Vue.nextTick(async function(){
                    // await Promise.all( ex.map(self.before_submit,fun=>{return fun()}  )  )
                    await self.beforeSubmit()
                    if(self.head.before_submit_express){
                        await ex.eval(self.head.before_submit_express,{vc:self})
                    }

                    if(!self.isValid()){
                        //reject()
                    }else{
                        var res = await  self.save()
                        resolve(res)
                    }
                })
            })

        },
        real_save:function () {
            /*三种方式设置after_save
            * 1. ps.submit().then((new_row)=>{ps.update_or_insert(new_row)})
            * 2. head.after_save = "scope.ps.update_or_insert(scope.row)"
            * 3. @finish="onfinish"   函数: onfinsih(new_row){}
            * */
            var self=this
            cfg.show_load()
            var post_data=[{fun:'save_row',row:this.row}]
            this.old_row=ex.copy(this.row)
            var p = new Promise((resolve,reject)=>{
                //ex.post('/d/ajax',JSON.stringify(post_data), (resp) =>{
                ex.director_call('d.save_row',{row:this.row}).then( (resp) =>{
                    cfg.hide_load()
                    delete self.row.meta_overlap_fields
                    delete self.row.meta_change_fields

                    var rt = resp //resp.save_row
                    if(rt.errors){
                        //cfg.hide_load()
                        self.setErrors(rt.errors)
                        self.showErrors(rt.errors)
                        //reject(rt.errors)
                    }else if(rt._outdate){
                        cfg.outdate_confirm(
                            rt._outdate,
                            function() {
                                ex.update_row(self.row)
                                // ex.director_call(self.row._director_name, {pk: self.row.pk}).then(resp=> {
                                //     ex.vueAssign(self.row, resp.row)
                                // })
                            },function(){
                                    self.row.meta_overlap_fields='__all__'
                                    self.submit()
                                }
                        )
                    }else{
                        ex.vueAssign(self.row,rt.row)
                        if(this.head && this.head.after_save_express){
                            ex.eval(this.head.after_save_express,{ps:self.parStore,vc:self,row:rt.row})
                        }else  if(this.head && this.head.after_save && typeof this.head.after_save =='string'){
                            // 老的调用，新的使用 after_save_express
                            ex.eval(this.head.after_save,{ps:self.parStore,vc:self,row:rt.row})
                        }else{
                            // 调用组件默认的
                            self.after_save(rt.row)
                            if(resp.msg || rt.msg){
                                //cfg.hide_load()
                                cfg.showMsg(resp.msg || rt.msg)
                            }else{
                                cfg.toast('操作成功！',{time: 1000})
                            }
                            if (this.head.extra_after_save_express){
                                ex.eval(this.head.extra_after_save_express,{ps:self.parStore,vc:self,row:rt.row})
                            }
                        }

                        self.setErrors({})
                         resolve(self.row)
                    }
                })
            })
            return p
        },
        async save(){
            var row = await this.real_save()
            this.$emit('finish',row)
            return row
        },

        after_save:function(new_row){

            //ex.assign(this.row,new_row)
            //TODO 配合 table_pop_fields ，tab-fields 统一处理 after_save的问题
            if(this.par_row){
                if(this.par_row._director_name == new_row._director_name){
                    if(this.par_row.pk == new_row.pk){
                        ex.vueAssign(this.par_row,new_row)
                    }else if(!this.par_row.pk){
                        ex.vueAssign(this.par_row,new_row)
                        this.parStore.update_or_insert(this.par_row)
                    }
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
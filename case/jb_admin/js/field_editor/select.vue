<template>
    <div class="com-field-select" :class="head.class">
        <span v-if='head.readonly' v-text='get_label'></span>
        <div v-else>
            <input type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]"><!-- :clearable="!head.required"-->
            <el-select  v-model="row[head.name]"
                        :filterable="head.multiple ||  head.filterable "
                        :placeholder="head.placeholder"
                        size="small"
                        :multiple="head.multiple"
                        :clearable="!head.multiple && !head.required">
                <el-option
                        v-for="item in normed_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
                </el-select>
        </div>
    </div>
</template>
<script>
    export default {
        props: ['row', 'head'],
        data: function () {
            var inn_config = {
//orgin_order:true,
                order: false
            }
            if (this.head.config) {
                ex.assign(inn_config, this.head.config)
            }

            this.head.placeholder = this.head.placeholder || '请选择'

            return {
                model: this.row[this.head.name],
                cfg: inn_config,
                parStore:ex.vueParStore(this),
                options:this.head.options || [],
            }
        },
        mounted: function () {
            // 如果有默认值，
            if (this.head.default && !this.row[this.head.name]) {
                Vue.set(this.row, this.head.name, this.head.default)
            }
            var self=this
            // 兼容老的调用,新的请在 on_mounted 里面调用
            // remote_options 只用在初始化的时候，请求远端服务器获取options。如果需要动态切换options，请设置 director_name 。
            // TODO 清楚这段代码
            if(this.head.remote_options){
                ex.director_call(this.head.remote_options,{crt_value:this.row[this.head.name]},function(resp){
                    self.head.options=resp
                    self.options = resp
                })
            }
            // TODO 清楚这段代码
            if(this.head.on_mounted){
                ex.eval(this.head.on_mounted,{vc:this})
            }

            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this})
            }
            // 这种方式，一般是与filter共用options的时候
            // TODO 清楚这段代码。用 mounted_express 代替
            if(this.head.ctx_name){
                self.head.options = named_ctx[this.head.ctx_name]
            }
            ex.vueEventRout(this)

            if(this.head.css){
                ex.append_css(this.head.css)
            }

        },

        watch:{
            my_value:function(v){
                this.$emit('input',v)
            }
        },

        computed:{

            novalue(){
                if(this.row[this.head.name] ==0){
                    var novalue = undefined
                }else if(! this.row[this.head.name]){
                    var novalue = this.row[this.head.name]
                }else{
                    var novalue = undefined
                }
                return novalue
            },
            my_value:function(){
                return this.row[this.head.name]
            },
            is_select:function(){
                var v = this.row[this.head.name]
                return v !== this.novalue
            },
            place_value:function(){
                var v = this.row[this.head.name]
                if(v === undefined){
                    return undefined
                }else  if(v === null){
                    return null
                }else{
                    return ''
                }
            },
            normed_options:function(){
                /*
                 head.hide_related_field设置 隐藏与 row.hide_related_field 相等的选项

                 * */
                var self=this
                if(this.head.hide_related_field){
                    var array = ex.filter(this.options,function(item){
                        return item.value != self.row[self.head.hide_related_field]
                    })
                }else{
                    if(this.head.option_show){
                        var array = ex.filter(this.options,(item)=>{
                                    return ex.eval(this.head.option_show,{option:item,row:self.row,ps:self.parStore,vc:self})
                                })
                    }else {
                        var array = ex.filter(this.options,(item)=>{
                                    if(item.show){
                            return ex.eval(item.show,{option:item,row:self.row,ps:self.parStore,vc:self})
                        }else{
                            return true
                        }
                    })
                    }
                }
                return array

//                return self.orderBy(array,'label')

            },
            get_label(){
                var value=this.row[this.head.name]
                if(value !=0 && !value){
                    return ''
                }
                if(this.head.multiple){
                    var list = ex.map(value,item=>{
                                var option = ex.findone(this.options,{value:item})
                                if(option){
                                    return option.label
                                }else{
                                    return item
                                }


                            })
                    return list.join(';')
                } else{
                    //                var option = ex.findone(options,{value:value})
                    var option = ex.findone(this.options,{value:value})
                    if(!option){
                        return '---'
                    }else{
                        return option.label
                    }
                }

            },
        },
        methods:{
            update_options:function(post_data){
                var self=this
                if(this.head.director_name){
                    cfg.show_load()
                    ex.director_call(self.head.director_name,post_data,function(data){
                        cfg.hide_load()
                        Vue.set(self.head,'options' ,data)
                    })
                }
            },

            orderBy:function(array,key){
                if(this.head.order || this.cfg.order){
                    return order_by_key(array,key)
                }else{
                    return array
                }

            }
        }
    }
</script>
<style scoped lang="scss">
.com-field-select{
    .novalue{
        color: #b7b7b7;
    }
    option{
        color: black;
    }

    }

</style>
<style lang="scss">
    .el-select-dropdown li.selected{
        display: none;
    }
</style>

<template>
    <div class="com-field-radio">
        <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
        <el-radio-group v-else v-model="row[head.name]">
            <el-radio v-for="opt in normed_options" :label="opt.value" v-text="opt.label"></el-radio>
        </el-radio-group>

        <!--<select v-else v-model='row[head.name]'  :id="'id_'+head.name" :name="head.name"  :class="['form-control input-sm',{ novalue: ! is_select}] ">-->
            <!--&lt;!&ndash;<option v-if="head.required"  :value="undefined" disabled selected style='display:none;' class="placeholder" v-text="head.placeholder"></option>&ndash;&gt;-->
            <!--&lt;!&ndash;<option v-else  :value="undefined" selected style="color: #b8b8b8" class="placeholder" v-text="head.placeholder"></option>&ndash;&gt;-->
            <!--<option v-if="head.required"  :value="novalue" disabled selected style='display:none;color: #b8b8b8' class="placeholder" v-text="head.placeholder"></option>-->
            <!--<option v-else   :value="novalue" selected style="color: #b8b8b8" class="placeholder" v-text="head.placeholder"></option>-->

            <!--<option v-for='opt in normed_options' :value='opt.value' v-text='opt.label'></option>-->
        <!--</select>-->
    </div>
</template>
<script>
/*
选项比较少，且必须有选择的时候，可以用这个控件
* */
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
            }
        },
        template: ``,
        mounted: function () {
// 如果有默认值，
            if (this.head.default && !this.row[this.head.name]) {
                Vue.set(this.row, this.head.name, this.head.default)
            }
            var self=this
            // 兼容老的调用,新的请在 on_mounted 里面调用
            // remote_options 只用在初始化的时候，请求远端服务器获取options。如果需要动态切换options，请设置 director_name 。
            if(this.head.remote_options){
                ex.director_call(this.head.remote_options,{crt_value:this.row[this.head.name]},function(resp){
                    self.head.options=resp
                })
            }
            if(this.head.on_mounted){
                ex.eval(this.head.on_mounted,{vc:this})
            }
// 这种方式，一般是与filter共用options的时候
            if(this.head.ctx_name){
                self.head.options = named_ctx[this.head.ctx_name]
            }
            ex.vueEventRout(this)

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
                    var array = ex.filter(this.head.options,function(item){
                        return item.value != self.row[self.head.hide_related_field]
                    })
                }else{
                    if(this.head.option_show){
                        var array = ex.filter(this.head.options,(item)=>{
                                    return ex.eval(this.head.option_show,{option:item,row:self.row,ps:self.parStore,vc:self})
                                })
                    }else {
                        var array = ex.filter(this.head.options,(item)=>{
                                    if(item.show){
                            return ex.eval(item.show,{option:item,row:self.row,ps:self.parStore,vc:self})
                        }else{
                            return true
                        }
                    })
                    }
                }

                return self.orderBy(array,'label')

            }
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
            get_label:function(options,value){
                var option = ex.findone(options,{value:value})
                if(!option){
                    return '---'
                }else{
                    return option.label
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

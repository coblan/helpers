<template>
    <div class="com-field-radio">
<!--        <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>-->
        <el-checkbox-group v-model="inn_value">
            <el-checkbox v-for="opt in normed_options" :label="opt.value">{{opt.label}}</el-checkbox>
        </el-checkbox-group>
    </div>
</template>
<script>
    export default {
        props: ['row', 'head'],
        data: function () {
            this.head.placeholder = this.head.placeholder || '请选择'
            return {
              inn_value:this.row[this.head.name] || [],
              parStore:ex.vueParStore(this),
            }
        },
        mounted: function () {
            var self=this
            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this})
            }
        },

        watch:{
          inn_value:function(v){
                this.row[this.head.name] = v
            },
          out_value(nv){
            if(nv){
              this.inn_value = nv
            }else{
              this.inn_value = []
            }
          }
        },

        computed:{
            out_value:function(){
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

                  if(this.head.option_show_express){
                      var array = ex.filter(this.head.options,(item)=>{
                                  return ex.eval(this.head.option_show_express,{option:item,row:self.row,ps:self.parStore,vc:self})
                              })
                    return  array
                  }else {
                     return this.head.options
                  }


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

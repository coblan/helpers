<template>
    <div class="com-filter-exact-text">
        <el-input class="input-with-select"
                  :placeholder="myplaceholder"
                  @keyup.native.13="parStore.search()"
                  size="small"
                  maxlength="200"
                  v-model="search_args[head.name]">
    <span slot="prefix" class="myicon el-input__icon">
        <img src="/static/jb_admin/equal.png" alt="">
    </span>
        </el-input>
    </div>
</template>

<script>
    export default {
        props:['head','search_args','config'],
        data:function(){
            var self=this
            return {
                parStore:ex.vueParStore(this)
            }
        },

        computed:{
            myvalue:function(){
                return this.search_args[this.head.name]
            },
            myplaceholder(){
                if(this.head.show_label){
                    return this.head.placeholder
                }else{
                    return this.head.placeholder ||this.head.label
                }
            }
        },
        watch:{
            myvalue:function(v){
                this.$emit('input',v)
            },
            options:function(v){
                delete  this.search_args[this.head.name]
            }
        },
        mounted:function(){
            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this,ps:this.parStore})
            }

        },
        methods:{
            clear_value:function(){
                delete this.search_args[this.head.name]
            },

        }
    }


//    var filter_input = {
//        props:['head','search_args','config'],
//        template:`<div class="com-filter-input">
//    <span v-if="head.show_label"><span  v-text="head.label"></span>:</span>
//        <input @keyup.enter="parStore.search()" type="text" v-model='search_args[head.name]' class="form-control input-sm" :placeholder="myplaceholder">
//    </div>
//    `,
</script>

<style scoped lang="scss">
    .myicon{
    img{
        width: 12px;
        display: inline-block;
        height: 6px;
        position: relative;
        left: 4px;
        top: -2px;
    }
    }
</style>





















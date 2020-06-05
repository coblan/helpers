<template>
    <div class='com-filter-check'>

        <el-checkbox  v-model="search_args[head.name]" :label="head.label" border size="small"></el-checkbox>
        <!--<label style="font-weight: 400" :for="'filter_'+head.name" v-text="head.label"></label>-->
        <!--<input :id="'filter_'+head.name" type="checkbox" v-model="search_args[head.name]">-->
    </div>
</template>
<script>
    export default {
        props:['head','search_args','config'],
        data:function(){
            var self=this
            return {
                order:this.head.order || false,
                parStore:ex.vueParStore(this)
            }
        },

        computed:{
            myvalue(){
                return this.search_args[this.head.name]
            },
            options:function(){
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
            if(this.head.event_slots){
                this.set_event_slot()
            }

        },
        methods:{

        }
    }
</script>
<style scoped lang="scss">
.com-filter-check /deep/ .el-checkbox.is-bordered.el-checkbox--small{
    height: 30px;
    margin-bottom: 0;
    color: #a0a0a0;
}
</style>


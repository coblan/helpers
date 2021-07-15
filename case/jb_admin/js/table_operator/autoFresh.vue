<template>
    <div class="com-op-table-refresh" style="display: inline-block;margin: 0 1px 0 3px">
        <select v-model='myvalue' class="form-control input-sm com-filter-select" >
            <option class="fake-placeholder"  value="" v-text='head.label' ></option>
            <option v-for='option in head.options' :value="option.value" v-text='option.label'></option>
        </select>
        <div v-show="is_loading" class="my-load">loading...</div>
    </div>
</template>

<script>
    export default {
        props:['head','disabled'],
        data:function(){
            var parStore = ex.vueParStore(this)
            return {
                myvalue:this.head.init_value || '',
                parStore : parStore,
                timeout_index:0,
                is_loading:false,
            }
        },
        watch:{
            myvalue(v){
                if(this.timeout_index){
                    clearTimeout(this.timeout_index)
                }
                if(v){
                    this.start_refresh()
                }
            },
        },
        methods:{
            start_refresh(){
                if(this.myvalue){
                    this.timeout_index =  setTimeout(()=>{
                                    this.is_loading=true
                                ex.eval(this.head.action_express,{ps:this.parStore}).then(()=>{
                                    this.is_loading=false
                                this.start_refresh()
                })

                },this.myvalue)
                }
            }
        }
    }
</script>
<style scoped lang="scss">
    .com-op-table-refresh{
        position: relative;
    }
.my-load{
    position: absolute;
    top:0;
    left: 0;
    right: 0;
    right: 0;
    text-align: center;
    line-height: 30px;
    background-color:rgba(0,0,0,0.7);
    color: white;
}
</style>
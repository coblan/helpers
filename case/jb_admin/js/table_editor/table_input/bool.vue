<template>
    <div class="com-table-input-int" >

        <el-checkbox v-model="rowData[field]"></el-checkbox>
        <span v-show="step=='upload'"><i class="el-icon-loading"></i></span>
        <div v-show="step=='upload'" class="overlap"></div>
    </div>
</template>
<script>
    import {save_row} from './save_fun'
    export default {
        props:['rowData','field','index'],
        data(){
            return {
                org_value :this.rowData[ this. field],
                step:'read',
            }
        },
        computed:{
            myvalue(){
                return this.rowData[ this. field]
            }
        },
        watch:{
            myvalue(v){
                this.step = 'upload'
                save_row(this.rowData).then(()=>{
                    this.step = "read"
                 })
            }
        },
        methods:{
            on_click(){
                Vue.nextTick(()=>{
                    if(this.org_value !=this.rowData[ this. field] ) {
                        this.step = 'upload'
                        save_row(this.rowData).then(()=>{
                            this.step = "read"
                        this.orgin_value = this.rowData[this.field]
                        })
                    }
                })

            }
        }
    }
</script>
<style scoped lang="scss">
    .overlap{
        position: absolute;
        top:0;
        left: 0;
        right: 0;
        bottom: 0;
        /*background-color: black;*/
        /*opacity: 0.2;*/
        z-index: 10;
    }
</style>
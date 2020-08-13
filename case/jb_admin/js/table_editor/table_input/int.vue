<template>
    <div class="com-table-input-int" @click="on_click">
        <span  v-show="step=='read' || step=='upload'" v-text="rowData[field]"></span>
        <span v-show="step=='upload'"><i class="el-icon-loading"></i></span>
        <input class="my-input" ref="myinput" @blur="on_blur" v-show="step=='write'"
               @keypress="isNumber($event)"
               type="text" v-model="rowData[field]">
        <!--<el-input class="my-input" ref="myinput" size="small" @blur="on_blur" v-show="step=='write'"-->
               <!--@keypress.native="isNumber($event)"-->
               <!--type="text" v-model="rowData[field]"></el-input>-->
    </div>
</template>

<script>
    import {save_row} from './save_fun'
    export default {
        props:['rowData','field','index'],
        data(){
            return {
                step:'read',
                orgin_value:this.rowData[this.field],
//                inn_value:this.rowData[this.field]
            }
        },
        created:function(){
            // find head from parent table
            var table_par = this.$parent
            while (true){
                if (table_par.heads){
                    break
                }
                table_par = table_par.$parent
                if(!table_par){
                    break
                }
            }
            this.table_par = table_par
            this. head  = ex.findone(this.table_par.heads,{name:this.field})
        },

        methods:{
            on_click(){
                if(this.step == 'read'){
                    this.step= 'write'
                    Vue.nextTick(()=>{
                        $( this.$refs.myinput ).focus()
                    })

                }
            },
            on_blur(){
                if (this.rowData[this.field] ==''){
                    if(this.head.required){
                        this.rowData[this.field] = this.orgin_value
                    }
                }
                this.rowData[this.field] = parseInt( this.rowData[this.field] )
                if(this.orgin_value != this.rowData[this.field] ) {
                    this.step = 'upload'
                    save_row(this.rowData).then(()=>{
                        this.step = "read"
                        this.orgin_value = this.rowData[this.field]
                    })
                }else{
                    this.step = "read"
                }

            },
            isNumber:function(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
                if(charCode== 46){
                    return evt.preventDefault();
                }

                if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
                    if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
                        return evt.preventDefault();
                    }else{
                        return true
                    }
                }else{
                    return evt.preventDefault();
                }
            }
        }
    }
</script>

<style scoped lang="scss">
.my-input{
    width: 100%;
}
</style>
<template>
    <div class="com-table-local-number" >
        <!--<span  v-show="step=='read' || step=='upload'" v-text="rowData[field]"></span>-->
        <!--<span v-show="step=='upload'"><i class="el-icon-loading"></i></span>-->
        <!--<input class="my-input" ref="myinput" @blur="on_blur" v-show="step=='write'"-->
               <!--@keypress="isNumber($event)"-->
               <!--type="text" v-model="rowData[field]">-->
        <input class="my-input" ref="myinput"
               @keypress="isNumber($event)"
               type="number" v-model="rowData[field]">
        <!--<el-input class="my-input" ref="myinput" size="small" @blur="on_blur" v-show="step=='write'"-->
        <!--@keypress.native="isNumber($event)"-->
        <!--type="text" v-model="rowData[field]"></el-input>-->
    </div>
</template>

<script>
//    import {save_row} from './save_fun'
    export default {
        props:['rowData','field','index'],
        data(){
            return {
                step:'read',
                orgin_value:this.rowData[this.field],
//                inn_value:this.rowData[this.field]
            }
        },
        mounted(){
            if(typeof this.rowData[this.field] =='string'){
                this.rowData[this.field] = this.rowData[this.field].trim()
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
//            on_click(){
//                if(this.step == 'read'){
//                    this.step= 'write'
//                    Vue.nextTick(()=>{
//                        $( this.$refs.myinput ).focus()
//                })
//
//                }
//            },
//            on_blur(){
//                if (this.rowData[this.field] ==''){
//                    if(this.head.required){
//                        this.rowData[this.field] = this.orgin_value
//                    }
//                }
//                this.rowData[this.field] = parseInt( this.rowData[this.field] )
//                if(this.orgin_value != this.rowData[this.field] ) {
//                    this.step = 'upload'
//                    save_row(this.rowData).then((row)=>{
//                        this.orgin_value = this.rowData[ this.field]
//                }).catch(()=>{
//                        this.rowData[ this. field] = this.orgin_value
//                }).finally (()=>{
//                        this.step = "read"
//                })
//
//                }else{
//                    this.step = "read"
//                }
//
//            },
            isNumber:function(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
//                if(charCode== 46){
//                    return evt.preventDefault();
//                }

                if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
                    var value = this.rowData[this.field]
                    if(charCode==46 && value.indexOf('.')!=-1){
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


    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        /* display: none; <- Crashes Chrome on hover */
        -webkit-appearance: none;
        margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
    }

    input[type=number] {
        -moz-appearance:textfield; /* Firefox */
    }
</style>
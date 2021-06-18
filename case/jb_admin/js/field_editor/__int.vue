<template>
    <div :class="['com-field-int','field-'+head.name,head.class]" >
        <span v-if='head.readonly && !head.prefix ' >
            <span v-text='row[head.name]'></span>
            <span v-text="head.suffix"></span>
        </span>
        <div  v-else class="form-inline">


            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder" :readonly="head.readonly"
                      :name="head.name"
                      :id="'id_'+head.name"
                      @keypress.native="isNumber($event)"
                      @blur.native="on_blur"
                      :autofocus="head.autofocus">
                <template slot="prepend" >
                    <span  v-if="head.prefix" v-html="head.prefix"></span>
                </template>
                <template slot="append">
                    <span  v-if="head.suffix" v-html="head.suffix"></span>
                </template>
            </el-input>

        </div>

    </div>
</template>

<script>
    export default {
        props:['row','head'],
        data(){
//            Vue.set(this.row,this.head.name,this.row[this.head.name] || '')
            return {
//              mydata:this.row[this.head.name]
            }
        },
        created(){
            this.head.fv_rule +=';integer'
        },
//        computed:{
//            mydata:{
//                get(){
//                    return this.row[this.head.name]
//                },
//                set(v,ov){
//                    if(/^-*\d+$/.test(v)){
//                        Vue.set(this.row,this.head.name,parseInt(v))
//                    }else{
//                        Vue.set(this.row,this.head.name,ov)
//                    }
////                    if(v ){
////                        Vue.set(this.row,this.head.name,parseInt(v))
//////                        this.row[this.head.name] = parseInt(v)
////                    }else{
////                        this.row[this.head.name] =v
////                    }
//                }
//            }
//        },
//        watch:{
//          mydata(v){
//              if(v || v==0){
//                  this.row[this.head.name] = parseInt(v)
//              }
//          }
//        },

        mounted(){
            if(this.head.mounted_express){
                ex.eval(this.head.mounted_express,{vc:this})
            }
        },
        methods:{
//            on_blur(){
//                this.row[this.head.name] =
//            },
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

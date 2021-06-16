<template>
    <line-text class="com-field-int" :row="row" :head="head">
        <template v-slot:inputbody>
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
        </template>
    </line-text>
</template>

<script>
    import lineText from './lineText.vue'
    import {LineTextLogic} from './lineText.vue'

    export class IntInputLogic extends LineTextLogic{
        constructor(){
            super()
            this.fv_rule=';integer'
        }
        setup(props){
            if(this.fv_rule){
                props.head.fv_rule += this.fv_rule
            }
            super.setup(props)
            return {
                isNumber:this.isNumber
            }
        }
        isNumber(evt){
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

    export default {
        props:['row','head','extendObj'],
        components:{
            lineText,
        },
        data(){
//            Vue.set(this.row,this.head.name,this.row[this.head.name] || '')
          return {
//              mydata:this.row[this.head.name]
          }
        },
        setup(props){
            if(props.extendObj){
                return props.extendObj
            }else{
                return  new IntInputLogic().setup(props)
            }


        },
        methods:{
//            on_blur(){
//                this.row[this.head.name] =
//            },
        }
    }
</script>

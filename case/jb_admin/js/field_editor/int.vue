<template>
    <line-text class="com-field-int" :row="row" :head="head">
        <template v-slot:inputbody>
            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder" :readonly="head.readonly"
                      :name="head.name"
                      :id="'id_'+head.name"
                      @keypress.native="isNumber($event)"
                      @blur="onBlur"
                      @focus="onFocus"
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
    // import {LineTextLogic} from './lineText.vue'

    function append_rule(props,new_rule){
        if(props.head.fv_rule){
          var fv_rule= props.head.fv_rule +';'+ new_rule
        }else{
          var fv_rule=  new_rule
        }
        Vue.set(props.head,'fv_rule',fv_rule)
    }
    function check_number(){
      var isNumber = (evt)=>{
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
      return {
        isNumber
      }
    }

    // export class IntInputLogic extends LineTextLogic{
    //     constructor(){
    //         super()
    //        this.fv_rule=';integer'
    //     }
    //     getSetup(props){
    //         if(this.fv_rule){
    //             if(props.head.fv_rule){
    //               var fv_rule= props.head.fv_rule + this.fv_rule
    //             }else{
    //               var fv_rule=  this.fv_rule
    //             }
    //             Vue.set(props.head,'fv_rule',fv_rule) //  props.head.fv_rule = this.fv_rule
    //         }
    //         var dc = super.getSetup(props)
    //         Object.assign(dc,{
    //             isNumber:this.isNumber
    //         })
    //         return dc
    //     }
    //     isNumber(evt){
    //         evt = (evt) ? evt : window.event;
    //         var charCode = (evt.which) ? evt.which : evt.keyCode;
    //         if(charCode== 46){
    //             return evt.preventDefault();
    //         }
    //
    //         if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
    //             if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
    //                 return evt.preventDefault();
    //             }else{
    //                 return true
    //             }
    //         }else{
    //             return evt.preventDefault();
    //         }
    //     }
    // }

    export default {
        props:['row','head','extendLogic'],
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
          append_rule(props, 'integer')
          var {isNumber} = check_number()
          return  {
            isNumber
          }

            // if(props.extendLogic){
            //     return new  props.extendLogic().getSetup(props)
            // }else{
            //     return  new IntInputLogic().getSetup(props)
            // }


        },
        methods:{
          onFocus(){
            this.inter_index = setInterval(this.filterIllegal,500)
          },
          onBlur(){
            if(this.inter_index){
              clearInterval(this.inter_index)
              this.inter_index=''
            }
            // this.filterIllegal()
          },
          filterIllegal(){
            var value = this.row[this.head.name]
            const newValue =
                value
                    .replace(/[^\d^\.^-]+/g, '')   // 把不是数字，不是小数点的过滤掉
                    .replace(/^0+(\d)/, '$1')      // 以0开头，0后面为数字，则过滤掉，取后面的数字
                    .replace(/^-0+(\d)/, '-$1')    // 以-0开头，0后面为数字，则过滤掉，取后面的数字
                    .replace(/-/g, (match, offset) => offset === 0 ? '-' : '') // 只允许第一个是负号-
                    .replace(/\./, '#').replace(/\./, '').replace(/#/, '\.') // 只保留第一个小数点

            this.row[this.head.name] = newValue
          }
//            on_blur(){
//                this.row[this.head.name] =
//            },
        }
    }
</script>

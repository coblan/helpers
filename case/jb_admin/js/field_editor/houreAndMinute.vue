<template>
  <div>
    <input type="text" @keypress="isNumber($event)">小时
    <input type="text">分钟
  </div>

</template>

<script>
import  elint from 'weblib/pc/fields/'
// import lineText from './lineText.vue'
// import {LineTextLogic} from './lineText.vue'

// export class IntInputLogic extends LineTextLogic{
//   constructor(){
//     super()
//     this.fv_rule=';integer'
//   }
//   getSetup(props){
//     if(this.fv_rule){
//       if(props.head.fv_rule){
//         var fv_rule= props.head.fv_rule + this.fv_rule
//       }else{
//         var fv_rule=  this.fv_rule
//       }
//       Vue.set(props.head,'fv_rule',fv_rule) //  props.head.fv_rule = this.fv_rule
//     }
//     var dc = super.getSetup(props)
//     Object.assign(dc,{
//       isNumber:this.isNumber
//     })
//     return dc
//   }
//
// }

export default {
  props:['row','head'],
  data(){
//            Vue.set(this.row,this.head.name,this.row[this.head.name] || '')
    return {
//              mydata:this.row[this.head.name]
    }
  },
  // setup(props){
  //   if(props.extendLogic){
  //     return new  props.extendLogic().getSetup(props)
  //   }else{
  //     return  new IntInputLogic().getSetup(props)
  //   }
  //
  // },
  methods:{
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
//            on_blur(){
//                this.row[this.head.name] =
//            },
  }
}
</script>

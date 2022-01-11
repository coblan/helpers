<template>
  <div class="hour-and-minute">
    <template v-if="head.readonly">
      <span>{{show_text}}</span>
    </template>
    <template v-else>
      <input type="text"  v-model="row[head.name]"
             :id="'id_'+head.name" :name="head.name" style="display: none;">

      <elInt class="hour-input" size="small" type="text" @keypress="isNumber($event)" v-model="my_hour"></elInt><span style="white-space: nowrap">小时</span>
      <el-select style="width:100px"  size="small" v-model="minute" >
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
      </el-select>
      <span style="white-space: nowrap">分钟</span>
    </template>

  </div>

</template>

<script>
import  elInt from 'weblib/pc/fields/elInt.vue'
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
  components:{
    elInt,
  },
  props:['row','head'],
  data(){
//            Vue.set(this.row,this.head.name,this.row[this.head.name] || '')
    var options= []
    for(var i =1;i<60;i++){
      options.push({value:i,label:i})
    }
    return {
      my_hour:'',
      minute:'',
      options:options
//              mydata:this.row[this.head.name]
    }
  },
  computed:{
    show_text(){
        if(this.mydata){
          var minut = this.mydata%60
          minut = minut.toString(). padStart(2, '0')
          return `${parseInt( this.mydata/60)}:${minut}`
        }else{
          return  0
        }
    },
    mydata(){
      return  this.row[this.head.name]
    }
  },
  watch:{
    my_hour(nv){
      this.readOutData()
    },
    minute(){
      this.readOutData()
    },
    mydata(nv){
      this.writeInData()
    }
  },
  mounted(){
    this.writeInData()
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
    readOutData(){
      this.row[this.head.name] = 0
      if(this.my_hour){
        this.row[this.head.name] = this.my_hour * 60
      }
      if(this.minute){
        this.row[this.head.name] += this.minute
      }
    },
    writeInData(){
      var vv = this.row[this.head.name]
      if(vv){
          this.my_hour = parseInt(vv/60)
          this.minute = parseInt(vv%60)
      }
    },
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
}
</script>
<style scoped lang="scss">
.hour-and-minute{
  display: flex;
  align-items: center;

  .hour-input{
    width: 100px;;
  }
  /deep/ input{
    width: 90%;
  }
}
</style>

<template>
  <div class="com-table-batch-int">
    <span  v-show="step=='read'">{{rowData[field]}}</span>
    <input class="my-input" ref="myinput" v-show="step=='write'"
           @keypress="isNumber($event)" @keyup.enter="on_enter"
           type="text" v-model="rowData[field]">
  </div>
</template>

<script>

class IntLogic{
  getSetup(props){
    var isNumber=function(evt){
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
}

export default {
  props:['rowData','field','index','extendLogic'],
  data(){
    var parStore = ex.vueParStore(this)

    return {
      parStore:parStore,
      head:ex.findone(parStore.vc.tableHeads,{name:this.field}),
      step:'read',
      orgin_value:this.rowData[this.field],
//                inn_value:this.rowData[this.field]
    }
  },
  setup(props){
    if(props.extendLogic){
        var logic = new props.extendLogic()
        return logic.getSetup(props)
    }else{
       var logic = new IntLogic()
       return  logic.getSetup(props)
    }
  },
  mounted(){
    if( this.head.mounted_express){
      ex.eval(this.head.mounted_express,{ps:this.parStore,head:this.head,vc:this})
    }
    if(this.head.enter_index){
      var crt_index = this.rowData[this.head.enter_index]
      this.parStore.vc.$on('enter_index:'+crt_index,()=>{
        $( this.$refs.myinput ).focus()
      })
    }
  },

  methods:{
    start_edit(){
      this.step = 'write'
    },
    on_enter(){
      if(this.head.enter_index){
        var crt_index = this.rowData[this.head.enter_index]
        var next_index = crt_index+1
        this.parStore.vc.$emit('enter_index:'+next_index)
      }
    }
    // on_click(){
    //   if(this.step == 'read'){
    //     this.step= 'write'
    //     Vue.nextTick(()=>{
    //       $( this.$refs.myinput ).focus()
    //     })
    //
    //   }
    // },


  }
}
</script>

<style scoped lang="scss">
.my-input{
  width: 100px;
}
</style>
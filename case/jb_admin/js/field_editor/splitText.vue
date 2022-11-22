<template>
  <div :class="['com-field-split-text',head.class]" :style="head.style" @click="onClick">
    <span class="readonly-info" v-if='head.readonly' v-text='row[head.name]'></span>
    <input v-else type="text" :class="['my-input-field',head.input_class]" v-model="row[head.name]"
           :id="'id_'+head.name" :name="head.name"
           :placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  data(){
    return {
      last_value:'',
      clicking:false,
    }
  },
  mounted(){
    if(this.head.css){
      ex.append_css(this.head.css)
    }
    var self=this

    setTimeout(()=>{

//var value = self.row[self.head.name]
//
//if (value){
//    var items =   value.split(',') //ex.map(value.split(','),ii=>{ return {label:ii} })
//}else{
//    var items = []
//}
//var options = self.head.options .concat(items)

      var bb = $(this.$el).find('.my-input-field').selectize({
        delimiter: this.head.splitter ||  ',',
        persist: false,
        create: true,
        createOnBlur:true,
//items:items,
//create: function(input) {
//    return {
//        value: input,
//        text: input
//    }
//},
//create: function(input) {
//    return {
//        label: input,
//    }
//},
        maxItems:this.head.maxItems,
        hideSelected:true,
        valueField: 'value',
        labelField:'label',
        searchField:'label',
//options:  self.head.options ||  [], //options,// items ,//
        onChange:function(value){
          self.row[self.head.name] = value
        },
        onBlur:function(){
          self.last_value = self.row[self.head.name]
          $(self.$el).find('.my-input-field').trigger('validate')
        },
        onFocus(){
          // if(self.head.maxItems==1){
          //   var value = this.getValue()
          //   this.clear()
          //   setTimeout(()=>{
          //     this.setTextboxValue(value)
          //   },100)
          // }
        }
      });
      Vue.nextTick(()=>{
//ex.each(items,(ii)=>{
//    bb[0].selectize.removeOption(ii)
//})
//bb[0].selectize.clearOptions()
        if(self.head.options){
          bb[0].selectize.addOption(self.head.options)
        }

//bb[0].selectize.setValue(items, true)
      })
      this.selectize = bb

    },100)



  },
  methods:{
    async onClick(){
      if(this.head.maxItems==1){
        if(! this.clicking){
          var selectize = this.selectize[0].selectize
          this.clicking =true
           var value =   selectize.getValue() //this.row[this.head.name] //
          if(!value){
            value = this.last_value  // 因为点击文件时，可能会把文字删除掉。
          }
          selectize.clear()
          setTimeout(()=>{
            console.log('value=',value)
            console.log('last_value=',this.last_value)
            selectize.setTextboxValue(value)
          },10)
          setTimeout(()=>{
            console.log('clear last_value')
            this.clicking = false
          },100)
        }
      }
    }
  }
}
</script>
<style scoped lang="scss">
.com-field-split-text{
  width: 23rem;
  //min-width:300px;
  //max-width:500px;
  //.my-input-field{
  //  min-width:300px;
  //  max-width:500px;
  //}

}

::v-deep{
  .selectize-control.single .selectize-input{
    background-image: none;
    background-color: white;
    border-color: #d9d9d9;
  }
}
</style>



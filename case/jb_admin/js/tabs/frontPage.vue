<template>
  <div class="myfront">
<!--    <com-form-one :ctx="$attrs.tab_head.fields_ctx"></com-form-one>-->
    <compnent :is="$attrs.tab_head.inn_editor_list[index]" v-bind="$attrs" @finish="onFinish"></compnent>
<!--    <com-tab-form v-bind="$attrs"></com-tab-form>-->
  </div>

</template>
<script>
export default {
  data(){
    return {
      index:0,
    }
  },

  methods:{
    onFinish(){
      this.index+=1
      console.log('finish')
      // if(this.$attrs.next_express){
      //   ex.eval(this.$attrs.next_express,{vc:this})
      // }else{
      //   this.index+=1
      // }

    }
  }
}
</script>
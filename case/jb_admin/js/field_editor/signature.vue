<template>
  <div class="com-field-signature">
    <img v-if="row[head.name]" :src="row[head.name]" alt="">
    <template v-if="!head.readonly">
      <el-button v-if="!row[head.name]" @click="open_signature_win" size="mini">请签名</el-button>
      <el-button v-else @click="open_signature_win"  size="mini">重新签名</el-button>
    </template>

    <input v-if="!head.readonly" type="text" style="display: none" :id="'id_'+head.name" :name="head.name" v-model="row[head.name]">
  </div>
</template>
<script>
import popSignature from './auxuis/popSignature.vue'
export default {
  props:['row','head'],
  methods:{
    async open_signature_win(){
      var option={
        area:['600px', '600px'],
        title:'签字'
      }
        var resp = await cfg.pop_vue_com(popSignature,{title:'签字',},option)
      this.row[this.head.name] = resp
    }
  }
}
</script>
<style scoped lang="scss">
.com-field-signature{
  display: flex;
  align-items: flex-end;
  img{
    max-width: 200px;
    max-height: 200px;
    background-color: white;
    border: 1px solid #ebebeb;
    margin-right: 20px;
  }
}
</style>
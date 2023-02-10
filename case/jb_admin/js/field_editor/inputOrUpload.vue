<template>
  <div>
    <div class="switch-pannel">
      <i class="fa fa-cloud-upload" :class="{active:crt_view=='upload'}"
         title="上传"
         aria-hidden="true" @click="crt_view='upload'"></i>
      <i class="fa fa-pencil-square-o" aria-hidden="true"
         title="输入"
         :class="{active:crt_view=='input'}"
         @click="crt_view='input'"></i>
    </div>

    <slot name="upload" v-if="crt_view=='upload'">
      <com-field-plain-file :row="row" :head="head" ></com-field-plain-file>
    </slot>
    <slot name="input">
      <lineText :row="row" :head="head" v-if="crt_view=='input'"></lineText>
    </slot>

  </div>
</template>
<script>
import lineText from "./lineText.vue";

export default  {
  components:{
    lineText
  },
  props:['row','head'],
  data(){
    return {
      crt_view:'upload'
    }
  }
}
</script>
<style scoped lang="scss">
.switch-pannel{
  position: relative;
  .fa{
    display: inline-block;
    padding: 0px 7px;
    margin: 2px 0;
    cursor: pointer;
  }
  .active{
    color: blue;
    background-color: white;
  }

  &:after{
    content: '';
    display: block;
    width: 128px;
    height: 1px;
    background-color: #e9e9e9;
    left: 0;
    bottom: 0;
  }
}
</style>
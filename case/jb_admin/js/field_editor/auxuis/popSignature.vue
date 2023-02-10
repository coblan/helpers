<template>
  <div class="pop-signature">
    <div style="display: flex;justify-content: center;">
      <div class="can-wrap">
        <canvas class="my-can" width="600" height="400" style="background-color: white"></canvas>
      </div>
    </div>


    <div style="display: flex;justify-content: flex-end;padding: 20px;">
      <el-button type="primary" size="small" @click="submit">确定</el-button>
      <el-button size="small" @click="clear">清空</el-button>
    </div>
  </div>
</template>
<script>
export default {
    mounted(){
      setTimeout(()=>{
        var can = this.$el.querySelector('.my-can')
        this. signaturePad = new SignaturePad(can)
      },100)
    },
    methods:{
      async submit(){

        var image_data = this.signaturePad.toDataURL()
        var resp = await ex.director_post('save/dataurl/png',{dataurl:image_data})
        this.$emit('finish',resp)
      },
      clear(){
        this. signaturePad.clear();
      }
    }
}

</script>
<style scoped lang="scss">
.pop-signature{
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f6f6f6;
}
.can-wrap{
}
.my-can{
  //height: 400px;
  //width: 600px;
}
</style>
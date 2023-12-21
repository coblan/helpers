<template>
  <div class="com-table-multi-file" style="white-space: nowrap">
    <div class="file-wrap" v-for="image in image_list">
      <img v-if="isImage(image)"  :title="image"
           @click="big_win(image)" style="max-width: 100%;max-height: 100%"  :src="image" alt="图片不能显示">
      <div v-else :title="image" @click="tryOpen(image)">
          {{getSuffix(image) .toUpperCase() }}
      </div>

    </div>

  </div>
</template>
<script>
export default {
  props:['rowData','field','index'],
  computed:{
    image_list:function(){
      if(this.rowData[this.field]){
        return this.rowData[this.field]
      }else{
        return []
      }
    }
  },
  methods:{
    big_win:function(imgsrc){
      var ctx = {imgsrc:imgsrc}
      pop_layer(ctx,'com-pop-image',function(){},{
        title:false,
        area: ['90%', '90%'],
        shade: 0.8,
        skin: 'img-shower',
        shadeClose: true,
      })
    },
    isImage(src){
      var ls =['.jpg','.jpeg','.png','.gif']
      var is_img = false
      ex.each(ls,sufix=>{
        if(src.toLowerCase().endsWith(sufix)){
          is_img =true
        }
      })
      return is_img
    },
    tryOpen(src){
      var sufix = this.getSuffix(src)
      if(['pdf'].includes(sufix)){
        window.open(src)
      }else{
        cfg.toast('该文件格式暂不能在线查看，请下载查看!')
      }
    },

    getSuffix(src){
      var rt  = /\.(\w+)$/.exec(src)
      if(rt){
        return rt[1]
      }else{
        return  '其他'
      }
    },

  }

}
</script>
<style scoped lang="scss">
.com-table-multi-file{
  display: flex;
  flex-shrink: 0;
  //flex-wrap: wrap;
  gap:5px;
}
.file-wrap{
  cursor: pointer;
  width: 40px;
  height: 40px;
  border: 1px solid #efefef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}
</style>


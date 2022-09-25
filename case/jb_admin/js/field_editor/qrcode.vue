<template>
  <div class="com-field-qrcode" :class="head.class">
    <div class="qr-pad" v-if="mytext"></div>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  async mounted(){
    await  ex.load_js(cfg.js_lib.qrcode)
  },
  computed:{
    mytext(){
      return this.row[this.head.name]
    }
  },
  watch:{
    mytext(nv){
      if(nv){
        Vue.nextTick(()=>{
          this.genQrcode()
        })

      }
    }
  },
  methods:{
    genQrcode(){
      var dom = this.$el.querySelector('.qr-pad')
      var qrcode = new QRCode(dom, {
        text: this.mytext,
        width: 108,
        height: 108,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
      });
    }
  }
}
</script>
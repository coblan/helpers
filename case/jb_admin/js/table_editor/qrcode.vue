<template>
  <div style="padding: 10px">
    <div class="qr-pad"></div>
  </div>
</template>
<script>
export  default {
  props:['rowData','field','index'],
  async mounted(){
    await  ex.load_js(cfg.js_lib.qrcode)
    this.genQrcode()
  },
  methods:{
    genQrcode(){
      var dom = this.$el.querySelector('.qr-pad')
      var qrcode = new QRCode(dom, {
        text: this.rowData[this.field],
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
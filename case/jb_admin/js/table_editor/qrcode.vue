<template>
  <div style="padding: 10px;height: 125px;width: 125px" @click="open_qr">
    <div class="qr-pad clickable"></div>
  </div>
</template>
<script>

var qrcode_show = {
  template:`<div style="padding: 10px;background-color: white;position: absolute;left: 50%;top:50%;transform: translate(-50%,-50%)">
      <div class="qr-pad"></div>
  </div>`,
  props:{
    text:{}
  },
  mounted(){
    this.genQrcode()
  },
  methods:{
    genQrcode(){
      var dom = this.$el.querySelector('.qr-pad')
      var qrcode = new QRCode(dom, {
        text: this.text,
        width: 324,
        height: 324,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
      });
    },
  }
}

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
    },
    open_qr(){
      cfg.pop_vue_com(qrcode_show,{text:this.rowData[this.field]},{
        title:false,
        area: ['90%', '90%'],
        shade: 0.8,
        skin: 'img-shower',
        shadeClose: true,
      })
    }
  }
}
</script>

<template>
  <div class="com-field-ratio-number" :class="head.class" :style="head.style">
    <div v-if='head.readonly'>
      <span class="readonly-info"  v-text='inn_value'></span>
      <span v-text="head.suffix"></span>
    </div>
    <div  v-else  class="form-inline test1">
      <el-input v-model="inn_value" size="small" :placeholder="head.placeholder"
                :id="'id_'+head.name" :name="head.name"
                @keypress.native="isNumber($event)"
                :maxlength="head.maxlength">
        <template v-slot:prepend >
          <span  v-if="head.prefix" v-html="head.prefix"></span>
        </template>
        <template v-slot:append>
          <span  v-if="head.suffix" v-html="head.suffix"></span>
        </template>
      </el-input>
    </div>
  </div>
</template>
<script>

export default {
  props:{
    row:{},
    head:{},
  },
  data(){
    return {
      inn_value:this.row[this.head.name] * this.head.ratio,
    }
  },
  computed:{
    out_value(){
      return this.row[this.head.name]
    }
  },
  watch:{
    inn_value(nv){
        this.row[this.head.name] = nv / this.head.ratio
    },
    out_value(){
      this.inn_value = this.out_value * this.head.ratio
    }
  },
  methods:{
    isNumber(evt){
      evt = (evt) ? evt : window.event;
      var charCode = (evt.which) ? evt.which : evt.keyCode;
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
  }
}
</script>


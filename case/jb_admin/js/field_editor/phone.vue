<template>
  <div class="com-field-phone" :class="head.class" :style="head.style">
    <div v-if='head.readonly'>
      <span class="readonly-info"  v-text='row[head.name]'></span>
    </div>
    <div  v-else  class="form-inline test1">
      <slot name="inputbody">
        <el-input v-model="phone" size="small" :placeholder="head.placeholder"
                  :id="'id_'+head.name" :name="head.name"
                  :maxlength="head.maxlength">
          <template v-slot:prepend >
            <el-select v-model="contry_code" placeholder="区号"  class="contry-code">
              <el-option
                  v-for="item in contry_code_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
              </el-option>
            </el-select>
          </template>
        </el-input>
      </slot>

    </div>
  </div>
</template>
<script>
export default {
  props:['row','head'],
  data(){
    return {
      contry_code: this.head.contry_code?this.head.contry_code[0]: '',
      phone:'',
      contry_code_options:[]
    }
  },
  mounted(){
    this.contry_code_options = ex.map(this.head.contry_code,item=>{
      return {value:item,label:item}
    })
    this.updateData()
  },
  watch:{
    contry_code(nv){
      debugger
      if(this.head.splitter){
        this.row[this.head.name] = `${nv}${this.head.splitter}${this.phone}`
      }
    },
    phone(nv){
      if(this.head.splitter){
        this.row[this.head.name] = `${this.contry_code}${this.head.splitter}${nv}`
      }else{
        this.row[this.head.name] = nv
      }
    }
  },
  methods:{
    updateData(){
      var value = this.row[this.head.name]
      debugger
      if(this.head.splitter && value){
        var ls = value.split(this.head.splitter)
        this.contry_code = ls[0]
        this.phone = ls[1]
      }
    }
  }
}
</script>
<style scoped lang="scss">
.contry-code{
  /deep/ {
    .el-input__inner{
      width: 100px;
    }
  }
}
</style>
<template>
  <div class="com-field-number" :class="head.class" :style="head.style">
    <div v-if='head.readonly'>
      <span class="readonly-info"  v-text='row[head.name]'></span>
      <span v-text="head.suffix"></span>
    </div>
    <div  v-else  class="form-inline test1">
        <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder"
                  :id="'id_'+head.name" :name="head.name"
                  @keypress.native="isNumber($event)"
                  @blur="onBlur"
                  @focus="onFocus"
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
      mounted(){
        if(this.head.mounted_express){
          ex.eval(this.head.mounted_express,{vc:this,head:this.head})
        }

      },
      beforeUnmount(){
         console.log('beforeUnmount')
      },
      unmounted(){
        console.log('Unmount')
      },
      methods:{
        isNumber(evt){
          console.log('input ...  .... ')
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
        },
        onBlur(){
          if(this.inter_index){
            clearInterval(this.inter_index)
            this.inter_index=''
          }
          // this.filterIllegal()
        },
        onFocus(){
          this.inter_index = setInterval(this.filterIllegal,500)
        },
        filterIllegal(){
          var value = this.row[this.head.name]
          const newValue =
              value
                  .replace(/[^\d^\.^-]+/g, '')   // 把不是数字，不是小数点的过滤掉
                  .replace(/^0+(\d)/, '$1')      // 以0开头，0后面为数字，则过滤掉，取后面的数字
                  .replace(/^-0+(\d)/, '-$1')    // 以-0开头，0后面为数字，则过滤掉，取后面的数字
                  .replace(/-/g, (match, offset) => offset === 0 ? '-' : '') // 只允许第一个是负号-
                  .replace(/\./, '#').replace(/\./, '').replace(/#/, '\.') // 只保留第一个小数点

          this.row[this.head.name] = newValue
        }
      }
    }
</script>


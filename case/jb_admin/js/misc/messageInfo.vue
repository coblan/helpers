<template>
  <div class="com-message-rows">
    <div class="inn-wrap">
      <table>
        <tr  v-for='(row,index) in ctx.messages' :key="index">
          <td class="my-number">
            <span>{{index+1}}:</span>
          </td>
          <td>
            <template v-if="row.type">
              <span :class="row.type">{{row.message}}</span>
            </template>
            <span v-else>{{row}}</span>
          </td>
        </tr>
      </table>
    </div>
  </div>

</template>
<script>
/*
* ctx: {messages}
* */
export default {
  props:{
    ctx:{}
  },
  unmounted(){
    this.$emit('finish')
  },
  computed:{
    length(){
      return this.ctx.messages.length
    }
  },
  watch:{
    length(){
      this.scrollToBottom()
    }
  },
  methods:{
    scrollToBottom(){
      this.$nextTick(()=>{
        var div = this.$el
        div.scrollTop = div.scrollHeight;
      })

    },
  }
}
</script>
<style scoped lang="scss">
.com-message-rows{
  height: 100%;
  width: 100%;
  overflow: auto;
}
.inn-wrap{
  display: grid;
  grid-template-columns: auto 1fr;
}
.my-number{
  padding: 0 10px;
  background-color: #e8e8e8;
  text-align: right;
}
.error{
  color: red;
}
</style>
<template>
  <div class="com-field-json-edit">
    <div style="padding-bottom: 5px;" v-if="head.dif &&content_changed">
      <el-button icon="el-icon-warning" type="success" plain  @click="difOperation()"  size="mini">比较变化</el-button>
    </div>

      <div class="editor" style="width: 600px; height: 400px;"></div>
  </div>
</template>
<script>
// import mycodeDif from './mycodeDif.vue'
// Vue.component('mycode-dif', async (resolve, reject)=> {
//   // await ex.load_js('https://cdn.jsdelivr.net/npm/@vue/composition-api@1.7.1')
//   await ex.load_js('https://cdn.jsdelivr.net/npm/v-code-diff@1.5.1/dist/v2/index.umd.js')
//   Vue.use(CodeDiff)
//   resolve(mycodeDif)
//
// })

export default {
  props:['row','head'],

  data(){
      return {
        inn_value:this.row[this.head.name],
        content_changed:false
      }
  },
  mounted(){
    this.initData()
    var par = ex.vueParStore(this)
    par.vc.before_submit.push(this.updateData )
  },
  computed:{
      out_value(){
        return this.row[this.head.name]
      }
  },
  watch:{
    out_value(nv){
        this.inn_value = this.row[this.head.name]
        this.updateEditorData()
    }
  },
  methods:{
    async initData(){
      var self = this
      ex.load_css(cfg.js_lib.jsoneditor_css)
      await ex.load_js(cfg.js_lib.jsoneditor)
      if(self.head.readonly){
        var options = {
          mode: 'view',
          // modes: ['code', 'form', 'text', 'tree', 'view', 'preview']
          modes: [ 'view', 'preview']
        }
      }else{
        var options = {
          mode: 'code',
          // modes: ['code', 'form', 'text', 'tree', 'view', 'preview']
          modes: ['code', 'form', 'tree', 'view', 'preview'],
          onChange(e){
              self.content_changed=true
          }
        }
      }

      var value =  this.inn_value  //this.row[this.head.name]

      this. editor = new JSONEditor(this.$el.querySelector('.editor'), options)

      // set json
      if(!value){
        var initialJson = ex.eval(this.head.default_value_express,{vc:this})  || {}
      } else if(typeof value =='string'){
        var initialJson = JSON.parse(this.row[this.head.name])
      }else{
        var initialJson = value
      }

      this.editor.set(initialJson)
      this.old_string = this.editor.getText()
        // get json
        // const updatedJson = editor.get()

    },
    updateEditorData(){
      var value =  this.inn_value  //this.row[this.head.name]

      if(!value){
        var initialJson = ex.eval(this.head.default_value_express,{vc:this})  || {}
      } else if(typeof value =='string'){
        var initialJson = JSON.parse(this.row[this.head.name])
      }else{
        var initialJson = value
      }
      this.editor.set(initialJson)
      this.old_string = this.editor.getText()
    },
    updateData(){
      this.row[this.head.name] = JSON.stringify( this.editor.get() )
      this.content_changed=false
    },
    async difOperation(){
      /*
      *  <code-diff
        old-string="const a = 1"
        :new-string="'const a = 2\nlet b = 3'"
        language="javascript"
        output-format="side-by-side"
      ></code-diff>
      * */

      // Vue.use(window. CodeDiff);
      // debugger
      // await ex.load_js('https://cdn.jsdelivr.net/npm/@vue/composition-api@1.7.1')
      // await ex.load_js('https://cdn.jsdelivr.net/npm/v-code-diff@1.5.1/dist/v2/index.umd.js')
      // Vue.use(window.CodeDiff)
      // debugger
      // await ex.load_js('https://cdn.jsdelivr.net/npm/@vue/composition-api@1.7.1')
      // await ex.load_js('https://cdn.jsdelivr.net/npm/v-code-diff@1.5.1/dist/v2/index.umd.js')
      await ex.load_js('https://cdn.jsdelivr.net/npm/v-code-diff@1.5.1/dist/v2/index.umd.js')
      Vue.use(CodeDiff)
      Vue.nextTick(()=>{
        var old_string = this.old_string
        var new_string =  this.editor.getText()
        cfg.pop_vue_com('code-diff',{title:'比较内容',
          oldString:old_string , // '111',
          newString:new_string , // 'const a = 2\\nlet b = 3',
          language:'javascript',
          outputFormat:'side-by-side'})
      })


      // cfg.pop_vue_com('mycode-dif',{title:'比较内容',
      //   oldString:'111',
      //   newString:'const a = 2\\nlet b = 3',
      //   language:'javascript',
      //   outputFormat:'side-by-side'})
    }
  }
}
</script>
<style scoped lang="scss">
.com-field-json-edit{
  width: 100%;
  .inn-wrap{
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
  }
}
::v-deep{
  .jsoneditor-menu a.jsoneditor-poweredBy{
    display: none;
  }
}
</style>
